"use client";

import React from "react";
import Link from "next/link";

/**
 * Centered authentication routes shell layout.
 */
export default function AuthLayout({ children }) {
  return (
    <div className="min-h-screen bg-[#020617] flex flex-col justify-center items-center p-6 relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[35rem] h-[35rem] rounded-full bg-indigo-500/10 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 translate-x-1/2 translate-y-1/2 w-[35rem] h-[35rem] rounded-full bg-purple-500/10 blur-[100px] pointer-events-none" />

      {/* Brand logo link */}
      <Link href="/" className="flex items-center gap-2.5 mb-8 z-10 group">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform duration-300">
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <span className="font-extrabold text-xl bg-gradient-to-r from-slate-100 to-slate-400 bg-clip-text text-transparent">
          Resume<span className="text-indigo-400 font-medium">AI</span>
        </span>
      </Link>

      <div className="w-full max-w-md z-10">
        {children}
      </div>
    </div>
  );
}
