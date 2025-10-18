import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { useForm } from "../../../shared/components/Form";
import { authHooks } from "../hooks/authHooks";
import { type registerRequest } from "../schemas/register.schema";
import { PasswordInput } from "../../../shared/components/PasswordInput";

export function registerPage() {
  const {
    register,
    loginWithFacebook,
    loginWithGoogle,
    isLoading,
    error,
    clearError,
  } = authHooks();
  const navigate = useNavigate();
  const { form: userData, handleChange } = useForm<registerRequest>({
    username: "",
    email: "",
    password: "",
    fullname: "",
  });

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await register(userData);
      if (response.success && response.user_id) {
        localStorage.setItem(
          "pending_verification_user_id",
          response.user_id.toString()
        );
        localStorage.setItem("pending_verification_email", userData.email);

        navigate("/verify-email", {
          state: {
            userId: response.user_id,
            email: userData.email,
          },
        });
      }
    } catch (error) {
      //Error already handled
    }
  };

  const handleFacebookSignup = async () => {
    loginWithFacebook();
  };

  const handleGoogleSignup = async () => {
    loginWithGoogle();
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Illustration */}
      <div className="hidden lg:flex lg:w-1/2 bg-yellow-400 items-center justify-center p-12">
        <div className="max-w-lg w-full">
          <div className="mb-16">
            <h1 className="text-4xl font-bold text-gray-900 mb-4 leading-tight">
              Join Our Community
            </h1>
            <p className="text-lg text-gray-600 leading-relaxed">
              Create your account and get started with all time access and free
              features
            </p>
          </div>

          <div className="flex items-center justify-center">
            <img
              src="/yellow.svg"
              alt="Sign up illustration"
              className="w-full max-w-6xl object-contain"
              onError={(e) => {
                e.currentTarget.style.display = "none";
              }}
            />
          </div>
        </div>
      </div>

      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12 bg-white">
        <div className="w-full max-w-md">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Sign Up</h2>
            <p className="text-gray-600">
              Join to Our Community with all time access and free
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          {/* OAuth Buttons */}
          <div className="space-y-3 mb-6">
            <button
              type="button"
              onClick={handleGoogleSignup}
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium text-gray-700 disabled:opacity-50"
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              Sign Up with Google
            </button>

            <button
              type="button"
              onClick={handleFacebookSignup}
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium text-gray-700 disabled:opacity-50"
            >
              <svg
                className="w-5 h-5 text-[#1877F2]"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
              </svg>
              Sign Up with Facebook
            </button>
          </div>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-200"></div>
            </div>
            <div className="relative flex justify-center text-xs">
              <span className="px-2 bg-white text-gray-500">or with email</span>
            </div>
          </div>

          {/* Registration Form */}
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700 mb-1.5"
              >
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                placeholder="johndoe"
                value={userData.username}
                onChange={handleChange}
                onFocus={() => error && clearError()}
                className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent text-sm"
                required
              />
            </div>

            <div>
              <label
                htmlFor="fullname"
                className="block text-sm font-medium text-gray-700 mb-1.5"
              >
                Full Name
              </label>
              <input
                id="fullname"
                name="fullname"
                type="text"
                placeholder="John Doe"
                value={userData.fullname}
                onChange={handleChange}
                onFocus={() => error && clearError()}
                className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent text-sm"
                required
              />
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-1.5"
              >
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                placeholder="name@example.com"
                value={userData.email}
                onChange={handleChange}
                onFocus={() => error && clearError()}
                className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent text-sm"
                required
              />
            </div>

            <div>
              <PasswordInput
                id="password"
                name="password"
                label="Password"
                value={userData.password}
                onChange={handleChange}
                onFocus={() => error && clearError()}
                placeholder="Create a strong password"
                required
                minLength={8}
                className="text-sm px-3.5 py-2.5 focus:ring-gray-900"
                helperText="Must be at least 8 characters with uppercase, lowercase, and numbers"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-amber-400 text-gray-900 py-3 rounded-lg text-sm font-semibold hover:bg-amber-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-6 shadow-sm"
            >
              {isLoading ? "Creating account..." : "Sign Up"}
            </button>
          </form>

          {/* Footer */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{" "}
              <Link
                to="/login"
                className="text-gray-900 hover:underline font-semibold"
              >
                Login here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
