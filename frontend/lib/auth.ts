"use client";

import api from "./apiClient";

export async function login(email: string, password: string): Promise<void> {
  const res = await api.post("/auth/login", { email, password });
  if (typeof window !== "undefined") {
    localStorage.setItem("crr_token", res.data.access_token);
  }
}

export async function register(email: string, password: string): Promise<void> {
  await api.post("/auth/register", { email, password });
}

