import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../../../shared/components/Button";
import { useForm } from "../../../shared/components/Form";

import { useAuth } from "../hooks/authHooks";
import { type registerRequest } from "../schemas/register.schema";

export function registerPage() {
    const navigate = useNavigate();
    const {register, isLoading, error, clearError}=  useAuth()
    const {form: userData, handleChange} = useForm<registerRequest>({
        username: "",
        email: "",
        password: "",
        fullname: "",
    });

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        try{
            const response = await register(userData);
            if (response.success && response.user.id){
                navigate("/mockBoard", {
                    state: {
                        userId: response.user.id,
                        email: userData.email
                    },
                });
            }
        } catch (error) {
            //Error already handled
        }
    };

    return (
        <form onSubmit={handleRegister}>
            {error && (
                <div className="bg-red-50 border-red-200 text-red-700 px-4 py-3 rounded">
                    {error}
                </div>
            )}
            <input 
                id="username"
                name="username"
                type="text"
                placeholder="username"
                value={userData.username}
                onChange={handleChange}
                onFocus={() => error && clearError()}
                required
            />
            <input 
                id="email"
                name="email"
                type="email"
                placeholder="email"
                value={userData.email}
                onChange={handleChange}
                onFocus={() => error && clearError()}
                required
            />
            <input 
                id="password"
                name="password"
                type="password"
                placeholder="password"
                value={userData.password}
                onChange={handleChange}
                onFocus={() => error && clearError()}
                required
            />
            <input 
                id="fullname"
                name="fullname"
                type="text"
                placeholder="fullname"
                value={userData.fullname}
                onChange={handleChange}
                onFocus={() => error && clearError()}
                required
            />
            <Button type="submit" isLoading={isLoading} className="w-full">
                Sign Up
            </Button>
        </form>
    )
}
