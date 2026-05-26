"use client";

import React from "react";

/**
 * Premium Card with cinematic glassmorphism.
 */
export default function Card({
  children,
  variant = "default",
  className = "",
  onClick,
  ...props
}) {
  const base = "rounded-2xl border transition-all duration-300 overflow-hidden";

  const variants = {
    default:
      "glass-card",
    elevated:
      "glass-strong shadow-2xl shadow-indigo-950/10",
    interactive:
      "glass-card hover:-translate-y-0.5 cursor-pointer",
    outline:
      "bg-transparent border-zinc-800/80 text-zinc-200",
  };

  return (
    <div
      onClick={onClick}
      className={`${base} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
