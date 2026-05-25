"use client";

import React from "react";

/**
 * Reusable styled Input component with standard validation styling.
 */
export default function Input({
  label = "",
  type = "text",
  placeholder = "",
  value,
  onChange,
  error = "",
  disabled = false,
  required = false,
  className = "",
  name = "",
  icon = null,
  ...props
}) {
  return (
    <div className={`flex flex-col gap-2 w-full ${className}`}>
      {label && (
        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
          {label} {required && <span className="text-rose-500">*</span>}
        </label>
      )}
      <div className="relative flex items-center">
        {icon && (
          <div className="absolute left-4 text-slate-500 pointer-events-none">
            {icon}
          </div>
        )}
        <input
          type={type}
          name={name}
          value={value}
          onChange={onChange}
          disabled={disabled}
          placeholder={placeholder}
          required={required}
          className={`w-full px-4 ${icon ? "pl-11" : "pl-4"} py-3 bg-slate-950/50 border rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed ${
            error
              ? "border-rose-500 focus:ring-rose-500"
              : "border-slate-800 hover:border-slate-700 focus:ring-indigo-500"
          }`}
          {...props}
        />
      </div>
      {error && (
        <p className="text-xs text-rose-500 font-medium mt-0.5">{error}</p>
      )}
    </div>
  );
}
