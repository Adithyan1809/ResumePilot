"use client";

import React, { useState, useEffect, useCallback } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";

// ── Micro Icon Factory ────────────────────────────────────────────────────────
const I = ({ d, size = "w-5 h-5", sw = 2 }) => (
  <svg className={size} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={sw} d={d} />
  </svg>
);
const Icons = {
  upload:    "M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12",
  brain:     "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
  link:      "M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1",
  zap:       "M13 10V3L4 14h7v7l9-11h-7z",
  check:     "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
  star:      "M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z",
  target:    "M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-4a6 6 0 100-12 6 6 0 000 12zm0-4a2 2 0 100-4 2 2 0 000 4z",
  book:      "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253",
  briefcase: "M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z",
  down:      "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4",
  chevDown:  "M19 9l-7 7-7-7",
  info:      "M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
  eye:       "M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z",
  map:       "M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7",
  users:     "M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z",
  back:      "M10 19l-7-7m0 0l7-7m-7 7h18",
  x:         "M6 18L18 6M6 6l12 12",
  refresh:   "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15",
};

function cn(...c) { return c.filter(Boolean).join(" "); }

function scoreColor(s) {
  if (s >= 85) return "text-emerald-400";
  if (s >= 70) return "text-teal-400";
  if (s >= 55) return "text-amber-400";
  return "text-rose-400";
}
function scoreBarColor(s) {
  if (s >= 85) return "from-emerald-500 to-emerald-400";
  if (s >= 70) return "from-teal-500 to-teal-400";
  if (s >= 55) return "from-amber-500 to-amber-400";
  return "from-rose-500 to-rose-400";
}
function scoreBg(s) {
  if (s >= 85) return "bg-emerald-500/10 border-emerald-500/20";
  if (s >= 70) return "bg-teal-500/10 border-teal-500/20";
  if (s >= 55) return "bg-amber-500/10 border-amber-500/20";
  return "bg-rose-500/10 border-rose-500/20";
}

// ── Circular Score Ring ───────────────────────────────────────────────────────
function ScoreRing({ score = 0, size = 100, label, sublabel }) {
  const r = (size - 16) / 2;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const col = score >= 85 ? "#10b981" : score >= 70 ? "#14b8a6" : score >= 55 ? "#f59e0b" : "#f43f5e";
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90 absolute inset-0">
          <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
          <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={col} strokeWidth="8"
            strokeDasharray={circ} strokeDashoffset={circ - fill} strokeLinecap="round"
            style={{ transition: "stroke-dashoffset 1s cubic-bezier(0.4,0,0.2,1)" }} />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn("font-black text-xl leading-none", scoreColor(score))}>{Math.round(score)}</span>
          <span className="text-xs text-slate-500 font-semibold">/ 100</span>
        </div>
      </div>
      {label && <div className="text-center">
        <div className="text-xs font-bold text-slate-300">{label}</div>
        {sublabel && <div className="text-xs text-slate-500 mt-0.5">{sublabel}</div>}
      </div>}
    </div>
  );
}

// ── Glass Card ────────────────────────────────────────────────────────────────
function GCard({ children, className = "" }) {
  return (
    <div className={cn("rounded-2xl border border-slate-800/60 bg-slate-900/60 backdrop-blur-sm shadow-xl", className)}>
      {children}
    </div>
  );
}

// ── Step Progress ─────────────────────────────────────────────────────────────
function StepProgress({ current, total = 5, hasProfile }) {
  const labels = hasProfile
    ? ["Profile Ready", "Job Target", "AI Audit", "Review", "Export"]
    : ["Upload Resume", "Job Target", "AI Audit", "Review", "Export"];
  return (
    <div className="flex items-center gap-0">
      {Array.from({ length: total }, (_, i) => i + 1).map((s, i) => (
        <React.Fragment key={s}>
          <div className="flex flex-col items-center gap-1.5">
            <div className={cn(
              "w-8 h-8 rounded-full flex items-center justify-center text-xs font-black border-2 transition-all duration-300",
              s < current ? "bg-emerald-500 border-emerald-500 text-white" :
              s === current ? "bg-indigo-500 border-indigo-500 text-white ring-4 ring-indigo-500/20" :
              "bg-slate-800 border-slate-700 text-slate-500"
            )}>
              {s < current ? "✓" : s}
            </div>
            <span className={cn("text-xs font-semibold hidden sm:block whitespace-nowrap", s === current ? "text-indigo-400" : s < current ? "text-emerald-400" : "text-slate-600")}>
              {labels[i]}
            </span>
          </div>
          {i < total - 1 && (
            <div className={cn("h-0.5 w-8 sm:w-16 flex-shrink-0 mb-5 transition-all duration-500", s < current ? "bg-emerald-500" : "bg-slate-700")} />
          )}
        </React.Fragment>
      ))}
    </div>
  );
}

// ── Score Bar ─────────────────────────────────────────────────────────────────
function ScoreBar({ label, value }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-36 flex-shrink-0">{label}</span>
      <div className="flex-1 bg-slate-800/60 rounded-full h-2 overflow-hidden">
        <div className={cn("h-full rounded-full bg-gradient-to-r transition-all duration-700", scoreBarColor(value))} style={{ width: `${value}%` }} />
      </div>
      <span className={cn("text-xs font-bold w-10 text-right flex-shrink-0", scoreColor(value))}>{Math.round(value)}%</span>
    </div>
  );
}

