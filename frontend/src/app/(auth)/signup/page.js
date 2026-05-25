"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../../../contexts/AuthContext";
import Card from "../../../components/ui/Card";
import Input from "../../../components/ui/Input";
import Button from "../../../components/ui/Button";

/**
 * Signup view.
 */
export default function SignupPage() {
  const router = useRouter();
  const { signup } = useAuth();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters long.");
      return;
    }

    setIsLoading(true);

    try {
      const { success, error } = await signup(fullName, email, password);
      if (success) {
        router.push("/dashboard");
      } else {
        setError(error || "Email is already registered. Try logging in.");
      }
    } catch (err) {
      setError("An unexpected error occurred during signup. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Quick strength indicator
  const passwordStrength = () => {
    if (!password) return 0;
    let strength = 0;
    if (password.length >= 8) strength += 25;
    if (/[A-Z]/.test(password)) strength += 25;
    if (/[0-9]/.test(password)) strength += 25;
    if (/[^A-Za-z0-9]/.test(password)) strength += 25;
    return strength;
  };

  const getStrengthLabel = (s) => {
    if (s >= 100) return { label: "Strong", color: "bg-emerald-500" };
    if (s >= 50) return { label: "Moderate", color: "bg-amber-500" };
    return { label: "Weak", color: "bg-rose-500" };
  };

  const strength = passwordStrength();
  const strengthInfo = getStrengthLabel(strength);

  return (
    <Card className="p-8 border-slate-800 bg-slate-900/60 shadow-2xl">
      <div className="flex flex-col gap-2 mb-8 text-center">
        <h2 className="text-2xl font-black text-slate-100 tracking-tight">Create Account</h2>
        <p className="text-sm text-slate-500 font-medium font-medium">
          Get started on your resume optimization journey
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <Input
          label="Full Name"
          type="text"
          placeholder="e.g. John Doe"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          required
          icon={
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          }
        />

        <Input
          label="Email Address"
          type="email"
          placeholder="e.g. name@domain.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          icon={
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.206" />
            </svg>
          }
        />

        <Input
          label="Password"
          type="password"
          placeholder="Min. 8 characters"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          icon={
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          }
        />

        {password && (
          <div className="flex flex-col gap-1.5 w-full -mt-2.5 px-1">
            <div className="flex justify-between items-center text-[10px] font-bold text-slate-500 uppercase">
              <span>Strength</span>
              <span className={strengthInfo.color.replace("bg-", "text-")}>
                {strengthInfo.label}
              </span>
            </div>
            <div className="w-full h-1 bg-slate-950 rounded-full overflow-hidden">
              <div
                className={`h-full ${strengthInfo.color} transition-all duration-300`}
                style={{ width: `${strength}%` }}
              />
            </div>
          </div>
        )}

        <Input
          label="Confirm Password"
          type="password"
          placeholder="Re-enter password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          icon={
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          }
        />

        {error && (
          <div className="p-3.5 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-xl text-xs font-semibold leading-relaxed">
            {error}
          </div>
        )}

        <Button
          type="submit"
          variant="gradient"
          className="w-full mt-2"
          isLoading={isLoading}
        >
          Register
        </Button>
      </form>

      <div className="mt-8 text-center text-xs text-slate-500 font-semibold">
        Already have an account?{" "}
        <Link href="/login" className="text-indigo-400 hover:text-indigo-300 hover:underline">
          Sign in instead
        </Link>
      </div>
    </Card>
  );
}
