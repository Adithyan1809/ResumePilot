"use client";

import { createContext, useContext, useState, useEffect, useCallback } from "react";
import api from "@/lib/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const savedToken = localStorage.getItem("resumeai_token");
    if (savedToken) {
      setToken(savedToken);
      api.setToken(savedToken);
      fetchUser(savedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async (authToken) => {
    try {
      const data = await api.get("/auth/me", authToken);
      setUser(data);
    } catch (err) {
      console.error("Failed to fetch user:", err);
      localStorage.removeItem("resumeai_token");
      setToken(null);
      api.setToken(null);
    } finally {
      setLoading(false);
    }
  };

  const login = useCallback(async (email, password) => {
    setError(null);
    try {
      const data = await api.post("/auth/login", { email, password });
      const accessToken = data.access_token;
      setToken(accessToken);
      localStorage.setItem("resumeai_token", accessToken);
      api.setToken(accessToken);
      await fetchUser(accessToken);
      return { success: true };
    } catch (err) {
      const message = err.message || "Login failed. Please try again.";
      setError(message);
      return { success: false, error: message };
    }
  }, []);

  const signup = useCallback(async (name, email, password) => {
    setError(null);
    try {
      await api.post("/auth/signup", { full_name: name, email, password });
      const loginResult = await login(email, password);
      return loginResult;
    } catch (err) {
      const message = err.message || "Signup failed. Please try again.";
      setError(message);
      return { success: false, error: message };
    }
  }, [login]);

  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    setError(null);
    localStorage.removeItem("resumeai_token");
    api.setToken(null);
  }, []);

  const clearError = useCallback(() => setError(null), []);

  const value = {
    user,
    token,
    loading,
    error,
    isAuthenticated: !!user && !!token,
    login,
    signup,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export default AuthContext;
