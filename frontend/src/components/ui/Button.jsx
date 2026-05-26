"use client";

import React from "react";
import Spinner from "./Spinner";

/**
 * Premium Button with cinematic interaction states.
 */
export default function Button({
  children,
  onClick,
  type = "button",
  variant = "primary",
  size = "md",
  isLoading = false,
  disabled = false,
  className = "",
  icon = null,
  ...props
}) {
  const base =
    "inline-flex items-center justify-center font-medium rounded-xl transition-all duration-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090b] disabled:opacity-40 disabled:cursor-not-allowed active:scale-[0.98]";

  const sizes = {
    sm: "px-3.5 py-1.5 text-xs gap-1.5",
    md: "px-5 py-2.5 text-sm gap-2",
    lg: "px-7 py-3 text-sm gap-2.5 font-semibold",
  };

  const variants = {
    primary:
      "bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/20 hover:shadow-indigo-500/30 focus-visible:ring-indigo-500",
    secondary:
      "bg-zinc-800 hover:bg-zinc-700 text-zinc-100 border border-zinc-700/60 focus-visible:ring-zinc-500",
    outline:
      "bg-transparent hover:bg-zinc-800/60 text-zinc-300 border border-zinc-700/60 hover:border-zinc-600 focus-visible:ring-zinc-500",
    ghost:
      "bg-transparent hover:bg-zinc-800/50 text-zinc-400 hover:text-zinc-100 focus-visible:ring-zinc-500",
    danger:
      "bg-rose-600 hover:bg-rose-500 text-white shadow-lg shadow-rose-600/20 focus-visible:ring-rose-500",
    gradient:
      "btn-gradient text-white shadow-xl shadow-indigo-500/15 focus-visible:ring-purple-500",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || isLoading}
      className={`${base} ${sizes[size]} ${variants[variant]} ${className}`}
      {...props}
    >
      {isLoading && <Spinner size="sm" color="white" />}
      {!isLoading && icon && <span className="flex-shrink-0">{icon}</span>}
      <span>{children}</span>
    </button>
  );
}
