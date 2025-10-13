import { Button } from "../../../shared/components/Button";
import { useForm } from "../../../shared/components/Form";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";

import { useLocation } from "react-router-dom";
import React, { useState, useEffect } from "react";

import { authHooks } from "../hooks/authHooks";
import { type loginRequest } from "../schemas/login.schema";

export function loginPage() {
    const {login, isLoading, error, clearError} = authHooks();
    const location = useLocation();
    const [verificationMessage, setVerificationMessage] = useState("");
    
    const {form: credentials, handleChange} = useForm<loginRequest>({
        email: location.state?.email || "",
        password: "",
    });

    useEffect(() => {
        if(location.state?.message){
            setVerificationMessage(location.state.message);

            const timer = setTimeout(() => {
                setVerificationMessage("");
            }, 5000);

            return () => clearTimeout(timer)
        }
    }, [location.state.message]);

    const handleLogin = async(e: React.FormEvent) => {
        e.preventDefault()
        try{
            await login(credentials)
        } catch (error) { 
            // error handlers here
        }
    }

    return (
        <>
        <h2>Login haha</h2>
        <form onSubmit={handleLogin}>
            {verificationMessage && (
            <div className="bg-green-50 border-green-200 text-green-700 px-4 py-3 rounded mb-4">
                {verificationMessage}
            </div>
            )}
            {error && (
                <div className="bg-red-50 border-red-50 text-red-700 px-4 py-3 rounded mb-4">
                    {error}
                </div>
            )}
            <input
                id="email"
                name="email"
                type="email"
                placeholder="Email"
                value={credentials.email}
                onChange={handleChange}
                onFocus={() => error && clearError}
                required
            />
            <input
                id="password"
                name="password"
                type="password"
                placeholder="Password"
                value={credentials.password}
                onChange={handleChange}
                onFocus={() => error && clearError}
                required
            />
            <Button type="submit" isLoading={isLoading} className="w-full">
                Sign in
            </Button>
        </form>

        </>
    )


}