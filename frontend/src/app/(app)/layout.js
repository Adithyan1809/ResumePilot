"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../contexts/AuthContext";
import Sidebar from "../../components/layout/Sidebar";
import Spinner from "../../components/ui/Spinner";

/**
 * App Shell layout for dashboard routes, handling auth guards.
 */
export default function AppShellLayout({ children }) {
  const router = useRouter();
  const { user, loading } = useAuth();
  const isInitialized = !loading;

  // Route guarding
  useEffect(() => {
    if (isInitialized && !user) {
      router.push("/login");
    }
  }, [user, isInitialized, router]);

  // Loading page block on initialization
  if (!isInitialized || !user) {
    return (
      <div className="min-h-screen bg-[#020617] flex items-center justify-center flex-col gap-4 text-center">
        <Spinner size="lg" color="indigo" />
        <span className="text-xs text-slate-500 font-bold uppercase tracking-widest animate-pulse">
          Validating Session...
        </span>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-[#020617] overflow-hidden">
      {/* Sidebar Panel */}
      <Sidebar />

      {/* Main Viewport Container */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        {/* Glow accents */}
        <div className="absolute top-0 right-0 w-[40rem] h-[40rem] rounded-full bg-indigo-500/5 blur-[120px] pointer-events-none" />
        <div className="absolute bottom-0 left-10 w-[30rem] h-[30rem] rounded-full bg-purple-500/3 blur-[100px] pointer-events-none" />

        {/* Scrollable Viewport Frame */}
        <div className="flex-1 overflow-y-auto p-6 md:p-8 relative z-10 custom-scrollbar">
          {children}
        </div>
      </main>
    </div>
  );
}
