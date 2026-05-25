"use client";

import React from "react";

/**
 * Reusable Card component with glassmorphism backdrop blur.
 */
export default function Card({
  children,
  variant = "default", // default, elevated, interactive, outline
  className = "",
  onClick,
  ...props
}) {
  const baseStyles =
    "rounded-2xl border transition-all duration-300 overflow-hidden";

  const variantStyles = {
    default:
      "bg-slate-900/60 backdrop-blur-md border-slate-800/80 text-slate-100 shadow-xl shadow-black/20",
    elevated:
      "bg-slate-850/80 backdrop-blur-lg border-slate-700/60 text-slate-100 shadow-2xl shadow-indigo-900/10",
    interactive:
      "bg-slate-900/60 backdrop-blur-md border-slate-800/80 text-slate-100 shadow-xl shadow-black/20 hover:border-slate-700 hover:shadow-2xl hover:shadow-indigo-500/5 hover:-translate-y-0.5 cursor-pointer",
    outline:
      "bg-transparent border-slate-800 text-slate-200",
  };

  return (
    <div
      onClick={onClick}
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
