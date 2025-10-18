import api from "../../../shared/services/api";
import type {
  TwoFactorSetupResponse,
  TwoFactorStatusResponse,
  TwoFactorEnableResponse,
} from "../types/two_factor.types";

export class TwoFactorService {
  async getStatus(): Promise<TwoFactorStatusResponse> {
    try {
      const response = await api.get(
        "/fullstack_authentication/auth/2fa/status"
      );
      return response as unknown as TwoFactorStatusResponse;
    } catch (error: any) {
      console.error("Failed to fetch 2FA status:", error);
      throw new Error("Failed to fetch 2FA status");
    }
  }

  async setup(): Promise<TwoFactorSetupResponse> {
    try {
      const response = await api.post(
        "/fullstack_authentication/auth/2fa/setup"
      );
      return response as unknown as TwoFactorSetupResponse;
    } catch (error: any) {
      console.error("Failed to setup 2FA:", error);
      throw new Error("Failed to setup 2FA");
    }
  }

  async enable(token: string): Promise<TwoFactorEnableResponse> {
    try {
      const response = await api.post(
        "/fullstack_authentication/auth/2fa/enable",
        { token }
      );
      return response as unknown as TwoFactorEnableResponse;
    } catch (error: any) {
      console.error("Failed to enable 2FA:", error);
      if (error.response?.status === 400) {
        throw new Error("Invalid verification code. Please try again.");
      }
      throw new Error("Failed to enable 2FA");
    }
  }

  async disable(password: string, token: string): Promise<any> {
    try {
      const response = await api.post(
        "/fullstack_authentication/auth/2fa/disable",
        { password, token }
      );
      return response as unknown as any;
    } catch (error: any) {
      console.error("Failed to disable 2FA:", error);
      if (error.response?.status === 400) {
        throw new Error("Invalid verification code");
      }
      if (error.response?.status === 401) {
        throw new Error("Invalid password");
      }
      throw new Error("Failed to disable 2FA");
    }
  }
}

export const twoFactorService = new TwoFactorService();
