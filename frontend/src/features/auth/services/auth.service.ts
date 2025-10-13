import api from "../../../shared/services/api";
import { loginSchema, type loginRequest } from "../schemas/login.schema";
import { registerSchema, type registerRequest } from "../schemas/register.schema";
import { authResponseSchema, type authResponse } from "../schemas/authResponse.schema";

export const authService = {
    async login(credentials: loginRequest): Promise<authResponse> {
        const validated = loginSchema.parse(credentials);
        const response = await api.post('/fullstack_authentication/auth/login', validated)
        return authResponseSchema.parse(response)
    },

    async register(data: registerRequest): Promise<authResponse> {
        const validated = registerSchema.parse(data)
        const response = await api.post('/fullstack_authentication/auth/register', validated)
        return authResponseSchema.parse(response)
    },

    async logout(){
        await api.post('/auth/logout')
    }
}
