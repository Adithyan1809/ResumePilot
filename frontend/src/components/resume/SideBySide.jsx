"use client";

import React, { useState } from "react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";

/**
 * Side-by-Side original vs. tailored resume view.
 */
export default function SideBySide({ original, tailored }) {
  const [activeTab, setActiveTab] = useState("experience"); // experience, summary, skills

  if (!original || !tailored) return null;

  return (
    <div className="flex flex-col gap-6 w-full">
      {/* Category Toggle Tabs */}
      <div className="flex bg-slate-950 p-1.5 rounded-2xl border border-slate-800/80 max-w-sm">
        {["summary", "experience", "skills"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`flex-1 py-2 text-xs font-semibold uppercase tracking-wider rounded-xl transition-all duration-200 ${
              activeTab === tab
                ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/10"
                : "text-slate-500 hover:text-slate-300"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Comparison Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Original */}
        <Card variant="outline" className="p-6 border-slate-850 flex flex-col gap-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h5 className="font-bold text-slate-200 text-sm">Original Resume</h5>
            <Badge variant="slate">Before</Badge>
          </div>
          <div className="max-h-[50vh] overflow-y-auto pr-2 custom-scrollbar">
            {activeTab === "summary" && (
              <p className="text-xs text-slate-400 leading-relaxed italic">
                {original.summary || "No summary provided in original resume."}
              </p>
            )}

            {activeTab === "experience" && (
              <div className="flex flex-col gap-6">
                {original.experience?.map((job, idx) => (
                  <div key={idx} className="flex flex-col gap-2">
                    <div className="flex flex-col">
                      <span className="font-bold text-slate-300 text-xs">{job.role}</span>
                      <span className="text-[10px] text-slate-500 font-semibold">{job.company}</span>
                    </div>
                    <ul className="list-disc pl-4 flex flex-col gap-1 text-[11px] text-slate-500">
                      {job.bullets?.map((b, bIdx) => (
                        <li key={bIdx}>{b}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}

            {activeTab === "skills" && (
              <div className="flex flex-wrap gap-1.5">
                {original.skills?.map((skill, idx) => (
                  <Badge key={idx} variant="slate" className="text-[10px] py-0.5">
                    {skill}
                  </Badge>
                ))}
              </div>
            )}
          </div>
        </Card>

        {/* Right Column: Tailored (Highlighted) */}
        <Card variant="elevated" className="p-6 border-indigo-950/40 bg-indigo-950/5 flex flex-col gap-4">
          <div className="flex items-center justify-between border-b border-indigo-900/20 pb-3">
            <h5 className="font-bold text-slate-100 text-sm">AI Tailored Resume</h5>
            <Badge variant="violet">Optimized</Badge>
          </div>
          <div className="max-h-[50vh] overflow-y-auto pr-2 custom-scrollbar">
            {activeTab === "summary" && (
              <p className="text-xs text-indigo-100 leading-relaxed bg-indigo-500/5 p-4 rounded-xl border border-indigo-500/10">
                {tailored.summary}
              </p>
            )}

            {activeTab === "experience" && (
              <div className="flex flex-col gap-6">
                {tailored.experience?.map((job, idx) => {
                  const origJob = original.experience?.[idx] || {};
                  return (
                    <div key={idx} className="flex flex-col gap-2 bg-indigo-950/10 border border-indigo-900/10 p-4 rounded-xl">
                      <div className="flex flex-col">
                        <span className="font-bold text-slate-200 text-xs">{job.role}</span>
                        <span className="text-[10px] text-indigo-400 font-semibold">{job.company}</span>
                      </div>
                      <ul className="list-disc pl-4 flex flex-col gap-1.5 text-[11px] text-slate-300">
                        {job.bullets?.map((b, bIdx) => {
                          const isNew = !origJob.bullets?.includes(b);
                          return (
                            <li
                              key={bIdx}
                              className={`transition-colors leading-relaxed ${
                                isNew
                                  ? "text-emerald-300 bg-emerald-500/10 px-1.5 py-0.5 rounded font-medium border border-emerald-500/10"
                                  : "text-slate-300"
                              }`}
                            >
                              {b}
                            </li>
                          );
                        })}
                      </ul>
                    </div>
                  );
                })}
              </div>
            )}

            {activeTab === "skills" && (
              <div className="flex flex-wrap gap-1.5">
                {tailored.skills?.map((skill, idx) => {
                  const isNew = !original.skills?.includes(skill);
                  return (
                    <Badge
                      key={idx}
                      variant={isNew ? "emerald" : "violet"}
                      className="text-[10px] py-0.5"
                    >
                      {skill}
                    </Badge>
                  );
                })}
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
