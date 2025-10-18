import api from "../../../shared/services/api";
import { ZodError } from "zod";
import {
  loginSchema,
  loginResponseSchema,
  type loginRequest,
  type loginResponse,
} from "../schemas/login.schema";
import {
  registerSchema,
  registrationResponseSchema,
  type registerRequest,
  type registrationResponse,
} from "../schemas/register.schema";
import {
  emailVerificationSchema,
  emailVerificationResponseSchema,
  resendVerificationSchema,
  type emailVerificationRequest,
  type emailVerificationResponse,
} from "../schemas/emailVerification.schema";

export const authService = {
  async login(credentials: loginRequest): Promise<loginResponse> {
    const validated = loginSchema.parse(credentials);
    const response = await api.post(
      "/fullstack_authentication/auth/login",
      validated
    );
    return loginResponseSchema.parse(response);
  },

  async register(data: registerRequest): Promise<registrationResponse> {
    const validated = registerSchema.parse(data);
    const response = await api.post(
      "/fullstack_authentication/auth/register",
      validated
    );
    const parsed = registrationResponseSchema.parse(response);
    return parsed;
  },

  async verifyEmail(
    verificationData: emailVerificationRequest
  ): Promise<emailVerificationResponse> {
    const validated = emailVerificationSchema.parse(verificationData);
    const response = await api.post(
      "/fullstack_authentication/auth/verify-email",
      validated
    );
    return emailVerificationResponseSchema.parse(response);
  },

  async resendVerification(userId: number): Promise<emailVerificationResponse> {
    try {
      const validated = resendVerificationSchema.parse({ user_id: userId });
      const response = await api.post(
        "/fullstack_authentication/auth/resend-verification",
        validated
      );
      return emailVerificationResponseSchema.parse(response);
    } catch (error) {
      if (error instanceof ZodError) {
        throw new Error(
          "Invalid request data: " +
            error.issues.map((e) => e.message).join(", ")
        );
      }
      throw error;
    }
  },

  async logout() {
    await api.post("/auth/logout");
  },

  async getFacebookLoginUrl(): Promise<{ authorization_url: string }> {
    return await api.get("/fullstack_authentication/auth/facebook/login");
  },

  async getGoogleLoginUrl(): Promise<{ authorization_url: string }> {
    return await api.get("/fullstack_authentication/auth/google/login");
  },

  async getCurrentUser(): Promise<any> {
    try {
      const response = await api.get("/fullstack_authentication/auth/me");
      return response;
    } catch (error) {
      throw error;
    }
  },

  async updateProfile(profileData: {
    username?: string;
    email?: string;
    full_name?: string;
    current_password?: string;
    new_password?: string;
  }): Promise<any> {
    try {
      const response = await api.put(
        "/fullstack_authentication/auth/profile",
        profileData
      );
      return response;
    } catch (error) {
      throw error;
    }
  },
};
