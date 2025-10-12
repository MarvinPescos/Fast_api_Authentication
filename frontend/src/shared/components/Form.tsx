import React, { useState } from "react";

export function useForm<T extends Record<any, string>>(initialValue:T) {
    const[form, setForm] = useState<T>(initialValue);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target
        setForm((prev) => ({...prev, [name]: value}))
    };
    return {form, handleChange}
}