// ── Resume Preview ────────────────────────────────────────────────────────────
function MiniResumePreview({ sections }) {
  if (!sections) return null;
  const ci = sections.contact_info || {};
  const exp = sections.experience || [];
  const skills = sections.skills;
  const skillsList = Array.isArray(skills) ? skills : Object.values(skills || {}).flat();

  return (
    <div className="bg-white text-gray-900 rounded-xl p-6 shadow-2xl text-xs leading-normal font-serif min-h-[500px]" style={{ fontFamily: "'Times New Roman', serif" }}>
      {/* Header */}
      <div className="text-center border-b-2 border-gray-800 pb-3 mb-3">
        <div className="text-lg font-bold uppercase tracking-widest">{ci.name || "Candidate Name"}</div>
        <div className="text-xs text-gray-600 mt-1">
          {[ci.email, ci.phone, ci.location].filter(Boolean).join(" · ")}
        </div>
        {ci.linkedin && <div className="text-xs text-blue-600">{ci.linkedin}</div>}
      </div>
      {/* Summary */}
      {sections.summary && (
        <div className="mb-3">
          <div className="text-xs font-bold uppercase tracking-widest text-gray-700 border-b border-gray-300 mb-1 pb-0.5">Professional Summary</div>
          <p className="text-xs leading-relaxed">{sections.summary}</p>
        </div>
      )}
      {/* Experience */}
      {exp.length > 0 && (
        <div className="mb-3">
          <div className="text-xs font-bold uppercase tracking-widest text-gray-700 border-b border-gray-300 mb-1 pb-0.5">Experience</div>
          {exp.map((e, i) => (
            <div key={i} className="mb-2">
              <div className="flex justify-between">
                <span className="font-bold text-xs">{e.role || e.title}</span>
                <span className="text-xs text-gray-500">{e.dates || e.duration}</span>
              </div>
              <div className="text-xs text-gray-600 italic mb-0.5">{e.company}</div>
              {(e.bullets || []).slice(0, 2).map((b, j) => (
                <div key={j} className="text-xs ml-2">• {typeof b === "string" ? b : b?.text || ""}</div>
              ))}
            </div>
          ))}
        </div>
      )}
      {/* Skills */}
      {skillsList.length > 0 && (
        <div className="mb-3">
          <div className="text-xs font-bold uppercase tracking-widest text-gray-700 border-b border-gray-300 mb-1 pb-0.5">Skills</div>
          <div className="text-xs">{skillsList.slice(0, 20).join(" · ")}</div>
        </div>
      )}
      {/* Education */}
      {(sections.education || []).map((e, i) => (
        <div key={i} className="mb-1 text-xs">
          <span className="font-bold">{e.degree}</span> — {e.school}
          {e.dates && <span className="text-gray-500"> ({e.dates})</span>}
        </div>
      ))}
    </div>
  );
}

// ── Severity Badge ────────────────────────────────────────────────────────────
function SeverityBadge({ level }) {
  const cfg = {
    high:   "bg-rose-500/15 text-rose-400 border-rose-500/25",
    medium: "bg-amber-500/15 text-amber-400 border-amber-500/25",
    low:    "bg-slate-700 text-slate-400 border-slate-600",
  };
  return <span className={cn("text-xs font-bold px-2 py-0.5 rounded-full border uppercase tracking-wider", cfg[level] || cfg.low)}>{level}</span>;
}

// ── Template Picker ───────────────────────────────────────────────────────────
const TEMPLATES = [
  { id: "classic",    name: "Classic",    badge: "Enterprise",  desc: "Traditional serif — ideal for Finance, Banking, Corporate." },
  { id: "modern",     name: "Modern",     badge: "Startup",     desc: "Sleek sans-serif — perfect for Tech, SaaS, Growth." },
  { id: "executive",  name: "Executive",  badge: "Leadership",  desc: "Bold accents — optimal for Senior, Lead, Principal." },
];

const TRACKS = [
  { id: "backend",      label: "Backend",      icon: "⚙️" },
  { id: "ai_ml",        label: "AI / ML",      icon: "🧠" },
  { id: "fullstack",    label: "Full Stack",    icon: "🌐" },
  { id: "data_science", label: "Data Science",  icon: "📊" },
];

