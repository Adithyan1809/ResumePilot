"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "../../contexts/AuthContext";
import Button from "../ui/Button";

/**
 * Global Navigation Header.
 */
export default function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  
  // Don't show in standard layout if inside the dashboard app shell
  const isAppShellRoute =
    pathname.startsWith("/dashboard") ||
    pathname.startsWith("/tailor") ||
    pathname.startsWith("/history");

  if (isAppShellRoute) return null;

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/40 bg-slate-950/70 backdrop-blur-md transition-all duration-300">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform duration-300">
            <svg
              className="w-5 h-5 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2.5"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <span className="font-extrabold text-xl bg-gradient-to-r from-slate-100 via-slate-200 to-slate-400 bg-clip-text text-transparent">
            Resume<span className="text-indigo-400 font-medium">AI</span>
          </span>
        </Link>

        {/* Links */}
        <nav className="hidden md:flex items-center gap-8">
          <Link
            href="#features"
            className="text-sm text-slate-400 hover:text-slate-200 font-medium transition-colors"
          >
            Features
          </Link>
          <Link
            href="#how-it-works"
            className="text-sm text-slate-400 hover:text-slate-200 font-medium transition-colors"
          >
            How it Works
          </Link>
          <Link
            href="#templates"
            className="text-sm text-slate-400 hover:text-slate-200 font-medium transition-colors"
          >
            Templates
          </Link>
        </nav>

        {/* Auth Actions */}
        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link href="/dashboard">
                <Button variant="secondary" size="sm">
                  Dashboard
                </Button>
              </Link>
              <Button onClick={logout} variant="outline" size="sm">
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link href="/login">
                <Button variant="ghost" size="sm">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button variant="gradient" size="sm">
                  Get Started
                </Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
