import api from "../../../shared/services/api";
import { loginSchema, loginResponseSchema, type loginRequest, type loginResponse } from "../schemas/login.schema";
import { registerSchema, registrationResponseSchema, type registerRequest, type registrationResponse } from "../schemas/register.schema";
import { emailVerificationSchema, emailVerificationResponseSchema, type emailVerificationRequest, type emailVerificationResponse } from "../schemas/emailVerification.schema";
// import { authResponseSchema, type authResponse } from "../schemas/authResponse.schema";

export const authService = {
    async login(credentials: loginRequest): Promise<loginResponse> {
        const validated = loginSchema.parse(credentials);
        const response = await api.post('/fullstack_authentication/auth/login', validated)
        return loginResponseSchema.parse(response)
    },

    async register(data: registerRequest): Promise<registrationResponse> {
        const validated = registerSchema.parse(data)
        const response = await api.post('/fullstack_authentication/auth/register', validated)
        return registrationResponseSchema.parse(response)
    },

    async verifyEmail(verificationData: emailVerificationRequest ): Promise<emailVerificationResponse> {
        const validated = emailVerificationSchema.parse(verificationData)
        const response = await api.post('/fullstack_authentication/auth/verify-email', validated)
        return emailVerificationResponseSchema.parse(response)
    },

    async logout(){
        await api.post('/auth/logout')
    }
}
