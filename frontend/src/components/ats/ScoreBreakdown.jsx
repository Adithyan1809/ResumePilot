"use client";

import React from "react";

/**
 * Granular ATS score breakdown bar charts.
 */
export default function ScoreBreakdown({ scores }) {
  if (!scores) return null;

  const dimensions = [
    { label: "Keyword Match", value: scores.keyword_match_score, color: "bg-indigo-500" },
    { label: "Skills Alignment", value: scores.skills_alignment_score, color: "bg-purple-500" },
    { label: "Semantic Similarity", value: scores.semantic_similarity_score, color: "bg-pink-500" },
    { label: "Action Verbs", value: scores.action_verb_score, color: "bg-blue-500" },
    { label: "Measurable Impact", value: scores.achievement_score, color: "bg-teal-500" },
    { label: "Formatting Quality", value: scores.formatting_score, color: "bg-emerald-500" },
    { label: "Section Completeness", value: scores.section_completeness_score, color: "bg-violet-500" },
  ];

  return (
    <div className="flex flex-col gap-4 w-full">
      {dimensions.map((dim, idx) => (
        <div key={idx} className="flex flex-col gap-1.5 w-full">
          <div className="flex justify-between items-center text-xs">
            <span className="font-semibold text-slate-300">{dim.label}</span>
            <span className="font-bold text-slate-400">{dim.value}%</span>
          </div>
          {/* Progress outer track */}
          <div className="w-full h-2.5 bg-slate-950 rounded-full border border-slate-900 overflow-hidden">
            {/* Progress fill */}
            <div
              className={`h-full ${dim.color} rounded-full transition-all duration-1000 ease-out`}
              style={{ width: `${dim.value}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
