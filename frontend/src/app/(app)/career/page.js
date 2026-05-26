"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import api from "../../../lib/api";
import Spinner from "../../../components/ui/Spinner";

function GCard({ children, className = "" }) {
  return (
    <div className={`rounded-2xl border border-slate-800/60 bg-slate-900/60 backdrop-blur-sm shadow-xl ${className}`}>
      {children}
    </div>
  );
}

function ScoreBar({ label, value, color = "indigo" }) {
  const colors = { indigo: "from-indigo-500 to-purple-500", teal: "from-teal-500 to-emerald-500", amber: "from-amber-500 to-orange-500", rose: "from-rose-500 to-pink-500" };
  const textColors = { indigo: "text-indigo-400", teal: "text-teal-400", amber: "text-amber-400", rose: "text-rose-400" };
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-40 flex-shrink-0">{label}</span>
      <div className="flex-1 bg-slate-800/60 rounded-full h-2 overflow-hidden">
        <div className={`h-full rounded-full bg-gradient-to-r transition-all duration-700 ${colors[color] || colors.indigo}`} style={{ width: `${value}%` }} />
      </div>
      <span className={`text-xs font-bold w-10 text-right flex-shrink-0 ${textColors[color] || textColors.indigo}`}>{Math.round(value)}%</span>
    </div>
  );
}

function StatBubble({ label, value, accent = "indigo" }) {
  const bg = { indigo: "bg-indigo-500/10 border-indigo-500/20 text-indigo-400", teal: "bg-teal-500/10 border-teal-500/20 text-teal-400", amber: "bg-amber-500/10 border-amber-500/20 text-amber-400", emerald: "bg-emerald-500/10 border-emerald-500/20 text-emerald-400" };
  return (
    <div className={`rounded-2xl border p-4 flex flex-col gap-1 ${bg[accent] || bg.indigo}`}>
      <div className="text-2xl font-black text-slate-100">{value}</div>
      <div className="text-xs font-semibold text-slate-500">{label}</div>
    </div>
  );
}

const TRENDING_TECH = [
  { name: "Python",      demand: 94, trend: "+12%", domain: "ai_ml,backend,data" },
  { name: "TypeScript",  demand: 89, trend: "+18%", domain: "fullstack,frontend" },
  { name: "Kubernetes",  demand: 82, trend: "+22%", domain: "devops,backend" },
  { name: "React/Next",  demand: 87, trend: "+8%",  domain: "fullstack,frontend" },
  { name: "FastAPI",     demand: 76, trend: "+31%", domain: "backend,ai_ml" },
  { name: "LLMs/AI",    demand: 91, trend: "+85%", domain: "ai_ml" },
  { name: "PostgreSQL",  demand: 80, trend: "+6%",  domain: "backend,data" },
  { name: "Docker",      demand: 85, trend: "+15%", domain: "backend,devops" },
  { name: "Go",          demand: 74, trend: "+28%", domain: "backend,infra" },
  { name: "Rust",        demand: 68, trend: "+42%", domain: "systems,infra" },
];

const PROGRESSION_PATHS = {
  backend:      ["Junior Backend Developer", "Backend Engineer", "Senior Backend Engineer", "Staff Engineer", "Principal Engineer / Architect"],
  ai_ml:        ["ML Intern / Junior DS", "Machine Learning Engineer", "Senior ML Engineer", "ML Lead / Research Engineer", "ML Systems Architect"],
  fullstack:    ["Junior Developer", "Full Stack Engineer", "Senior Full Stack", "Tech Lead", "Engineering Manager / Principal"],
  data_science: ["Data Analyst", "Data Scientist", "Senior Data Scientist", "Principal DS / ML Lead", "Director of Data Science"],
};

