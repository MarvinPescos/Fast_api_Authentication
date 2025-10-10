import {z} from "zod"
import { userSchema } from "../../users/schemas/users.schema"

export const authResponseSchema = z.object({
    success: z.boolean(),
    message: z.string(),
    user: userSchema
})

export type AuthResponse = z.infer<typeof authResponseSchema>;

