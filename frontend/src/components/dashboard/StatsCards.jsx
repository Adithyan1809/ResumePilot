"use client";

import React from "react";
import Card from "../ui/Card";

/**
 * Dashboard stats counters panel.
 */
export default function StatsCards({ stats = {} }) {
  const cards = [
    {
      label: "Total Uploads",
      value: stats.totalResumes || 0,
      icon: (
        <svg className="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
      ),
      bgGlow: "shadow-indigo-500/5 border-indigo-950/20",
    },
    {
      label: "Tailored Versions",
      value: stats.totalTailored || 0,
      icon: (
        <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
      bgGlow: "shadow-purple-500/5 border-purple-950/20",
    },
    {
      label: "Average ATS Score",
      value: `${stats.avgScore || 0}%`,
      icon: (
        <svg className="w-5 h-5 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      bgGlow: "shadow-teal-500/5 border-teal-950/20",
    },
    {
      label: "Best Match",
      value: `${stats.bestScore || 0}%`,
      icon: (
        <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
        </svg>
      ),
      bgGlow: "shadow-amber-500/5 border-amber-950/20",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full">
      {cards.map((card, idx) => (
        <Card
          key={idx}
          className={`flex items-center justify-between p-6 ${card.bgGlow}`}
        >
          <div className="flex flex-col gap-1">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">
              {card.label}
            </span>
            <span className="text-3xl font-extrabold text-slate-100 mt-1 tracking-tight">
              {card.value}
            </span>
          </div>
          {/* Icon frame */}
          <div className="w-12 h-12 rounded-xl bg-slate-950/80 border border-slate-800/80 flex items-center justify-center shadow-inner">
            {card.icon}
          </div>
        </Card>
      ))}
    </div>
  );
}