// ══════════════════════════════════════════════════════════════════════════════
// MAIN PAGE
// ══════════════════════════════════════════════════════════════════════════════
export default function TailorWizardPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const preloadedId = searchParams.get("id");

  // ── Wizard State ──────────────────────────────────────────────────────────
  const [step, setStep] = useState(1);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingMsg, setProcessingMsg] = useState("Processing...");
  const [error, setError] = useState(null);

  // ── Profile State ─────────────────────────────────────────────────────────
  const [masterProfile, setMasterProfile] = useState(null);
  const [hasProfile, setHasProfile] = useState(false);
  const [isLoadingProfile, setIsLoadingProfile] = useState(true);

  // ── Upload State (no-profile path) ────────────────────────────────────────
  const [resumeId, setResumeId] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);

  // ── Job Input State ───────────────────────────────────────────────────────
  const [jobUrl, setJobUrl] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [company, setCompany] = useState("");
  const [template, setTemplate] = useState("classic");
  const [strategyTrack, setStrategyTrack] = useState("backend");
  const [githubUrl, setGithubUrl] = useState("");
  const [inputMode, setInputMode] = useState("url"); // "url" | "text"

  // ── Output State ─────────────────────────────────────────────────────────
  const [result, setResult] = useState(null);           // full pipeline result
  const [coverLetter, setCoverLetter] = useState("");
  const [isGeneratingCL, setIsGeneratingCL] = useState(false);
  const [isHeatmapActive, setIsHeatmapActive] = useState(false);
  const [expandedSections, setExpandedSections] = useState({});

  // ── Load master profile on mount ─────────────────────────────────────────
  useEffect(() => {
    (async () => {
      try {
        const p = await api.get("/tailor/profile/master");
        setMasterProfile(p);
        setHasProfile(!!p?.has_profile);
        // Pre-fill github from evidence
        const gh = p?.structured_evidence?.contact_info?.github;
        if (gh) setGithubUrl(gh);
      } catch { /* ignore */ }
      finally { setIsLoadingProfile(false); }
    })();
  }, []);

  // ── Pre-load existing tailoring session ──────────────────────────────────
  useEffect(() => {
    if (preloadedId && !isLoadingProfile) {
      (async () => {
        setIsProcessing(true);
        try {
          const res = await api.get(`/tailor/${preloadedId}`);
          setResult({
            job_title: res.job_title, company: res.company,
            tailored_sections: res.tailored_sections,
            ats_score: res.ats_score,
            missing_keywords: res.missing_keywords,
            suggestions: res.suggestions,
          });
          setJobTitle(res.job_title || "");
          setCompany(res.company || "");
          setTemplate(res.template || "classic");
          setStep(5);
        } catch { setStep(hasProfile ? 2 : 1); }
        finally { setIsProcessing(false); }
      })();
    }
  }, [preloadedId, isLoadingProfile, hasProfile]);

  // ── STEP 1: File Upload (no-profile path) ────────────────────────────────
  const handleFileDrop = useCallback(async (file) => {
    if (!file) return;
    setUploadedFile(file);
    setIsProcessing(true);
    setProcessingMsg("Parsing resume & building evidence profile...");
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await api.postForm("/resumes/upload", fd);
      setResumeId(res.id);
      // Reload profile after upload
      const p = await api.get("/tailor/profile/master");
      setMasterProfile(p);
      setHasProfile(!!p?.has_profile);
      setStep(2);
    } catch (err) {
      setError("Upload failed: " + (err.message || "Please check your API key."));
    } finally { setIsProcessing(false); }
  }, []);

  // ── STEP 2: Run the full pipeline ────────────────────────────────────────
  const handleRunPipeline = useCallback(async () => {
    const hasJobInput = jobUrl.trim() || jobDescription.trim().length >= 50;
    if (!hasJobInput) {
      setError("Please provide a job URL or paste a job description (min 50 characters).");
      return;
    }
    setError(null);
    setIsProcessing(true);

    const steps = [
      "Scraping job intelligence...",
      "Loading your evidence profile...",
      "Mapping transferable skills...",
      "Running ATS simulation...",
      "Simulating recruiter scan...",
      "Generating tailored resume...",
      "Computing employability score...",
      "Finalizing output...",
    ];
    let idx = 0;
    setProcessingMsg(steps[0]);
    const ticker = setInterval(() => {
      idx = Math.min(idx + 1, steps.length - 1);
      setProcessingMsg(steps[idx]);
    }, 1800);

    try {
      const token = localStorage.getItem("resumeai_token");
      if (hasProfile) {
        // Use the full intelligence pipeline
        const res = await api.post("/tailor/quick-tailor", {
          job_url: jobUrl.trim(),
          job_description: jobDescription.trim(),
          job_title: jobTitle.trim(),
          company: company.trim(),
          template,
          github_url: githubUrl.trim(),
          strategy_track: strategyTrack,
        }, token);
        setResult(res);
        if (res.job_title) setJobTitle(res.job_title);
        if (res.company) setCompany(res.company);
      } else {
        // Fallback: standard analyze endpoint with uploaded resume
        const res = await api.post("/tailor/analyze", {
          resume_id: resumeId,
          job_description: jobDescription.trim(),
          job_title: jobTitle.trim(),
          company: company.trim(),
          template,
        }, token);
        setResult(res);
      }
      setStep(3);
    } catch (err) {
      setError(err.message || "Pipeline failed. Please check your configuration.");
    } finally {
      clearInterval(ticker);
      setIsProcessing(false);
    }
  }, [jobUrl, jobDescription, jobTitle, company, template, githubUrl, strategyTrack, hasProfile, resumeId]);

  // ── Cover Letter ──────────────────────────────────────────────────────────
  const handleGenerateCoverLetter = useCallback(async () => {
    if (!result) return;
    setIsGeneratingCL(true);
    try {
      const res = await api.post("/tailor/cover-letter", {
        tailored_resume_id: result.id || "00000000-0000-0000-0000-000000000000",
        tone: "professional",
      });
      setCoverLetter(res.cover_letter);
    } catch {
      setCoverLetter(`Dear Hiring Team,\n\nI am excited to apply for the ${jobTitle} position at ${company}. My background in ${(result?.tailored_sections?.skills && Object.values(result.tailored_sections.skills || {}).flat().slice(0,3).join(", ")) || "software engineering"} aligns strongly with your requirements.\n\nI look forward to contributing to your team's success.\n\nSincerely,\n${result?.tailored_sections?.contact_info?.name || "Candidate"}`);
    }
    setIsGeneratingCL(false);
  }, [result, jobTitle, company]);

  // ── Download ──────────────────────────────────────────────────────────────
  const handleDownload = useCallback(async (format) => {
    const tailoredId = result?.id || "00000000-0000-0000-0000-000000000000";
    const token = localStorage.getItem("resumeai_token");
    try {
      const resp = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1"}/tailor/download`,
        { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
          body: JSON.stringify({ tailored_resume_id: tailoredId, format, template }) }
      );
      if (!resp.ok) {
        let msg = "Download failed";
        try { const d = await resp.json(); msg = d.detail?.failures?.join(", ") || d.detail || msg; } catch {}
        throw new Error(msg);
      }
      const buf = await resp.arrayBuffer();
      const blob = new Blob([buf], { type: format === "pdf" ? "application/pdf" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url; a.download = `ResumePilot_${(jobTitle || "Resume").replace(/\s+/g, "_")}.${format}`;
      document.body.appendChild(a); a.click(); URL.revokeObjectURL(url); a.remove();
    } catch (err) {
      setError(`Export failed: ${err.message}`);
    }
  }, [result, template, jobTitle]);

  // ── Helpers ───────────────────────────────────────────────────────────────
  const toggleSection = (key) => setExpandedSections(p => ({ ...p, [key]: !p[key] }));

  const ats = result?.ats_score || {};
  const empScore = result?.employability_index?.employability_score || ats.overall_score || 0;
  const recruiterScore = result?.interview_readiness?.interview_readiness_score || 82;
  const gapReport = result?.missing_keywords || [];
  const roadmap = result?.learning_roadmap || {};
  const interviewQ = result?.interview_simulation || {};
  const branding = result?.branding_profiles || {};
  const explainability = result?.explainability_rationales || [];
  const companyIntel = result?.company_intelligence || {};

  // ── Loading ───────────────────────────────────────────────────────────────
  if (isLoadingProfile) return (
    <div className="flex h-[70vh] items-center justify-center flex-col gap-4">
      <div className="w-10 h-10 rounded-full border-2 border-indigo-500/30 border-t-indigo-500 animate-spin" />
      <span className="text-xs text-slate-500 font-bold uppercase tracking-widest animate-pulse">Loading Profile...</span>
    </div>
  );

  // ── Processing overlay ────────────────────────────────────────────────────
  const ProcessingOverlay = () => (
    <div className="flex flex-col items-center justify-center h-[55vh] gap-8">
      <div className="relative">
        <div className="w-20 h-20 rounded-full border-2 border-slate-700 flex items-center justify-center">
          <div className="w-12 h-12 rounded-full border-2 border-indigo-500/40 border-t-indigo-500 animate-spin" />
        </div>
        <div className="absolute -inset-4 rounded-full bg-indigo-500/5 animate-pulse" />
      </div>
      <div className="flex flex-col items-center gap-2">
        <p className="text-indigo-400 font-bold text-sm animate-pulse">{processingMsg}</p>
        <p className="text-xs text-slate-600">AI Employability Pipeline Running</p>
      </div>
      <div className="flex gap-1.5">
        {[0,1,2,3,4].map(i => (
          <div key={i} className="w-1.5 h-5 rounded-full bg-indigo-500/30 animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
        ))}
      </div>
    </div>
  );

  return (
    <div className="flex flex-col gap-6 w-full pb-10">
      {/* ── Header ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/60 pb-5">
        <div>
          <h1 className="text-3xl font-black text-slate-100 tracking-tight">AI Resume Optimizer</h1>
          <p className="text-sm text-slate-500 mt-0.5">Evidence-grounded · Recruiter-calibrated · ATS-optimized</p>
        </div>
        <StepProgress current={step} hasProfile={hasProfile} />
      </div>

      {/* ── Error Banner ── */}
      {error && (
        <div className="flex items-start gap-3 px-5 py-4 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400">
          <I d={Icons.x} size="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div className="flex-1 text-sm">{error}</div>
          <button onClick={() => setError(null)} className="flex-shrink-0 text-rose-400/60 hover:text-rose-400"><I d={Icons.x} size="w-4 h-4" /></button>
        </div>
      )}

      {/* ── Processing Overlay ── */}
      {isProcessing && <ProcessingOverlay />}

      {/* ══════════════ STEP 1: SMART UPLOAD / PROFILE ACTIVE ══════════════ */}
      {!isProcessing && step === 1 && (
        <div className="flex flex-col gap-6">
          {hasProfile ? (
            /* Master Profile Active */
            <GCard className="overflow-hidden">
              <div className="h-1 bg-gradient-to-r from-emerald-500 via-teal-500 to-indigo-500" />
              <div className="p-8 flex flex-col md:flex-row items-start md:items-center gap-8">
                <div className="w-20 h-20 rounded-3xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-2xl shadow-emerald-500/30 flex-shrink-0">
                  <I d={Icons.check} size="w-10 h-10 text-white" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-xs font-bold text-emerald-400 uppercase tracking-widest bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">✓ Master Profile Active</span>
                  </div>
                  <h2 className="text-2xl font-black text-slate-100 mb-1">
                    {masterProfile?.structured_evidence?.contact_info?.name || "Your Profile"} is Ready
                  </h2>
                  <p className="text-slate-400 text-sm max-w-lg">
                    Your evidence database is loaded with {masterProfile?.structured_evidence?.skills ? Object.values(masterProfile.structured_evidence.skills).flat().length : 0} verified skills and {(masterProfile?.structured_evidence?.experience || []).length} experience nodes. No upload needed — just paste a job URL below.
                  </p>
                  <div className="flex flex-wrap gap-2 mt-3">
                    {Object.values(masterProfile?.structured_evidence?.skills || {}).flat().slice(0, 8).map((s, i) => (
                      <span key={i} className="text-xs px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 border border-slate-700">{s}</span>
                    ))}
                  </div>
                </div>
                <button
                  onClick={() => setStep(2)}
                  className="flex-shrink-0 px-7 py-3.5 rounded-2xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-bold text-sm shadow-xl shadow-purple-500/25 hover:scale-105 transition-all duration-200"
                >
                  Continue → Set Job Target
                </button>
              </div>
            </GCard>
          ) : (
            /* Upload UI */
            <GCard className="p-8">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-8 h-8 rounded-xl bg-indigo-500/10 flex items-center justify-center"><I d={Icons.upload} size="w-4 h-4 text-indigo-400" /></div>
                <h2 className="text-xl font-bold text-slate-100">Upload Your Master Resume</h2>
              </div>
              <p className="text-sm text-slate-400 mb-8 max-w-lg">
                Upload once. ResumePilot extracts your skills, experience, and projects into a permanent evidence database. Future tailoring requires only a job URL.
              </p>
              <div
                onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={(e) => { e.preventDefault(); setIsDragging(false); const f = e.dataTransfer.files[0]; if (f) handleFileDrop(f); }}
                onClick={() => document.getElementById("resume-file-input").click()}
                className={cn(
                  "border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300",
                  isDragging ? "border-indigo-500 bg-indigo-500/5 scale-[1.01]" : "border-slate-700 hover:border-slate-600 hover:bg-slate-800/20"
                )}
              >
                <input id="resume-file-input" type="file" accept=".pdf,.docx" className="hidden" onChange={(e) => e.target.files[0] && handleFileDrop(e.target.files[0])} />
                <div className="w-16 h-16 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center mx-auto mb-4">
                  <I d={Icons.upload} size="w-8 h-8 text-slate-400" />
                </div>
                <p className="text-slate-300 font-bold text-sm mb-1">{uploadedFile ? uploadedFile.name : "Drop your resume here or click to browse"}</p>
                <p className="text-xs text-slate-500">PDF or DOCX · Max 10 MB</p>
              </div>
            </GCard>
          )}
        </div>
      )}

      {/* ══════════════ STEP 2: JOB TARGET ══════════════ */}
      {!isProcessing && step === 2 && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Input */}
          <div className="lg:col-span-2 flex flex-col gap-5">
            <GCard className="p-6 flex flex-col gap-5">
              <div>
                <h3 className="text-lg font-bold text-slate-100 mb-0.5">Job Target</h3>
                <p className="text-sm text-slate-500">Provide a job URL for auto-scraping, or paste the description manually.</p>
              </div>

              {/* Mode Toggle */}
              <div className="flex rounded-xl border border-slate-700 p-1 bg-slate-800/50 w-fit gap-1">
                {[["url", "🔗 Job URL (Auto-Scrape)"], ["text", "📋 Paste JD Manually"]].map(([mode, label]) => (
                  <button key={mode} onClick={() => setInputMode(mode)}
                    className={cn("px-4 py-2 rounded-lg text-xs font-bold transition-all duration-200",
                      inputMode === mode ? "bg-indigo-500 text-white shadow-md" : "text-slate-400 hover:text-slate-200")}>
                    {label}
                  </button>
                ))}
              </div>

              {inputMode === "url" ? (
                <div className="flex flex-col gap-2">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Job URL</label>
                  <div className="flex gap-2">
                    <div className="flex-1 relative">
                      <div className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500"><I d={Icons.link} size="w-4 h-4" /></div>
                      <input className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                        placeholder="https://linkedin.com/jobs/... or greenhouse.io/... or lever.co/..."
                        value={jobUrl} onChange={e => setJobUrl(e.target.value)} />
                    </div>
                  </div>
                  <p className="text-xs text-slate-600">Supports: LinkedIn · Greenhouse · Lever · Indeed · Wellfound · Company careers pages</p>
                  <div className="border-t border-slate-700/40 pt-3 mt-1">
                    <p className="text-xs text-slate-500 mb-2">Or add job details manually as backup:</p>
                    <textarea rows={3} placeholder="Optional: paste additional job description context..."
                      value={jobDescription} onChange={e => setJobDescription(e.target.value)}
                      className="w-full p-3 bg-slate-800/60 border border-slate-700/60 rounded-xl text-slate-300 text-xs placeholder-slate-600 focus:outline-none focus:border-indigo-500 resize-none transition-colors" />
                  </div>
                </div>
              ) : (
                <div className="flex flex-col gap-2">
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Job Description *</label>
                  <textarea rows={9} placeholder="Paste the complete job description here (minimum 50 characters)..."
                    value={jobDescription} onChange={e => setJobDescription(e.target.value)}
                    className="w-full p-4 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:border-indigo-500 resize-none transition-colors" />
                  <p className="text-xs text-slate-600">{jobDescription.length} characters {jobDescription.length < 50 ? "(min 50)" : "✓"}</p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">Job Title</label>
                  <input className="w-full px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                    placeholder="e.g. Backend Engineer" value={jobTitle} onChange={e => setJobTitle(e.target.value)} />
                </div>
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">Company</label>
                  <input className="w-full px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                    placeholder="e.g. Google, Stripe..." value={company} onChange={e => setCompany(e.target.value)} />
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">GitHub URL (Optional — for portfolio analysis)</label>
                <input className="w-full px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                  placeholder="https://github.com/yourname" value={githubUrl} onChange={e => setGithubUrl(e.target.value)} />
              </div>
            </GCard>

            <div className="flex justify-between items-center">
              <button onClick={() => setStep(1)} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-sm font-semibold hover:bg-slate-700 transition-colors">
                <I d={Icons.back} size="w-4 h-4" /> Back
              </button>
              <button onClick={handleRunPipeline}
                className="flex items-center gap-2 px-7 py-3 rounded-xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-bold text-sm shadow-xl shadow-purple-500/20 hover:scale-105 transition-all duration-200">
                <I d={Icons.zap} size="w-4 h-4" /> Run AI Pipeline
              </button>
            </div>
          </div>

          {/* Right: Template + Strategy */}
          <div className="flex flex-col gap-5">
            <GCard className="p-5 flex flex-col gap-4">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Resume Template</h4>
              <div className="flex flex-col gap-2">
                {TEMPLATES.map(t => (
                  <div key={t.id} onClick={() => setTemplate(t.id)}
                    className={cn("p-3.5 rounded-xl border cursor-pointer transition-all duration-200", template === t.id ? "border-indigo-500 bg-indigo-500/8" : "border-slate-700/60 hover:border-slate-600")}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-bold text-slate-200">{t.name}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-400">{t.badge}</span>
                    </div>
                    <p className="text-xs text-slate-500">{t.desc}</p>
                  </div>
                ))}
              </div>
            </GCard>

            <GCard className="p-5 flex flex-col gap-4">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Strategy Track</h4>
              <div className="grid grid-cols-2 gap-2">
                {TRACKS.map(t => (
                  <div key={t.id} onClick={() => setStrategyTrack(t.id)}
                    className={cn("p-3 rounded-xl border cursor-pointer transition-all duration-200 text-center", strategyTrack === t.id ? "border-purple-500 bg-purple-500/8" : "border-slate-700/60 hover:border-slate-600")}>
                    <div className="text-lg mb-1">{t.icon}</div>
                    <div className={cn("text-xs font-bold", strategyTrack === t.id ? "text-purple-400" : "text-slate-400")}>{t.label}</div>
                  </div>
                ))}
              </div>
            </GCard>
          </div>
        </div>
      )}

      {/* ══════════════ STEP 3: AI INTELLIGENCE AUDIT ══════════════ */}
      {!isProcessing && step === 3 && result && (
        <div className="flex flex-col gap-6">
          {/* Score trinity */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
            <GCard className="p-6 flex flex-col items-center gap-3">
              <ScoreRing score={empScore} size={110} label="Employability Score" sublabel={result?.employability_index?.employability_band || "Strong"} />
            </GCard>
            <GCard className="p-6 flex flex-col items-center gap-3">
              <ScoreRing score={ats.keyword_match_score || 0} size={110} label="ATS Compatibility" sublabel="Keyword + semantic" />
            </GCard>
            <GCard className="p-6 flex flex-col items-center gap-3">
              <ScoreRing score={recruiterScore} size={110} label="Recruiter Readiness" sublabel="6-sec scan simulation" />
            </GCard>
          </div>

          {/* ATS Dimension Breakdown */}
          <GCard className="p-6 flex flex-col gap-4">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <I d={Icons.target} size="w-4 h-4 text-indigo-400" /> ATS Dimension Breakdown
            </h3>
            <div className="flex flex-col gap-3">
              {[
                ["Keyword Match", ats.keyword_match_score],
                ["Semantic Alignment", ats.semantic_similarity_score],
                ["Skills Coverage", ats.skills_alignment_score],
                ["Action Verbs", ats.action_verb_score],
                ["Achievement Density", ats.achievement_score],
                ["Formatting Quality", ats.formatting_score],
                ["Section Completeness", ats.section_completeness_score],
              ].map(([label, val]) => <ScoreBar key={label} label={label} value={val || 0} />)}
            </div>
          </GCard>

          {/* Gap Analysis + Roadmap */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            <GCard className="p-5 flex flex-col gap-4">
              <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
                <I d={Icons.briefcase} size="w-4 h-4 text-rose-400" /> Role Gap Analysis
              </h3>
              {gapReport.length === 0 ? (
                <div className="flex items-center gap-2 text-emerald-400 text-sm py-4">
                  <I d={Icons.check} size="w-5 h-5" /> No critical skill gaps detected. Strong role alignment!
                </div>
              ) : (
                <div className="flex flex-col gap-2 max-h-52 overflow-y-auto pr-1 custom-scrollbar">
                  {gapReport.map((g, i) => (
                    <div key={i} className="flex items-center justify-between gap-3 p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
                      <span className="text-sm font-semibold text-slate-200">{g.keyword}</span>
                      <SeverityBadge level={g.importance} />
                    </div>
                  ))}
                </div>
              )}
            </GCard>

            <GCard className="p-5 flex flex-col gap-4">
              <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
                <I d={Icons.map} size="w-4 h-4 text-teal-400" /> Learning Roadmap
              </h3>
              {roadmap.priority_learning_path && roadmap.priority_learning_path.length > 0 ? (
                <div className="flex flex-col gap-2.5">
                  {roadmap.priority_learning_path.slice(0, 5).map((item, i) => (
                    <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
                      <div className="w-5 h-5 rounded-full bg-teal-500/20 flex items-center justify-center text-xs font-black text-teal-400 flex-shrink-0">{i + 1}</div>
                      <div>
                        <div className="text-sm font-semibold text-slate-200">{typeof item === "string" ? item : item.skill || item.topic}</div>
                        {item.rationale && <div className="text-xs text-slate-500 mt-0.5">{item.rationale}</div>}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-500">No critical learning gaps for this role.</p>
              )}
            </GCard>
          </div>

          {/* Company Intelligence */}
          <GCard className="p-5 flex flex-col gap-4">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">
              <I d={Icons.briefcase} size="w-4 h-4 text-amber-400" /> Company Hiring Intelligence · {company || "Target Company"}
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { label: "Culture Fit", value: companyIntel.culture_emphasis || (template === "startup" ? "Startup Agility" : "Enterprise Scale") },
                { label: "Recruiter Focus", value: companyIntel.hiring_signal || "Technical Depth" },
                { label: "Strategy Track", value: strategyTrack.replace("_", "/").toUpperCase() },
                { label: "Template", value: template.charAt(0).toUpperCase() + template.slice(1) },
              ].map(item => (
                <div key={item.label} className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
                  <div className="text-xs text-slate-500 font-semibold mb-1">{item.label}</div>
                  <div className="text-sm font-bold text-indigo-400">{item.value}</div>
                </div>
              ))}
            </div>
          </GCard>

          <div className="flex justify-between">
            <button onClick={() => setStep(2)} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-sm font-semibold hover:bg-slate-700 transition-colors">
              <I d={Icons.back} size="w-4 h-4" /> Edit Job Target
            </button>
            <button onClick={() => setStep(4)} className="px-7 py-2.5 rounded-xl bg-indigo-600 text-white font-bold text-sm hover:bg-indigo-500 transition-colors shadow-lg shadow-indigo-600/20">
              Review Resume →
            </button>
          </div>
        </div>
      )}

      {/* ══════════════ STEP 4: REVIEW DIFF + COVER LETTER ══════════════ */}
      {!isProcessing && step === 4 && result && (
        <div className="flex flex-col gap-6">
          <GCard className="overflow-hidden">
            <div className="p-5 border-b border-slate-700/40">
              <h3 className="text-sm font-bold text-slate-200">Tailored Resume Preview</h3>
              <p className="text-xs text-slate-500 mt-0.5">AI-assembled from your verified evidence — not generated from scratch</p>
            </div>
            <div className="p-5">
              <MiniResumePreview sections={result.tailored_sections} />
            </div>
          </GCard>

          {/* Cover Letter */}
          <GCard className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h4 className="text-sm font-bold text-slate-200">Cover Letter Generator</h4>
                <p className="text-xs text-slate-500 mt-0.5">AI-crafted using your evidence, the JD, and company culture signals</p>
              </div>
              {!coverLetter && (
                <button onClick={handleGenerateCoverLetter} disabled={isGeneratingCL}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-xs font-bold hover:bg-slate-700 transition-colors disabled:opacity-50">
                  {isGeneratingCL ? <><div className="w-3 h-3 border border-slate-400 border-t-transparent rounded-full animate-spin" /> Generating...</> : "Generate Cover Letter"}
                </button>
              )}
            </div>
            {coverLetter ? (
              <textarea rows={9} value={coverLetter} onChange={e => setCoverLetter(e.target.value)}
                className="w-full p-4 bg-slate-800/50 border border-slate-700 rounded-xl text-slate-300 text-xs font-mono focus:outline-none focus:border-indigo-500 resize-none" />
            ) : (
              <p className="text-xs text-slate-500 p-4 border border-dashed border-slate-700 rounded-xl">
                Click "Generate Cover Letter" to create a targeted cover letter tailored to {company || "the company"} and {jobTitle || "the role"}.
              </p>
            )}
          </GCard>

          <div className="flex justify-between">
            <button onClick={() => setStep(3)} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-sm font-semibold hover:bg-slate-700 transition-colors">
              <I d={Icons.back} size="w-4 h-4" /> Back
            </button>
            <button onClick={() => setStep(5)} className="px-7 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold text-sm shadow-lg shadow-indigo-500/20 hover:scale-105 transition-all">
              Export & Intelligence →
            </button>
          </div>
        </div>
      )}

      {/* ══════════════ STEP 5: EXPORT + FULL INTELLIGENCE ══════════════ */}
      {!isProcessing && step === 5 && result && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* LEFT: Controls + Intelligence Panels */}
          <div className="lg:col-span-5 flex flex-col gap-5">

            {/* Score Summary */}
            <GCard className="p-5">
              <div className="h-1 -mx-5 -mt-5 mb-5 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-t-2xl" />
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-slate-100">Employability OS Index</h3>
                <span className="text-xs bg-indigo-500/10 text-indigo-400 px-2.5 py-1 rounded-full border border-indigo-500/20 font-bold">v4 Audit</span>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Employability", value: empScore, color: "text-indigo-400", ring: "from-indigo-500 to-purple-500" },
                  { label: "ATS Score", value: ats.keyword_match_score || 0, color: "text-teal-400", ring: "from-teal-500 to-emerald-500" },
                ].map(g => (
                  <div key={g.label} className="flex flex-col items-center gap-2 p-4 rounded-xl bg-slate-800/50 border border-slate-700/40">
                    <div className="relative w-16 h-16">
                      <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                        <path stroke="#1e293b" strokeWidth="3" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        <path stroke="url(#g)" strokeWidth="3" strokeLinecap="round" fill="none"
                          strokeDasharray={`${g.value}, 100`}
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                      </svg>
                      <defs><linearGradient id="g"><stop offset="0%" stopColor="#6366f1"/><stop offset="100%" stopColor="#a855f7"/></linearGradient></defs>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className={cn("text-sm font-black", g.color)}>{Math.round(g.value)}</span>
                      </div>
                    </div>
                    <span className="text-xs font-semibold text-slate-400">{g.label}</span>
                  </div>
                ))}
              </div>
            </GCard>

            {/* Template + Download */}
            <GCard className="p-5 flex flex-col gap-4">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Template & Export</h4>
              <div className="flex flex-col gap-2">
                {TEMPLATES.map(t => (
                  <div key={t.id} onClick={() => setTemplate(t.id)}
                    className={cn("px-3.5 py-2.5 rounded-xl border cursor-pointer flex items-center justify-between transition-all", template === t.id ? "border-indigo-500 bg-indigo-500/8" : "border-slate-700/60 hover:border-slate-600")}>
                    <span className={cn("text-sm font-semibold", template === t.id ? "text-indigo-300" : "text-slate-300")}>{t.name}</span>
                    {template === t.id && <span className="text-xs text-indigo-400">✓ Selected</span>}
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-700/40">
                <button onClick={() => handleDownload("pdf")}
                  className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 text-white text-xs font-bold hover:bg-indigo-500 transition-colors">
                  <I d={Icons.down} size="w-3.5 h-3.5" /> PDF
                </button>
                <button onClick={() => handleDownload("docx")}
                  className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-xs font-bold hover:bg-slate-700 transition-colors">
                  <I d={Icons.down} size="w-3.5 h-3.5" /> DOCX
                </button>
              </div>
            </GCard>

            {/* Interview Readiness */}
            {result.interview_readiness && (
              <GCard className="p-5 flex flex-col gap-4">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                  <I d={Icons.users} size="w-3.5 h-3.5 text-purple-400" /> Interview Readiness
                </h4>
                <div className="flex items-center gap-4">
                  <div className="relative w-14 h-14 flex-shrink-0">
                    <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                      <path stroke="#1e293b" strokeWidth="3.5" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831" />
                      <path stroke="#a855f7" strokeWidth="3.5" strokeLinecap="round" fill="none"
                        strokeDasharray={`${result.interview_readiness.interview_readiness_score || 75}, 100`}
                        d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-xs font-black text-purple-400">{result.interview_readiness.interview_readiness_score || 75}</span>
                    </div>
                  </div>
                  <div>
                    <div className="text-sm font-bold text-slate-200">{result.interview_readiness.readiness_band || "Moderately Ready"}</div>
                    <div className="text-xs text-slate-500 mt-0.5">Based on project depth + skill coverage</div>
                  </div>
                </div>
                {result.interview_readiness.likely_topics && (
                  <div className="flex flex-wrap gap-1.5">
                    {result.interview_readiness.likely_topics.slice(0, 5).map((t, i) => (
                      <span key={i} className="text-xs px-2.5 py-1 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20 font-semibold">{t}</span>
                    ))}
                  </div>
                )}
              </GCard>
            )}

            {/* Interview Questions Preview */}
            {(interviewQ.technical_questions || interviewQ.behavioral_questions) && (
              <GCard className="p-5 flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                    <I d={Icons.book} size="w-3.5 h-3.5 text-amber-400" /> Predicted Interview Questions
                  </h4>
                  <Link href="/interview" className="text-xs font-bold text-amber-400 hover:underline">Full Simulator →</Link>
                </div>
                <div className="flex flex-col gap-2 max-h-40 overflow-y-auto custom-scrollbar">
                  {[...(interviewQ.technical_questions || []).slice(0,2), ...(interviewQ.behavioral_questions || []).slice(0,1)].map((q, i) => (
                    <div key={i} className="text-xs text-slate-300 p-2.5 bg-slate-800/50 rounded-lg border border-slate-700/40">
                      <span className="text-amber-400 font-bold mr-1">Q{i+1}.</span> {typeof q === "string" ? q : q.question}
                    </div>
                  ))}
                </div>
              </GCard>
            )}

            {/* Branding Preview */}
            {branding.linkedin_headline && (
              <GCard className="p-5 flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                    <I d={Icons.star} size="w-3.5 h-3.5 text-sky-400" /> Personal Branding
                  </h4>
                  <Link href="/branding" className="text-xs font-bold text-sky-400 hover:underline">Full Optimizer →</Link>
                </div>
                <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
                  <div className="text-xs text-slate-500 mb-1 font-semibold">LinkedIn Headline</div>
                  <div className="text-sm font-bold text-sky-300">{branding.linkedin_headline}</div>
                </div>
              </GCard>
            )}

            {/* Explainability */}
            {explainability.length > 0 && (
              <GCard className="p-5 flex flex-col gap-3">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-2">
                  <I d={Icons.info} size="w-3.5 h-3.5 text-indigo-400" /> Why These Changes?
                </h4>
                <div className="flex flex-col gap-2 max-h-44 overflow-y-auto custom-scrollbar">
                  {explainability.slice(0, 4).map((item, i) => (
                    <div key={i} className="p-2.5 bg-slate-800/40 border border-slate-700/30 rounded-xl text-xs">
                      <span className="font-bold text-slate-200 block mb-0.5">{item.component} → {item.action}</span>
                      <p className="text-slate-400 leading-relaxed">{item.rationale}</p>
                      {item.impact_metric && <span className="text-emerald-400 font-semibold block mt-1">{item.impact_metric}</span>}
                    </div>
                  ))}
                </div>
              </GCard>
            )}

            <div className="flex items-center justify-between pt-2">
              <button onClick={() => setStep(4)} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-sm font-semibold hover:bg-slate-700 transition-colors">
                <I d={Icons.back} size="w-4 h-4" /> Back
              </button>
              <Link href="/dashboard">
                <button className="px-5 py-2.5 rounded-xl bg-slate-800/60 border border-slate-700 text-slate-400 text-sm hover:text-slate-200 hover:bg-slate-700 transition-colors">
                  ← Dashboard
                </button>
              </Link>
            </div>
          </div>

          {/* RIGHT: Live Resume Preview */}
          <div className="lg:col-span-7 flex flex-col gap-4">
            <GCard className="flex flex-col h-full">
              <div className="flex items-center justify-between p-5 border-b border-slate-700/40">
                <div>
                  <h4 className="text-sm font-bold text-slate-200">Live Resume Preview — {template.charAt(0).toUpperCase() + template.slice(1)}</h4>
                  <p className="text-xs text-slate-500 mt-0.5">High-fidelity export simulation · Evidence-grounded</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 font-semibold">Recruiter Scan</span>
                  <button onClick={() => setIsHeatmapActive(h => !h)}
                    className={cn("w-10 h-5 rounded-full transition-all duration-300 relative", isHeatmapActive ? "bg-indigo-500" : "bg-slate-700")}>
                    <div className={cn("absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all duration-300", isHeatmapActive ? "left-5" : "left-0.5")} />
                  </button>
                </div>
              </div>
              <div className="p-5 overflow-y-auto flex-1 custom-scrollbar relative">
                {isHeatmapActive && (
                  <div className="absolute inset-0 pointer-events-none z-10">
                    <div className="absolute top-[14%] left-[10%] right-[10%] h-10 bg-red-500/10 border border-red-500/20 rounded-lg animate-pulse flex items-center px-3">
                      <span className="text-red-400 text-xs font-bold">👁 Name & Contact — High Attention</span>
                    </div>
                    <div className="absolute top-[30%] left-[10%] right-[10%] h-8 bg-amber-500/8 border border-amber-500/15 rounded-lg animate-pulse" />
                    <div className="absolute top-[50%] left-[10%] right-[10%] h-16 bg-indigo-500/8 border border-indigo-500/15 rounded-lg animate-pulse" />
                  </div>
                )}
                <MiniResumePreview sections={result.tailored_sections} />
              </div>
            </GCard>
          </div>
        </div>
      )}
    </div>
  );
}
