"use client";

import React, { useState } from "react";
import Badge from "../ui/Badge";

/**
 * Keyword match / missing grid component.
 */
export default function KeywordGrid({ missingKeywords = [] }) {
  const [filter, setFilter] = useState("all"); // all, high, medium, low

  const filtered = missingKeywords.filter((kw) => {
    if (filter === "all") return true;
    return kw.importance === filter;
  });

  return (
    <div className="flex flex-col gap-5 w-full">
      {/* Filters */}
      <div className="flex items-center gap-2 border-b border-slate-800/80 pb-3">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider mr-2">
          Missing Keywords:
        </span>
        {["all", "high", "medium", "low"].map((priority) => (
          <button
            key={priority}
            onClick={() => setFilter(priority)}
            className={`px-3 py-1 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all duration-200 ${
              filter === priority
                ? "bg-indigo-600/20 text-indigo-400 border border-indigo-500/20"
                : "text-slate-500 hover:text-slate-300"
            }`}
          >
            {priority}
          </button>
        ))}
      </div>

      {/* Grid */}
      {filtered.length > 0 ? (
        <div className="flex flex-wrap gap-2.5">
          {filtered.map((item, idx) => {
            // Determine border glow based on importance level
            let importanceClass = "rose";
            if (item.importance === "medium") {
              importanceClass = "amber";
            } else if (item.importance === "low") {
              importanceClass = "slate";
            }
            return (
              <Badge
                key={idx}
                variant={importanceClass}
                className="py-1 px-3 shadow-md shadow-black/10 hover:scale-103 transition-transform"
              >
                <span className="flex items-center gap-1.5">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <span>{item.keyword}</span>
                  <span className="opacity-50 text-[10px] font-medium font-mono">({item.importance})</span>
                </span>
              </Badge>
            );
          })}
        </div>
      ) : (
        <div className="p-6 bg-slate-900/20 border border-slate-800 rounded-2xl text-center">
          <p className="text-sm text-slate-400 font-medium">
            🎉 Excellent! No missing keywords found in this filter range.
          </p>
        </div>
      )}
    </div>
  );
}
