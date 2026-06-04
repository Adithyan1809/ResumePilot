"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import api from "@/lib/api";
import Spinner from "../../../components/ui/Spinner";

function GCard({ children, className = "" }) {
  return (
    <div className={`rounded-2xl border border-slate-800/60 bg-slate-900/60 backdrop-blur-sm shadow-xl ${className}`}>
      {children}
    </div>
  );
}

const CATEGORIES = ["Technical", "Behavioral", "System Design", "Resume-Specific"];

const CATEGORY_ICONS = {
  "Technical": "⚙️",
  "Behavioral": "🧠",
  "System Design": "🏗️",
  "Resume-Specific": "📄",
};

const SAMPLE_QUESTIONS = {
  Technical: [
    "Explain how you would design a rate-limiting system for a REST API.",
    "What is the difference between a process and a thread?",
    "How does database indexing work? When would you avoid indexes?",
    "Describe your experience with async programming and event loops.",
    "Explain CAP theorem and how it applies to distributed databases.",
  ],
  Behavioral: [
    "Describe a time you disagreed with a technical decision and how you handled it.",
    "Tell me about a project where you had to learn a new technology quickly.",
    "How do you prioritize tasks when working on multiple deadlines?",
    "Describe a situation where you had to debug a critical production issue.",
    "Tell me about a time you mentored someone or helped a teammate grow.",
  ],
  "System Design": [
    "Design a URL shortener like bit.ly at scale.",
    "How would you architect a real-time notification system?",
    "Design a distributed job queue that handles millions of tasks per day.",
    "How would you build a caching layer for a high-traffic API?",
    "Design a multi-tenant SaaS authentication system.",
  ],
  "Resume-Specific": [
    "Walk me through your most impactful project from your resume.",
    "You mentioned [Project X] — what was the biggest technical challenge?",
    "How did you measure the performance improvements you listed?",
    "What would you do differently on your most recent project?",
    "Your background shows [Skill Y] — describe a real scenario where you used it.",
  ],
};

const DIFFICULTY_COLORS = {
  Easy: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
  Medium: "text-amber-400 bg-amber-500/10 border-amber-500/20",
  Hard: "text-rose-400 bg-rose-500/10 border-rose-500/20",
};

function ReadinessRing({ score = 0 }) {
  const circ = 2 * Math.PI * 42;
  const fill = (score / 100) * circ;
  const color = score >= 80 ? "#10b981" : score >= 60 ? "#14b8a6" : score >= 40 ? "#f59e0b" : "#f43f5e";
  const label = score >= 80 ? "Interview Ready" : score >= 60 ? "Moderately Ready" : score >= 40 ? "Needs Preparation" : "Early Stage";
  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative w-36 h-36">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="42" fill="none" stroke="#1e293b" strokeWidth="8" />
          <circle cx="50" cy="50" r="42" fill="none" stroke={color} strokeWidth="8"
            strokeDasharray={circ} strokeDashoffset={circ - fill} strokeLinecap="round"
            style={{ transition: "stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1)" }} />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-black text-slate-100">{score}</span>
          <span className="text-xs text-slate-500 font-semibold">/ 100</span>
        </div>
      </div>
      <div className="text-center">
        <div className="text-sm font-bold text-slate-200">{label}</div>
        <div className="text-xs text-slate-500 mt-0.5">Interview Readiness Score</div>
      </div>
    </div>
  );
}

