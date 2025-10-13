import { useLocation, useNavigate } from "react-router-dom";

import { useState, useEffect } from "react";
import { authHooks } from "../hooks/authHooks";

import { Button } from "../../../shared/components/Button";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";

export function emailVerificationPage() {
    const {verifyEmail, isLoading, error, clearError, } = authHooks();

    const [code, setCode] = useState("");
    const [resendTimer, setResendTimer] = useState(0);
    const [successMessage, setSuccessMessage] = useState("");
    const [isRedirecting, setisRedirecting] = useState(false)

    const navigate = useNavigate()
    const location = useLocation()

    const user_id = location.state?.userId
    const email = location.state?.email

    useEffect(() => {
        if(!user_id) {
            navigate('/register')
        }
    }, [user_id, navigate]);

    useEffect(() => {
        let interval: number | undefined;
        if(resendTimer > 0){
            interval = setInterval(() => {
                setResendTimer((prev) => prev - 1)
            }, 1000);
        }
        return () => clearInterval(interval)
    }, [resendTimer]);

    const handleVerification = async(e: React.FormEvent) => {
        e.preventDefault()
        if(!user_id || code.length !== 6)return;

        try {
            const response = await verifyEmail({user_id: user_id, code});
            if(response.success){
                setSuccessMessage("Email verified successfully")
                setisRedirecting(true)

                setTimeout(() => {
                    navigate('/login', {
                        state: {
                            autoLogin: true,
                            email: email,
                            message: "Email verified! Please log in to continue",
                        }
                    });
                }, 2000)
            }
        } catch (error){ /* error handler in here */}
    }

    const handleCodeChange = async(e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value.replace(/\D/g, "").slice(0, 6)
        setCode(value);
        if (error) clearError;
    };

    // Don't render until we have user_id (will redirect via useEffect if missing)
    if (!user_id) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen">
                <LoadingSpinner />
                <p className="mt-4">Redirecting...</p>
            </div>
        );
    }

    if (isRedirecting){
        return(
            <div className="flex flex-col items-center justify-center min-h-screen">
                <LoadingSpinner/>
            </div>
        )
    }

    //return of this function
    return (
        <>
            <h2>Verify your Email</h2>
            <p> We've sent a 6-digits verification codee to <strong>{email || "your email"}</strong></p>
            <br />
            <span className="text-sm">Check your spam folder if you don't see it</span>

            {error && (
                <div className="bg-red-50 border-red-200 text-red-700 px-4 py-3 rounded mb-4">
                    {error}
                </div>
            )}

            <form onSubmit={handleVerification}>
                <input
                id="code" 
                type="text" 
                value={code}
                onChange={handleCodeChange}
                placeholder="123456"
                maxLength={6}
                />

                <Button 
                type="submit"
                isLoading={isLoading}
                disabled={code.length !== 6}
                >
                    Verify Email
                </Button>

                {/* <div>
                    <p>Didn't recieve the code?</p>
                    <Button
                    type="button"
                    
                    >

                    </Button>
                </div> */}
            </form>
        </>
    )




}

