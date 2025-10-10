import { z } from "zod";

export const userSchema = z.object({
  id: z.number(),
  username: z
    .string()
    .min(3, "Username must be at least 3 characters")
    .regex(/^[a-zA-Z0-9]+$/, "Username must be alphanumeric"),
  email: z.string().email(),
  full_name: z.string().optional(),
  is_active: z.boolean(),
  role: z.enum(["user", "admin", "moderator"]),
  created_at: z.string(),
  updated_at: z.string().optional(),
});

export type User = z.infer<typeof userSchema>


