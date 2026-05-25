"use client";

import React from "react";
import Badge from "../ui/Badge";

/**
 * Renders structured suggestions and checklists for resume improvement.
 */
export default function SuggestionsList({ suggestions = [] }) {
  if (suggestions.length === 0) {
    return (
      <div className="p-6 bg-slate-900/10 border border-slate-800/80 rounded-3xl text-center">
        <p className="text-sm text-slate-400 font-semibold">
          🎉 Incredible! No formatting or structural issues detected. Your resume is in pristine shape.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3.5 w-full">
      {suggestions.map((sugg, idx) => {
        // Decide badge colors
        let priorityVariant = "rose";
        if (sugg.priority === "medium") {
          priorityVariant = "amber";
        } else if (sugg.priority === "low") {
          priorityVariant = "slate";
        }

        return (
          <div
            key={idx}
            className="flex items-start gap-4 p-4 rounded-2xl bg-slate-950/20 border border-slate-850 hover:border-slate-800 transition-all duration-300 shadow-inner"
          >
            {/* Warning indicator */}
            <div className={`mt-0.5 w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 ${
              sugg.priority === "high" ? "bg-rose-500/10 text-rose-400" :
              sugg.priority === "medium" ? "bg-amber-500/10 text-amber-400" :
              "bg-slate-800 text-slate-400"
            }`}>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>

            <div className="flex flex-col gap-1.5 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <Badge variant={priorityVariant}>
                  {sugg.priority} priority
                </Badge>
                <Badge variant="slate">
                  {sugg.category}
                </Badge>
              </div>
              <p className="text-xs md:text-sm text-slate-300 leading-relaxed font-medium">
                {sugg.suggestion}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