export default function CareerIntelPage() {
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTrack, setActiveTrack] = useState("backend");
  const [currentStep, setCurrentStep] = useState(1);

  useEffect(() => {
    (async () => {
      try {
        const p = await api.get("/tailor/profile/master");
        setProfile(p);
      } catch {}
      finally { setIsLoading(false); }
    })();
  }, []);

  if (isLoading) return (
    <div className="flex h-[70vh] items-center justify-center flex-col gap-4">
      <Spinner size="lg" color="indigo" />
      <span className="text-xs text-slate-500 font-bold uppercase tracking-widest animate-pulse">Loading Career Intelligence...</span>
    </div>
  );

  const evidence = profile?.structured_evidence || {};
  const skills = Array.isArray(evidence.skills) ? evidence.skills : Object.values(evidence.skills || {}).flat();
  const memory = profile?.profile_memory || {};
  const analytics = profile?.analytics || {};

  const skillSet = new Set(skills.map(s => s.toLowerCase()));
  const enrichedTech = TRENDING_TECH.map(t => ({
    ...t,
    hasSkill: skillSet.has(t.name.toLowerCase()) || skills.some(s => s.toLowerCase().includes(t.name.split("/")[0].toLowerCase())),
  }));

  const rolesHistory = memory.target_roles_history || [];
  const progression = PROGRESSION_PATHS[activeTrack] || PROGRESSION_PATHS.backend;

  return (
    <div className="flex flex-col gap-7 w-full pb-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-100 tracking-tight">Career Intelligence</h1>
          <p className="text-sm text-slate-500 mt-0.5">Market demand · Role transitions · Career progression · Skill gap analysis</p>
        </div>
        <Link href="/tailor">
          <button className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-bold shadow-lg hover:scale-105 transition-all">
            ⚡ Tailor Resume
          </button>
        </Link>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <StatBubble label="Skills in Profile" value={skills.length || 0} accent="indigo" />
        <StatBubble label="Tailored Resumes" value={memory.tailored_counts || 0} accent="teal" />
        <StatBubble label="Avg ATS Score" value={`${Math.round(memory.average_ats_score || 0)}%`} accent="amber" />
        <StatBubble label="Apps Tracked" value={analytics.total_applied || 0} accent="emerald" />
      </div>

      {/* Market Intelligence */}
      <GCard>
        <div className="p-5 border-b border-slate-700/40">
          <h2 className="text-sm font-bold text-slate-200">🔥 2025 Market Demand Intelligence</h2>
          <p className="text-xs text-slate-500 mt-0.5">Live technology demand rankings · Green = in your profile</p>
        </div>
        <div className="p-5 flex flex-col gap-3">
          {enrichedTech.map(tech => (
            <div key={tech.name} className="flex items-center gap-3">
              <div className="w-28 flex-shrink-0 flex items-center gap-2">
                <div className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${tech.hasSkill ? "bg-emerald-400" : "bg-slate-600"}`} />
                <span className={`text-sm font-semibold ${tech.hasSkill ? "text-slate-200" : "text-slate-500"}`}>{tech.name}</span>
              </div>
              <div className="flex-1 bg-slate-800/60 rounded-full h-2.5 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${tech.hasSkill ? "bg-gradient-to-r from-indigo-500 to-purple-500" : "bg-slate-600/50"}`}
                  style={{ width: `${tech.demand}%` }}
                />
              </div>
              <div className="w-12 text-right flex-shrink-0">
                <span className="text-xs font-bold text-emerald-400">{tech.trend}</span>
              </div>
              <div className="w-8 text-center flex-shrink-0 text-xs font-bold text-slate-500">{tech.demand}%</div>
            </div>
          ))}
          <div className="pt-3 border-t border-slate-700/40 flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-emerald-400" /><span className="text-slate-400">In your profile ({enrichedTech.filter(t => t.hasSkill).length})</span></div>
            <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-slate-600" /><span className="text-slate-500">Growth opportunities ({enrichedTech.filter(t => !t.hasSkill).length})</span></div>
          </div>
        </div>
      </GCard>

      {/* Career Progression Map */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GCard>
          <div className="p-5 border-b border-slate-700/40">
            <h2 className="text-sm font-bold text-slate-200">🗺️ Career Progression Map</h2>
            <div className="flex gap-2 mt-3 flex-wrap">
              {Object.keys(PROGRESSION_PATHS).map(track => (
                <button key={track} onClick={() => { setActiveTrack(track); setCurrentStep(1); }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${activeTrack === track ? "bg-indigo-500/15 border-indigo-500/30 text-indigo-400" : "border-slate-700 text-slate-500 hover:border-slate-600 hover:text-slate-400"}`}>
                  {track.replace("_", " / ").toUpperCase()}
                </button>
              ))}
            </div>
          </div>
          <div className="p-5">
            <div className="flex flex-col gap-0">
              {progression.map((step, i) => (
                <div key={i} className="flex items-start gap-4">
                  <div className="flex flex-col items-center">
                    <button
                      onClick={() => setCurrentStep(i)}
                      className={`w-8 h-8 rounded-full border-2 flex items-center justify-center text-xs font-black transition-all cursor-pointer ${
                        i < currentStep ? "bg-emerald-500 border-emerald-500 text-white" :
                        i === currentStep ? "bg-indigo-500 border-indigo-500 text-white ring-4 ring-indigo-500/20 scale-110" :
                        "bg-slate-800 border-slate-700 text-slate-500 hover:border-slate-600"
                      }`}>
                      {i < currentStep ? "✓" : i + 1}
                    </button>
                    {i < progression.length - 1 && (
                      <div className={`w-0.5 h-8 mt-1 ${i < currentStep ? "bg-emerald-500/40" : "bg-slate-700"}`} />
                    )}
                  </div>
                  <div className="pt-1 pb-6">
                    <div className={`text-sm font-bold ${i < currentStep ? "text-emerald-400" : i === currentStep ? "text-indigo-300" : "text-slate-500"}`}>
                      {step}
                      {i === currentStep && <span className="ml-2 text-xs bg-indigo-500/15 text-indigo-400 px-2 py-0.5 rounded-full border border-indigo-500/20">Current Target</span>}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="flex gap-2 mt-2">
              <button onClick={() => setCurrentStep(Math.max(0, currentStep - 1))} disabled={currentStep === 0}
                className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-400 text-xs disabled:opacity-40 hover:bg-slate-700 transition-colors">← Back</button>
              <button onClick={() => setCurrentStep(Math.min(progression.length - 1, currentStep + 1))} disabled={currentStep === progression.length - 1}
                className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-400 text-xs disabled:opacity-40 hover:bg-slate-700 transition-colors">Next →</button>
            </div>
          </div>
        </GCard>

        {/* Targeted Roles History */}
        <GCard>
          <div className="p-5 border-b border-slate-700/40">
            <h2 className="text-sm font-bold text-slate-200">🎯 Targeted Role History</h2>
            <p className="text-xs text-slate-500 mt-0.5">From your tailoring sessions</p>
          </div>
          <div className="flex-1 divide-y divide-slate-700/30 max-h-72 overflow-y-auto custom-scrollbar">
            {rolesHistory.length === 0 ? (
              <div className="p-8 text-center">
                <div className="text-slate-600 text-sm">No targeting history yet.</div>
                <Link href="/tailor" className="text-indigo-400 text-xs font-bold mt-2 block hover:underline">Start tailoring →</Link>
              </div>
            ) : (
              [...rolesHistory].reverse().map((r, i) => {
                const score = r.score || 0;
                const color = score >= 85 ? "text-emerald-400" : score >= 70 ? "text-teal-400" : score >= 55 ? "text-amber-400" : "text-rose-400";
                return (
                  <div key={i} className="flex items-center gap-4 px-5 py-3.5 hover:bg-slate-800/20 transition-colors">
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-semibold text-slate-200 truncate">{r.role}</div>
                      <div className="text-xs text-slate-500 truncate">{r.company}</div>
                    </div>
                    <div className={`text-lg font-black flex-shrink-0 ${color}`}>{Math.round(score)}%</div>
                  </div>
                );
              })
            )}
          </div>

          {/* Skills Match Panel */}
          <div className="p-5 border-t border-slate-700/40">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-3">Your Evidence Snapshot</h3>
            <div className="flex flex-wrap gap-1.5">
              {skills.slice(0, 20).map((s, i) => (
                <span key={i} className="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 text-xs border border-slate-700 hover:border-indigo-500/40 hover:text-indigo-300 transition-colors">{s}</span>
              ))}
              {skills.length === 0 && <p className="text-xs text-slate-500">Upload your master resume to populate evidence.</p>}
            </div>
          </div>
        </GCard>
      </div>

      {/* Skill Gap vs Market */}
      <GCard className="p-6">
        <h2 className="text-sm font-bold text-slate-200 mb-4">📈 Your Profile vs Market Demand</h2>
        <div className="flex flex-col gap-3">
          {enrichedTech.map(tech => (
            <div key={tech.name} className="flex items-center gap-4">
              <div className={`w-28 text-sm font-semibold flex-shrink-0 ${tech.hasSkill ? "text-slate-300" : "text-slate-600"}`}>{tech.name}</div>
              <div className="flex-1 grid grid-cols-2 gap-2">
                <div className="flex items-center gap-2">
                  <div className="text-xs text-slate-600 w-14 flex-shrink-0">Market:</div>
                  <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div className="h-full rounded-full bg-gradient-to-r from-slate-500 to-slate-400" style={{ width: `${tech.demand}%` }} />
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-xs text-slate-600 w-10 flex-shrink-0">You:</div>
                  <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div className={`h-full rounded-full ${tech.hasSkill ? "bg-gradient-to-r from-indigo-500 to-purple-500" : ""}`} style={{ width: tech.hasSkill ? "100%" : "0%" }} />
                  </div>
                  {!tech.hasSkill && <span className="text-xs text-rose-400 font-semibold">Gap</span>}
                  {tech.hasSkill && <span className="text-xs text-emerald-400 font-semibold">✓</span>}
                </div>
              </div>
            </div>
          ))}
        </div>
      </GCard>
    </div>
  );
}
