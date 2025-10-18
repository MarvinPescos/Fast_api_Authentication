import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import api from "../../../shared/services/api";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";
import { PasswordInput } from "../../../shared/components/PasswordInput";

export function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const [code, setCode] = useState(searchParams.get("code") || "");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const validatePassword = () => {
    if (newPassword.length < 8) {
      setError("Password must be at least 8 characters long");
      return false;
    }
    if (!/[A-Z]/.test(newPassword)) {
      setError("Password must contain at least one uppercase letter");
      return false;
    }
    if (!/[a-z]/.test(newPassword)) {
      setError("Password must contain at least one lowercase letter");
      return false;
    }
    if (!/\d/.test(newPassword)) {
      setError("Password must contain at least one number");
      return false;
    }
    if (newPassword !== confirmPassword) {
      setError("Passwords do not match");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validatePassword()) {
      return;
    }

    setIsLoading(true);

    try {
      await api.post("/fullstack_authentication/auth/password/reset", {
        code,
        new_password: newPassword,
      });
      setSuccess(true);
      setTimeout(() => navigate("/login"), 3000);
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Failed to reset password. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-amber-50 to-orange-50">
        <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full mx-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
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
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Password Reset Successful!
            </h2>
            <p className="text-gray-600 mb-6">
              Your password has been successfully reset. You'll be redirected to
              the login page shortly.
            </p>
            <LoadingSpinner size="sm" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-amber-50 to-orange-50">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full mx-4">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Reset Password
          </h2>
          <p className="text-gray-600">
            Enter your reset code and new password
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label
              htmlFor="code"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Reset Code
            </label>
            <input
              type="text"
              id="code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Enter the code from your email"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent font-mono"
              required
            />
            <p className="mt-1 text-xs text-gray-500">
              Check your email for the reset code
            </p>
          </div>

          <PasswordInput
            id="newPassword"
            label="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            placeholder="Enter new password"
            required
            minLength={8}
          />

          <PasswordInput
            id="confirmPassword"
            label="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm new password"
            required
            minLength={8}
          />

          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-xs text-gray-600 mb-2 font-medium">
              Password must contain:
            </p>
            <ul className="text-xs text-gray-600 space-y-1">
              <li className="flex items-center gap-2">
                <span
                  className={newPassword.length >= 8 ? "text-green-600" : ""}
                >
                  {newPassword.length >= 8 ? "✓" : "•"}
                </span>
                At least 8 characters
              </li>
              <li className="flex items-center gap-2">
                <span
                  className={/[A-Z]/.test(newPassword) ? "text-green-600" : ""}
                >
                  {/[A-Z]/.test(newPassword) ? "✓" : "•"}
                </span>
                One uppercase letter
              </li>
              <li className="flex items-center gap-2">
                <span
                  className={/[a-z]/.test(newPassword) ? "text-green-600" : ""}
                >
                  {/[a-z]/.test(newPassword) ? "✓" : "•"}
                </span>
                One lowercase letter
              </li>
              <li className="flex items-center gap-2">
                <span
                  className={/\d/.test(newPassword) ? "text-green-600" : ""}
                >
                  {/\d/.test(newPassword) ? "✓" : "•"}
                </span>
                One number
              </li>
              <li className="flex items-center gap-2">
                <span
                  className={
                    newPassword && newPassword === confirmPassword
                      ? "text-green-600"
                      : ""
                  }
                >
                  {newPassword && newPassword === confirmPassword ? "✓" : "•"}
                </span>
                Passwords match
              </li>
            </ul>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full px-4 py-3 bg-amber-400 text-gray-900 font-semibold rounded-lg hover:bg-amber-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" />
                <span className="ml-2">Resetting...</span>
              </>
            ) : (
              "Reset Password"
            )}
          </button>
        </form>

        <div className="mt-6 text-center space-y-2">
          <Link
            to="/forgot-password"
            className="block text-amber-600 hover:text-amber-700 font-medium text-sm"
          >
            Resend Reset Code
          </Link>
          <Link
            to="/login"
            className="block text-gray-600 hover:text-gray-700 text-sm"
          >
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
}
