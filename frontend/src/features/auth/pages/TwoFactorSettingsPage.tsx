import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { twoFactorService } from "../services/twoFactor.service";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";
import { ActivityLayout } from "../../../shared/components/ActivityLayout";
import type {
  TwoFactorSetupResponse,
  TwoFactorEnableResponse,
} from "../types/two_factor.types";

export function TwoFactorSettingsPage() {
  const navigate = useNavigate();
  const [isEnabled, setIsEnabled] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [setupData, setSetupData] = useState<TwoFactorSetupResponse | null>(
    null
  );
  const [verificationCode, setVerificationCode] = useState("");
  const [backupCodes, setBackupCodes] = useState<string[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // For disabling 2FA
  const [showDisableModal, setShowDisableModal] = useState(false);
  const [disablePassword, setDisablePassword] = useState("");
  const [disableCode, setDisableCode] = useState("");

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    setIsLoading(true);
    try {
      const status = await twoFactorService.getStatus();
      setIsEnabled(status.enabled);
    } catch (err) {
      setError("Failed to load 2FA status");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSetupClick = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await twoFactorService.setup();
      setSetupData(data);
    } catch (err: any) {
      setError(err.message || "Failed to setup 2FA");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnableSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (verificationCode.length !== 6) {
      setError("Please enter a 6-digit code");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const response: TwoFactorEnableResponse = await twoFactorService.enable(
        verificationCode
      );
      setBackupCodes(response.backup_codes);
      setIsEnabled(true);
      setSuccess("2FA enabled successfully!");
      setSetupData(null);
      setVerificationCode("");
    } catch (err: any) {
      setError(err.message || "Failed to enable 2FA");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisable = async (e: React.FormEvent) => {
    e.preventDefault();
    if (disableCode.length !== 6) {
      setError("Please enter a 6-digit code");
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      await twoFactorService.disable(disablePassword, disableCode);
      setIsEnabled(false);
      setShowDisableModal(false);
      setDisablePassword("");
      setDisableCode("");
      setSuccess("2FA disabled successfully");
    } catch (err: any) {
      setError(err.message || "Failed to disable 2FA");
    } finally {
      setIsLoading(false);
    }
  };

  const downloadBackupCodes = () => {
    if (!backupCodes) return;
    const text = `BalanceHub 2FA Backup Codes\n\n${backupCodes.join(
      "\n"
    )}\n\nKeep these codes in a safe place!`;
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "balancehub-backup-codes.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  if (isLoading && !setupData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <ActivityLayout
      title="Two-Factor Authentication"
      description="Enhance your account security with 2FA"
      currentPath="/settings/2fa"
    >
      {/* Error/Success Messages */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg mb-6">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {success && (
        <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded-lg mb-6">
          <p className="text-green-700">{success}</p>
        </div>
      )}

      {/* Backup Codes Display */}
      {backupCodes && (
        <div className="bg-yellow-50 border-2 border-yellow-400 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-semibold text-yellow-900 mb-3 flex items-center gap-2">
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clipRule="evenodd"
              />
            </svg>
            Save Your Backup Codes
          </h3>
          <p className="text-yellow-800 mb-4">
            Save these codes in a secure location. You can use them to access
            your account if you lose access to your authenticator app.
          </p>
          <div className="bg-white p-4 rounded border border-yellow-300 mb-4">
            <div className="grid grid-cols-2 gap-2 font-mono text-sm">
              {backupCodes.map((code, index) => (
                <div key={index} className="text-gray-800">
                  {code}
                </div>
              ))}
            </div>
          </div>
          <button
            onClick={downloadBackupCodes}
            className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
          >
            Download Backup Codes
          </button>
        </div>
      )}

      {/* Main Content */}
      {!setupData && !backupCodes && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-start gap-4 mb-6">
            <div className="text-4xl">🔐</div>
            <div className="flex-1">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                Status: {isEnabled ? "Enabled ✓" : "Disabled"}
              </h3>
              <p className="text-gray-600 mb-4">
                Two-factor authentication adds an extra layer of security to
                your account by requiring a verification code from your phone in
                addition to your password.
              </p>

              {!isEnabled ? (
                <button
                  onClick={handleSetupClick}
                  disabled={isLoading}
                  className="px-6 py-3 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300"
                >
                  {isLoading ? "Loading..." : "Enable 2FA"}
                </button>
              ) : (
                <button
                  onClick={() => setShowDisableModal(true)}
                  className="px-6 py-3 bg-red-500 text-white font-medium rounded-lg hover:bg-red-600 transition-colors"
                >
                  Disable 2FA
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Setup Flow */}
      {setupData && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            Scan QR Code
          </h3>

          <div className="space-y-6">
            <div>
              <p className="text-gray-600 mb-4">
                1. Download Google Authenticator or any TOTP app
              </p>
              <p className="text-gray-600 mb-4">
                2. Scan this QR code with your authenticator app:
              </p>
              <div className="flex justify-center bg-gray-50 p-6 rounded-lg">
                <img
                  src={setupData.qr_code}
                  alt="2FA QR Code"
                  className="w-64 h-64"
                />
              </div>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-2">
                Or enter this key manually:
              </p>
              <code className="bg-white px-3 py-2 rounded border border-gray-300 text-sm font-mono block">
                {setupData.manual_entry_key}
              </code>
            </div>

            <form onSubmit={handleEnableSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  3. Enter the 6-digit code from your app:
                </label>
                <input
                  type="text"
                  value={verificationCode}
                  onChange={(e) =>
                    setVerificationCode(e.target.value.replace(/\D/g, ""))
                  }
                  maxLength={6}
                  placeholder="000000"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-center text-2xl tracking-widest font-mono"
                  required
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isLoading || verificationCode.length !== 6}
                  className="flex-1 px-6 py-3 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {isLoading ? "Verifying..." : "Verify & Enable"}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setSetupData(null);
                    setVerificationCode("");
                  }}
                  className="px-6 py-3 bg-gray-500 text-white font-medium rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Disable 2FA Modal */}
      {showDisableModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Disable Two-Factor Authentication
            </h3>
            <p className="text-gray-600 mb-6">
              To disable 2FA, please enter your password and a verification code
              from your authenticator app.
            </p>

            <form onSubmit={handleDisable} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <input
                  type="password"
                  value={disablePassword}
                  onChange={(e) => setDisablePassword(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Verification Code
                </label>
                <input
                  type="text"
                  value={disableCode}
                  onChange={(e) =>
                    setDisableCode(e.target.value.replace(/\D/g, ""))
                  }
                  maxLength={6}
                  placeholder="000000"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 text-center font-mono tracking-widest"
                  required
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="flex-1 px-6 py-3 bg-red-500 text-white font-medium rounded-lg hover:bg-red-600 transition-colors disabled:bg-gray-300"
                >
                  {isLoading ? "Disabling..." : "Disable 2FA"}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowDisableModal(false);
                    setDisablePassword("");
                    setDisableCode("");
                    setError(null);
                  }}
                  className="px-6 py-3 bg-gray-500 text-white font-medium rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </ActivityLayout>
  );
}
