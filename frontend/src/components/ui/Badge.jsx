"use client";

import React from "react";

/**
 * Reusable Badge component for labels, tags, and status.
 */
export default function Badge({
  children,
  variant = "indigo", // indigo, slate, emerald, amber, rose, violet
  className = "",
  ...props
}) {
  const baseStyles =
    "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide transition-all duration-300";

  const variantStyles = {
    indigo: "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20",
    violet: "bg-violet-500/10 text-violet-400 border border-violet-500/20",
    slate: "bg-slate-800 text-slate-300 border border-slate-700",
    emerald: "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20",
    amber: "bg-amber-500/10 text-amber-400 border border-amber-500/20",
    rose: "bg-rose-500/10 text-rose-400 border border-rose-500/20",
  };

  return (
    <span
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}
