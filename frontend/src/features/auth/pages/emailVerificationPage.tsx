import { useLocation, useNavigate } from "react-router-dom";
import React, { useState, useEffect } from "react";
import { authHooks } from "../hooks/authHooks";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";

export function emailVerificationPage() {
  const { verifyEmail, resendVerification, isLoading, error, clearError } =
    authHooks();
  const [code, setCode] = useState("");
  const [resendTimer, setResendTimer] = useState(0);
  const [successMessage, setSuccessMessage] = useState("");
  const [isRedirecting, setisRedirecting] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();

  const userIdFromState = location.state?.userId as number | undefined;
  const emailFromState = location.state?.email as string | undefined;

  const userIdFromStorage = localStorage.getItem(
    "pending_verification_user_id"
  );
  const emailFromStorage = localStorage.getItem("pending_verification_email");

  let parsedUserId: number | undefined = undefined;
  if (userIdFromStorage) {
    const parsed = parseInt(userIdFromStorage, 10);
    parsedUserId = !isNaN(parsed) ? parsed : undefined;
  }

  const user_id = userIdFromState || parsedUserId;
  const email = emailFromState || emailFromStorage || undefined;

  useEffect(() => {
    if (!user_id) {
      navigate("/register");
    }
  }, [user_id, navigate]);

  useEffect(() => {
    let interval: number | undefined;
    if (resendTimer > 0) {
      interval = setInterval(() => {
        setResendTimer((prev) => prev - 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [resendTimer]);

  const handleVerification = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user_id || code.length !== 6) return;

    try {
      const response = await verifyEmail({ user_id: user_id, code });
      if (response.success) {
        localStorage.removeItem("pending_verification_user_id");
        localStorage.removeItem("pending_verification_email");

        setSuccessMessage("Email verified successfully");
        setisRedirecting(true);

        setTimeout(() => {
          navigate("/login", {
            state: {
              autoLogin: true,
              email: email,
              message: "Email verified! Please log in to continue",
            },
          });
        }, 2000);
      }
    } catch (error) {
      /* error handler in here */
    }
  };

  const handleCodeChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.replace(/\D/g, "").slice(0, 6);
    setCode(value);
    if (error) clearError();
  };

  const handleResendVerification = async () => {
    if (!user_id || resendTimer > 0) return;

    try {
      const response = await resendVerification(user_id);
      if (response?.success) {
        setSuccessMessage("Verification code sent! Check your email");
        setResendTimer(60);
        setTimeout(() => setSuccessMessage(""), 3000);
      }
    } catch (error) {
      console.error("Resend verification error:", error);
    }
  };

  if (!user_id) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-white">
        <LoadingSpinner />
      </div>
    );
  }

  if (isRedirecting) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-white">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 mb-4">
            <svg
              className="w-8 h-8 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            Verification Successful!
          </h3>
          <p className="text-gray-600 text-sm">Redirecting you to login...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Illustration */}
      <div className="hidden lg:flex lg:w-1/2 bg-gray-50 items-center justify-center p-12">
        <div className="max-w-lg w-full text-center">
          <div className="mb-16">
            <h1 className="text-4xl font-bold text-gray-900 mb-4 leading-tight">
              Check Your Email
            </h1>
            <p className="text-lg text-gray-600 leading-relaxed">
              We've sent a verification code to your email address
            </p>
          </div>

          {/* Image placeholder - Replace with your illustration */}
          <div className="flex items-center justify-center">
            <img
              src="/yellow.svg"
              alt="Email verification illustration"
              className="w-full max-w-2xl object-contain"
              onError={(e) => {
                e.currentTarget.style.display = "none";
              }}
            />
          </div>
        </div>
      </div>

      {/* Right Side - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12 bg-white">
        <div className="w-full max-w-md">
          {/* Header */}
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Verify Your Email
            </h2>
            <p className="text-gray-600 text-sm mb-1">
              We've sent a 6-digit code to
            </p>
            <p className="text-gray-900 font-semibold text-sm">
              {email || "your email"}
            </p>
          </div>

          {/* Messages */}
          {successMessage && !isRedirecting && (
            <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
              {successMessage}
            </div>
          )}

          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleVerification} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3 text-center">
                Enter Verification Code
              </label>
              <input
                id="code"
                type="text"
                value={code}
                onChange={handleCodeChange}
                placeholder="000000"
                maxLength={6}
                className="w-full px-4 py-4 border border-gray-300 rounded-lg text-center text-2xl font-bold tracking-widest focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
                autoFocus
              />
              <p className="mt-2 text-xs text-gray-500 text-center">
                Enter the 6-digit code from your email
              </p>
            </div>

            <button
              type="submit"
              disabled={isLoading || code.length !== 6}
              className="w-full bg-amber-400 text-gray-900 py-3 rounded-lg text-sm font-semibold hover:bg-amber-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
            >
              {isLoading ? "Verifying..." : "Verify Email"}
            </button>
          </form>

          {/* Resend Section */}
          <div className="mt-8 pt-6 border-t border-gray-200 text-center">
            <p className="text-xs text-gray-600 mb-3">
              Didn't receive the code?
            </p>
            <button
              type="button"
              onClick={handleResendVerification}
              disabled={!user_id || resendTimer > 0 || isLoading}
              className="text-gray-900 hover:underline font-semibold text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {resendTimer > 0 ? `Resend in ${resendTimer}s` : "Resend Code"}
            </button>
          </div>

          {/* Help Text */}
          <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-xs text-gray-700 font-medium mb-1">
              💡 Check your spam folder
            </p>
            <p className="text-xs text-gray-600 leading-relaxed">
              If you don't see the email in your inbox, it might be in your spam
              or junk folder.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
