import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { ActivityLayout } from "../../../shared/components/ActivityLayout";
import { useAuthStore } from "../store/authStore";
import { authService } from "../services/auth.service";
import { PasswordInput } from "../../../shared/components/PasswordInput";
import api from "../../../shared/services/api";

export function ProfilePage() {
  const { user, setUser } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [editingProfile, setEditingProfile] = useState(false);
  const [editingPassword, setEditingPassword] = useState(false);

  // 2FA states
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);
  const [twoFactorLoading, setTwoFactorLoading] = useState(false);
  const [show2FASetup, setShow2FASetup] = useState(false);
  const [qrCode, setQrCode] = useState<string | null>(null);
  const [twoFactorSecret, setTwoFactorSecret] = useState<string | null>(null);
  const [verificationCode, setVerificationCode] = useState("");

  // Initialize form with user data
  useEffect(() => {
    if (user) {
      setUsername(user.username || "");
      setFullName(user.full_name || "");
    }
  }, [user]);

  // Check 2FA status
  useEffect(() => {
    check2FAStatus();
  }, []);

  const check2FAStatus = async () => {
    try {
      const response = await api.get(
        "/fullstack_authentication/auth/2fa/status"
      );
      setTwoFactorEnabled((response as any).enabled);
    } catch (error) {
      // Silently fail - 2FA status check is not critical
    }
  };

  const setup2FA = async () => {
    setTwoFactorLoading(true);
    setError(null);
    try {
      const response = await api.post(
        "/fullstack_authentication/auth/2fa/setup"
      );
      setQrCode((response as any).qr_code);
      setTwoFactorSecret((response as any).secret);
      setShow2FASetup(true);
    } catch (error: any) {
      setError(error.response?.data?.detail || "Failed to setup 2FA");
    } finally {
      setTwoFactorLoading(false);
    }
  };

  const enable2FA = async () => {
    if (!verificationCode || verificationCode.length !== 6) {
      setError("Please enter a valid 6-digit code");
      return;
    }

    setTwoFactorLoading(true);
    setError(null);
    try {
      await api.post("/fullstack_authentication/auth/2fa/enable", {
        token: verificationCode,
      });
      setTwoFactorEnabled(true);
      setShow2FASetup(false);
      setSuccess("Two-factor authentication enabled successfully!");
      setTimeout(() => setSuccess(null), 5000);
    } catch (error: any) {
      setError(error.response?.data?.detail || "Failed to enable 2FA");
    } finally {
      setTwoFactorLoading(false);
    }
  };

  const disable2FA = async () => {
    if (!currentPassword) {
      setError("Current password is required to disable 2FA");
      return;
    }

    if (!verificationCode || verificationCode.length !== 6) {
      setError("Please enter a valid 6-digit code");
      return;
    }

    setTwoFactorLoading(true);
    setError(null);
    try {
      await api.post("/fullstack_authentication/auth/2fa/disable", {
        password: currentPassword,
        token: verificationCode,
      });
      setTwoFactorEnabled(false);
      setSuccess("Two-factor authentication disabled successfully!");
      setTimeout(() => setSuccess(null), 5000);
    } catch (error: any) {
      setError(error.response?.data?.detail || "Failed to disable 2FA");
    } finally {
      setTwoFactorLoading(false);
    }
  };

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);

    try {
      // Build update payload
      const updateData: any = {};

      // Add profile fields if they changed
      if (username !== user?.username) updateData.username = username;
      if (fullName !== user?.full_name) updateData.full_name = fullName;

      // Check if anything changed
      if (Object.keys(updateData).length === 0) {
        setError("No changes detected");
        setLoading(false);
        return;
      }

      const updatedUser = await authService.updateProfile(updateData);
      setUser(updatedUser);
      setSuccess("Profile updated successfully!");
      setEditingProfile(false);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Failed to update profile. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Validate passwords
    if (!currentPassword) {
      setError("Current password is required");
      return;
    }

    if (!newPassword) {
      setError("New password is required");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("New passwords do not match");
      return;
    }

    if (newPassword.length < 8) {
      setError("New password must be at least 8 characters");
      return;
    }

    setLoading(true);

    try {
      await authService.updateProfile({
        current_password: currentPassword,
        new_password: newPassword,
      });

      setSuccess("Password changed successfully!");
      setEditingPassword(false);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          "Failed to change password. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ActivityLayout
      title="Profile Settings"
      description="Manage your account information and security"
      currentPath="/profile"
    >
      <div className="max-w-3xl mx-auto">
        {/* Success Message */}
        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 text-green-500 mr-2"
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
              <span className="text-green-800 font-medium">{success}</span>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 text-red-500 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
              <span className="text-red-800 font-medium">{error}</span>
            </div>
          </div>
        )}

        {/* Profile Information Section */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              Profile Information
            </h2>
            {!editingProfile && (
              <button
                onClick={() => setEditingProfile(true)}
                className="px-4 py-2 text-sm font-medium text-amber-700 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors"
              >
                Edit Profile
              </button>
            )}
          </div>

          {!editingProfile ? (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  Username
                </label>
                <p className="text-gray-900">{user?.username || "Not set"}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  Full Name
                </label>
                <p className="text-gray-900">{user?.full_name || "Not set"}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-600 mb-1">
                  Account Status
                </label>
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    user?.is_active
                      ? "bg-green-100 text-green-800"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {user?.is_active ? "Active" : "Inactive"}
                </span>
              </div>
            </div>
          ) : (
            <form onSubmit={handleUpdateProfile} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Username
                </label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                  placeholder="Enter username"
                  minLength={3}
                  maxLength={50}
                  required
                />
                <p className="mt-1 text-xs text-gray-500">
                  Username must be 3-50 alphanumeric characters
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                  placeholder="Enter full name"
                  maxLength={100}
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? "Saving..." : "Save Changes"}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setEditingProfile(false);
                    setUsername(user?.username || "");
                    setFullName(user?.full_name || "");
                    setCurrentPassword("");
                  }}
                  disabled={loading}
                  className="px-6 py-3 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>

        {/* Change Password Section */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Security</h2>
              <p className="text-sm text-gray-600 mt-1">
                Change your password to keep your account secure
              </p>
            </div>
            {!editingPassword && (
              <button
                onClick={() => setEditingPassword(true)}
                className="px-4 py-2 text-sm font-medium text-amber-700 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors"
              >
                Change Password
              </button>
            )}
          </div>

          {editingPassword && (
            <form onSubmit={handleChangePassword} className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Current Password
                  </label>
                  <Link
                    to="/forgot-password"
                    className="text-xs text-amber-600 hover:text-amber-700 font-medium"
                  >
                    Forgot Password?
                  </Link>
                </div>
                <PasswordInput
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="Enter current password"
                  required
                />
              </div>

              <PasswordInput
                label="New Password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="Enter new password"
                minLength={8}
                required
                helperText="Password must be at least 8 characters with uppercase, lowercase, and numbers"
              />

              <PasswordInput
                label="Confirm New Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm new password"
                minLength={8}
                required
              />

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? "Changing..." : "Change Password"}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setEditingPassword(false);
                    setCurrentPassword("");
                    setNewPassword("");
                    setConfirmPassword("");
                  }}
                  disabled={loading}
                  className="px-6 py-3 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>

        {/* Two-Factor Authentication Section */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                Two-Factor Authentication
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                Add an extra layer of security to your account
              </p>
            </div>
            <div className="flex items-center gap-3">
              <span
                className={`px-3 py-1 rounded-full text-xs font-medium ${
                  twoFactorEnabled
                    ? "bg-green-100 text-green-800"
                    : "bg-gray-100 text-gray-800"
                }`}
              >
                {twoFactorEnabled ? "Enabled" : "Disabled"}
              </span>
              {!twoFactorEnabled && !show2FASetup && (
                <button
                  onClick={setup2FA}
                  disabled={twoFactorLoading}
                  className="px-4 py-2 text-sm font-medium text-amber-700 bg-amber-50 rounded-lg hover:bg-amber-100 transition-colors disabled:opacity-50"
                >
                  {twoFactorLoading ? "Setting up..." : "Enable 2FA"}
                </button>
              )}
            </div>
          </div>

          {!twoFactorEnabled && !show2FASetup && (
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Two-Factor Authentication is Disabled
              </h3>
              <p className="text-gray-600 mb-4">
                Protect your account with an additional layer of security
              </p>
            </div>
          )}

          {show2FASetup && (
            <div className="space-y-6">
              <div className="text-center">
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Set Up Two-Factor Authentication
                </h3>
                <p className="text-gray-600 mb-4">
                  Scan the QR code with your authenticator app
                </p>
              </div>

              {qrCode && (
                <div className="flex justify-center">
                  <img
                    src={qrCode}
                    alt="2FA QR Code"
                    className="w-48 h-48 border border-gray-200 rounded-lg"
                  />
                </div>
              )}

              {twoFactorSecret && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-2">
                    Can't scan? Enter this code manually:
                  </p>
                  <code className="text-sm font-mono bg-white p-2 rounded border">
                    {twoFactorSecret}
                  </code>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Enter 6-digit code from your authenticator app
                </label>
                <input
                  type="text"
                  value={verificationCode}
                  onChange={(e) =>
                    setVerificationCode(e.target.value.replace(/\D/g, ""))
                  }
                  maxLength={6}
                  placeholder="000000"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent text-center text-lg tracking-widest font-mono"
                />
              </div>

              <div className="flex gap-3">
                <button
                  onClick={enable2FA}
                  disabled={twoFactorLoading || verificationCode.length !== 6}
                  className="flex-1 px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {twoFactorLoading ? "Enabling..." : "Enable 2FA"}
                </button>
                <button
                  onClick={() => {
                    setShow2FASetup(false);
                    setQrCode(null);
                    setTwoFactorSecret(null);
                    setVerificationCode("");
                  }}
                  disabled={twoFactorLoading}
                  className="px-6 py-3 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {twoFactorEnabled && (
            <div className="space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center">
                  <svg
                    className="w-5 h-5 text-green-500 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <span className="text-green-800 font-medium">
                    Two-factor authentication is enabled
                  </span>
                </div>
                <p className="text-green-700 text-sm mt-1">
                  Your account is protected with an additional layer of security
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Current Password (required to disable)
                </label>
                <input
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                  placeholder="Enter current password"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Enter 6-digit code from your authenticator app
                </label>
                <input
                  type="text"
                  value={verificationCode}
                  onChange={(e) =>
                    setVerificationCode(e.target.value.replace(/\D/g, ""))
                  }
                  maxLength={6}
                  placeholder="000000"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent text-center text-lg tracking-widest font-mono"
                />
              </div>

              <button
                onClick={disable2FA}
                disabled={
                  twoFactorLoading ||
                  !currentPassword ||
                  verificationCode.length !== 6
                }
                className="w-full px-6 py-3 bg-red-500 text-white font-medium rounded-lg hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {twoFactorLoading ? "Disabling..." : "Disable 2FA"}
              </button>
            </div>
          )}
        </div>
      </div>
    </ActivityLayout>
  );
}