export default function InterviewPrepPage() {
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState("Technical");
  const [targetRole, setTargetRole] = useState("");
  const [targetCompany, setTargetCompany] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [questions, setQuestions] = useState(null);
  const [checkedQ, setCheckedQ] = useState({});
  const [notes, setNotes] = useState({});

  useEffect(() => {
    (async () => {
      try {
        const p = await api.get("/tailor/profile/master");
        setProfile(p);
        // Pre-fill from last session
        const lastRole = p?.profile_memory?.target_roles_history?.slice(-1)?.[0];
        if (lastRole) {
          setTargetRole(lastRole.role || "");
          setTargetCompany(lastRole.company || "");
        }
      } catch {}
      finally { setIsLoading(false); }
    })();
  }, []);

  const handleGenerate = async () => {
    setIsGenerating(true);
    // Simulate pipeline call — in production calls /tailor/quick-tailor and extracts interview_simulation
    await new Promise(r => setTimeout(r, 1500));
    const evidence = profile?.structured_evidence || {};
    const skills = Array.isArray(evidence.skills) ? evidence.skills : Object.values(evidence.skills || {}).flat();
    // Build role-personalized questions
    const techQ = [
      `Given your experience with ${skills[0] || "Python"}, how would you design a scalable ${skills[1] || "API"} service?`,
      `Explain how you've optimized ${skills[2] || "database"} queries in a production environment.`,
      `How would you implement caching in a ${(targetRole || "backend").split(" ")[0]} system using your current stack?`,
      `Describe your approach to error handling and observability in ${skills[0] || "Python"} applications.`,
      ...SAMPLE_QUESTIONS.Technical.slice(0, 3),
    ];
    setQuestions({
      Technical: techQ,
      Behavioral: SAMPLE_QUESTIONS.Behavioral,
      "System Design": SAMPLE_QUESTIONS["System Design"],
      "Resume-Specific": [
        `Walk me through your strongest project from your resume and what problem it solved.`,
        `You have experience with ${skills.slice(0,3).join(", ")} — describe a real-world scenario where all three were used together.`,
        ...SAMPLE_QUESTIONS["Resume-Specific"].slice(2),
      ],
    });
    setIsGenerating(false);
  };

  const toggleCheck = (qIdx) => setCheckedQ(p => ({ ...p, [qIdx]: !p[qIdx] }));
  const updateNote = (qIdx, val) => setNotes(p => ({ ...p, [qIdx]: val }));

  if (isLoading) return (
    <div className="flex h-[70vh] items-center justify-center flex-col gap-4">
      <Spinner size="lg" color="indigo" />
      <span className="text-xs text-slate-500 font-bold uppercase tracking-widest animate-pulse">Loading Interview Prep...</span>
    </div>
  );

  const evidence = profile?.structured_evidence || {};
  const skills = Array.isArray(evidence.skills) ? evidence.skills : Object.values(evidence.skills || {}).flat();
  const readiness = profile?.profile_memory?.average_ats_score ? Math.min(95, Math.round(profile.profile_memory.average_ats_score * 0.9)) : 0;
  const currentQuestions = questions ? questions[activeCategory] : SAMPLE_QUESTIONS[activeCategory];
  const checkedCount = Object.values(checkedQ).filter(Boolean).length;
  const totalQ = Object.values(questions || SAMPLE_QUESTIONS).flat().length;

  return (
    <div className="flex flex-col gap-7 w-full pb-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-100 tracking-tight">Interview Simulator</h1>
          <p className="text-sm text-slate-500 mt-0.5">AI-generated questions calibrated to your evidence, role & target company</p>
        </div>
        <Link href="/tailor">
          <button className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-bold shadow-lg hover:scale-105 transition-all">
            ⚡ Tailor Resume First
          </button>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Setup + Readiness */}
        <div className="flex flex-col gap-5">
          {/* Readiness Score */}
          <GCard className="p-6 flex flex-col items-center gap-4">
            <ReadinessRing score={readiness} />
            {readiness === 0 && (
              <p className="text-xs text-slate-500 text-center">Tailor a resume first to get your personalized readiness score.</p>
            )}
            <div className="w-full flex flex-col gap-2">
              {[
                { label: "Technical Depth", value: Math.min(95, (skills.length / 20) * 100) },
                { label: "Project Evidence", value: Math.min(90, ((evidence.experience || []).length * 25)) },
                { label: "Role Alignment", value: readiness },
              ].map(s => (
                <div key={s.label} className="flex items-center gap-3">
                  <span className="text-xs text-slate-500 w-28 flex-shrink-0">{s.label}</span>
                  <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-700" style={{ width: `${s.value}%` }} />
                  </div>
                  <span className="text-xs font-bold text-indigo-400 w-8 text-right">{Math.round(s.value)}%</span>
                </div>
              ))}
            </div>
          </GCard>

          {/* Setup */}
          <GCard className="p-5 flex flex-col gap-4">
            <h3 className="text-sm font-bold text-slate-200">Configure Session</h3>
            <div className="flex flex-col gap-3">
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">Target Role</label>
                <input value={targetRole} onChange={e => setTargetRole(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  placeholder="e.g. Backend Engineer" />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">Target Company</label>
                <input value={targetCompany} onChange={e => setTargetCompany(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  placeholder="e.g. Google, Stripe..." />
              </div>
              <button onClick={handleGenerate} disabled={isGenerating}
                className="w-full py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-bold disabled:opacity-50 hover:scale-[1.02] transition-all shadow-lg shadow-indigo-500/20">
                {isGenerating ? (
                  <span className="flex items-center justify-center gap-2">
                    <div className="w-3.5 h-3.5 border border-white/30 border-t-white rounded-full animate-spin" /> Generating Questions...
                  </span>
                ) : "🧠 Generate AI Questions"}
              </button>
            </div>
          </GCard>

          {/* Progress */}
          <GCard className="p-5 flex flex-col gap-3">
            <h3 className="text-sm font-bold text-slate-200">Practice Progress</h3>
            <div className="flex items-center gap-3">
              <div className="flex-1 bg-slate-800 rounded-full h-3 overflow-hidden">
                <div className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-500"
                  style={{ width: `${totalQ > 0 ? (checkedCount / totalQ) * 100 : 0}%` }} />
              </div>
              <span className="text-sm font-bold text-emerald-400 flex-shrink-0">{checkedCount}/{totalQ}</span>
            </div>
            <p className="text-xs text-slate-500">Check questions as you practice them</p>
          </GCard>
        </div>

        {/* Right: Questions */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          {/* Category Tabs */}
          <div className="flex flex-wrap gap-2">
            {CATEGORIES.map(cat => (
              <button key={cat} onClick={() => setActiveCategory(cat)}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-xl border text-xs font-bold transition-all ${
                  activeCategory === cat ? "bg-indigo-500/15 border-indigo-500/30 text-indigo-400" : "border-slate-700 text-slate-500 hover:border-slate-600 hover:text-slate-400"
                }`}>
                {CATEGORY_ICONS[cat]} {cat}
              </button>
            ))}
          </div>

          {/* Questions List */}
          <GCard className="flex flex-col">
            <div className="p-4 border-b border-slate-700/40 flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-200">{CATEGORY_ICONS[activeCategory]} {activeCategory} Questions</h3>
              {questions && <span className="text-xs text-emerald-400 font-bold bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">✓ AI Generated</span>}
            </div>
            <div className="flex flex-col divide-y divide-slate-700/30 max-h-[600px] overflow-y-auto custom-scrollbar">
              {currentQuestions.map((q, i) => {
                const key = `${activeCategory}-${i}`;
                const isChecked = checkedQ[key];
                return (
                  <div key={key} className={`p-5 transition-colors ${isChecked ? "bg-emerald-500/3" : "hover:bg-slate-800/20"}`}>
                    <div className="flex items-start gap-3">
                      <button onClick={() => toggleCheck(key)}
                        className={`w-5 h-5 rounded border-2 flex-shrink-0 mt-0.5 flex items-center justify-center transition-all ${
                          isChecked ? "bg-emerald-500 border-emerald-500" : "border-slate-600 hover:border-indigo-400"
                        }`}>
                        {isChecked && <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" /></svg>}
                      </button>
                      <div className="flex-1">
                        <p className={`text-sm leading-relaxed ${isChecked ? "text-slate-500 line-through" : "text-slate-200"}`}>
                          <span className="font-bold text-indigo-400 mr-1.5">Q{i + 1}.</span>{q}
                        </p>
                        {isChecked && (
                          <textarea
                            value={notes[key] || ""}
                            onChange={e => updateNote(key, e.target.value)}
                            placeholder="Add your answer notes here..."
                            rows={2}
                            className="mt-2 w-full px-3 py-2 rounded-lg bg-slate-800/60 border border-slate-700/60 text-slate-400 text-xs focus:outline-none focus:border-indigo-500 resize-none"
                          />
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </GCard>

          {/* Key Skills to Highlight */}
          {skills.length > 0 && (
            <GCard className="p-5">
              <h3 className="text-sm font-bold text-slate-200 mb-3">💡 Key Evidence to Highlight in Interviews</h3>
              <div className="flex flex-wrap gap-2">
                {skills.slice(0, 16).map((s, i) => (
                  <span key={i} className="px-3 py-1.5 rounded-xl bg-indigo-500/10 text-indigo-300 text-xs font-semibold border border-indigo-500/20">
                    {s}
                  </span>
                ))}
              </div>
            </GCard>
          )}
        </div>
      </div>
    </div>
  );
}
