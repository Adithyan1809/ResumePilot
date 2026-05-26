"use client";

import React, { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import api from "../../../lib/api";
import Spinner from "../../../components/ui/Spinner";

// ── Inline Icon Components ────────────────────────────────────────────────────

const Icon = ({ d, className = "w-5 h-5", strokeWidth = 2 }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={strokeWidth} d={d} />
  </svg>
);

const UploadIcon = () => <Icon d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />;
const BrainIcon = () => <Icon d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />;
const ChartIcon = () => <Icon d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />;
const StarIcon = () => <Icon d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />;
const RocketIcon = () => <Icon d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.82m5.84-2.56a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.82m2.56-5.84a14.927 14.927 0 00-2.58 5.84m2.699-2.707a6.001 6.001 0 00-3.014-3.014" />;
const TargetIcon = () => <Icon d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-4a6 6 0 100-12 6 6 0 000 12zm0-4a2 2 0 100-4 2 2 0 000 4z" />;
const ClockIcon = () => <Icon d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />;
const CheckIcon = () => <Icon d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />;
const XIcon = () => <Icon d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />;
const TrendUpIcon = () => <Icon d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />;
const TrashIcon = () => <Icon className="w-4 h-4" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />;
const EyeIcon = () => <Icon className="w-4 h-4" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />;
const ZapIcon = () => <Icon d="M13 10V3L4 14h7v7l9-11h-7z" />;
const FlameIcon = () => <Icon d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.974 7.974 0 01-2.343 5.657z M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z" />;
const TrophyIcon = () => <Icon d="M8 21h8M12 17v4M7 3H5a2 2 0 00-2 2v3c0 3.314 2.686 6 6 6h6c3.314 0 6-2.686 6-6V5a2 2 0 00-2-2h-2M7 3h10M7 3V1m10 2V1" />;
const MapIcon = () => <Icon d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />;
const PlusIcon = () => <Icon d="M12 4v16m8-8H4" />;

// ── Utility ───────────────────────────────────────────────────────────────────
function cn(...classes) {
  return classes.filter(Boolean).join(" ");
}

function formatDate(isoStr) {
  if (!isoStr) return "—";
  return new Date(isoStr).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

function getScoreColor(score) {
  if (score >= 85) return "text-emerald-400";
  if (score >= 70) return "text-teal-400";
  if (score >= 55) return "text-amber-400";
  return "text-rose-400";
}

function getScoreGlow(score) {
  if (score >= 85) return "shadow-emerald-500/20";
  if (score >= 70) return "shadow-teal-500/20";
  if (score >= 55) return "shadow-amber-500/20";
  return "shadow-rose-500/20";
}

function ScoreRing({ score, size = 80 }) {
  const radius = (size - 12) / 2;
  const circumference = 2 * Math.PI * radius;
  const filled = ((score || 0) / 100) * circumference;
  const color =
    score >= 85 ? "#10b981" : score >= 70 ? "#14b8a6" : score >= 55 ? "#f59e0b" : "#f43f5e";

  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={color}
        strokeWidth="6"
        strokeDasharray={circumference}
        strokeDashoffset={circumference - filled}
        strokeLinecap="round"
        style={{ transition: "stroke-dashoffset 0.8s cubic-bezier(0.4,0,0.2,1)" }}
      />
    </svg>
  );
}

function GlassCard({ children, className = "", glowColor = "" }) {
  return (
    <div
      className={cn(
        "relative rounded-2xl border border-slate-800/60 bg-slate-900/60 backdrop-blur-sm shadow-xl overflow-hidden",
        glowColor,
        className
      )}
    >
      {children}
    </div>
  );
}

// ── Application Status Badge ──────────────────────────────────────────────────
function AppStatusBadge({ status }) {
  const cfg = {
    applied: { label: "Applied", cls: "bg-blue-500/15 text-blue-400 border-blue-500/20" },
    callback: { label: "Callback", cls: "bg-teal-500/15 text-teal-400 border-teal-500/20" },
    oa_invite: { label: "OA Invite", cls: "bg-purple-500/15 text-purple-400 border-purple-500/20" },
    interview: { label: "Interview", cls: "bg-amber-500/15 text-amber-400 border-amber-500/20" },
    offer: { label: "Offer 🎉", cls: "bg-emerald-500/15 text-emerald-400 border-emerald-500/20" },
    rejected: { label: "Rejected", cls: "bg-rose-500/15 text-rose-400 border-rose-500/20" },
  };
  const c = cfg[status] || { label: status, cls: "bg-slate-700 text-slate-300 border-slate-600" };
  return (
    <span className={cn("text-xs font-bold px-2.5 py-1 rounded-full border uppercase tracking-wider", c.cls)}>
      {c.label}
    </span>
  );
}

// ── Log Application Modal ─────────────────────────────────────────────────────
function LogAppModal({ onClose, onSubmit }) {
  const [form, setForm] = useState({ company: "", job_title: "", status: "applied" });
  const [loading, setLoading] = useState(false);

  const handle = async () => {
    if (!form.company || !form.job_title) return;
    setLoading(true);
    await onSubmit(form);
    setLoading(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl p-6 flex flex-col gap-5">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-slate-100">Log Application</h3>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 transition-colors">
            ✕
          </button>
        </div>
        <div className="flex flex-col gap-3">
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">Company</label>
            <input
              className="w-full px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm"
              placeholder="e.g. Google, Stripe..."
              value={form.company}
              onChange={(e) => setForm((p) => ({ ...p, company: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">Role</label>
            <input
              className="w-full px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm"
              placeholder="e.g. Backend Engineer"
              value={form.job_title}
              onChange={(e) => setForm((p) => ({ ...p, job_title: e.target.value }))}
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">Initial Status</label>
            <select
              className="w-full px-4 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 focus:outline-none focus:border-indigo-500 text-sm"
              value={form.status}
              onChange={(e) => setForm((p) => ({ ...p, status: e.target.value }))}
            >
              {["applied", "callback", "oa_invite", "interview", "offer", "rejected"].map((s) => (
                <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1).replace("_", " ")}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="flex gap-3 mt-1">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2.5 rounded-xl bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700 text-sm font-semibold transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handle}
            disabled={loading || !form.company || !form.job_title}
            className="flex-1 px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-500 text-white text-sm font-semibold hover:from-indigo-600 hover:to-purple-600 disabled:opacity-50 transition-all"
          >
            {loading ? "Logging..." : "Log Application"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Master Resume Hero Card ───────────────────────────────────────────────────
function MasterResumeHero({ profile, resumes, onUploadClick }) {
  const hasProfile = profile?.has_profile;
  const memory = profile?.profile_memory || {};
  const evidence = profile?.structured_evidence || {};
  const masterResumeId = profile?.master_resume_id;

  const masterResume = resumes.find((r) => r.id === masterResumeId);
  const rawSkills = evidence.skills || [];
  const skills = Array.isArray(rawSkills)
    ? rawSkills
    : Object.values(rawSkills).flat().filter(Boolean);
  const experience = evidence.experience || [];

  if (!hasProfile) {
    return (
      <GlassCard className="col-span-full p-8">
        {/* Decorative gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 via-purple-500/5 to-pink-500/5 pointer-events-none" />
        <div className="relative flex flex-col md:flex-row items-center gap-8">
          <div className="flex-shrink-0 w-24 h-24 rounded-3xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-2xl shadow-indigo-500/30">
            <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div className="flex flex-col gap-3 text-center md:text-left">
            <div className="flex flex-col gap-1">
              <h2 className="text-2xl font-black text-slate-100">Set Your Master Resume</h2>
              <p className="text-slate-400 text-sm max-w-lg">
                Upload your master resume once — ResumePilot extracts your evidence, skills, and experience into a permanent AI profile. Every future tailoring uses this as the ground truth.
              </p>
            </div>
            <div className="flex flex-wrap gap-2 justify-center md:justify-start">
              {["One-time upload", "Persistent AI memory", "Instant tailoring", "Evidence database"].map((tag) => (
                <span key={tag} className="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-bold border border-indigo-500/20">
                  ✓ {tag}
                </span>
              ))}
            </div>
            <div>
              <Link href="/tailor">
                <button className="mt-2 px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-bold text-sm shadow-xl shadow-purple-500/25 hover:shadow-purple-500/40 hover:scale-105 transition-all duration-200">
                  Upload Master Resume →
                </button>
              </Link>
            </div>
          </div>
        </div>
      </GlassCard>
    );
  }

  return (
    <GlassCard className="col-span-full overflow-hidden">
      {/* Top accent bar */}
      <div className="h-1 w-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />
      <div className="p-6 flex flex-col lg:flex-row gap-6">
        {/* Left: identity */}
        <div className="flex-shrink-0 flex flex-col gap-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-xl shadow-indigo-500/30 flex-shrink-0">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div>
              <p className="text-xs font-bold text-indigo-400 uppercase tracking-widest mb-0.5">Master Resume</p>
              <h2 className="text-xl font-black text-slate-100">
                {evidence?.contact_info?.name || masterResume?.filename?.replace(/\.[^.]+$/, "") || "AI Profile Active"}
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                {masterResume?.filename || "Profile synced from latest upload"}
              </p>
            </div>
          </div>

          {/* Profile Memory Stats */}
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: "Tailored", value: memory.tailored_counts || 0, color: "text-indigo-400", icon: "⚡" },
              { label: "Avg Score", value: `${memory.average_ats_score || 0}%`, color: "text-teal-400", icon: "📊" },
            ].map((s) => (
              <div key={s.label} className="bg-slate-800/60 rounded-xl p-3 border border-slate-700/40">
                <div className="text-lg font-extrabold text-slate-100">{s.icon} {s.value}</div>
                <div className="text-xs text-slate-500 font-semibold">{s.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div className="hidden lg:block w-px bg-slate-700/40 self-stretch" />

        {/* Middle: Skills snapshot */}
        <div className="flex flex-col gap-3 flex-1 min-w-0">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Evidence Snapshot</p>
          <div className="flex flex-wrap gap-2">
            {skills.slice(0, 18).map((skill, i) => (
              <span
                key={i}
                className="px-2.5 py-1 rounded-lg bg-slate-800/80 text-slate-300 text-xs font-semibold border border-slate-700/50 hover:border-indigo-500/40 hover:text-indigo-300 transition-colors"
              >
                {skill}
              </span>
            ))}
            {skills.length > 18 && (
              <span className="px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-400 text-xs font-bold border border-indigo-500/20">
                +{skills.length - 18} more
              </span>
            )}
            {skills.length === 0 && (
              <span className="text-sm text-slate-500 italic">No skills extracted yet. Upload a resume to populate evidence.</span>
            )}
          </div>

          {/* Experience preview */}
          {experience.length > 0 && (
            <div className="flex flex-col gap-2 mt-1">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Experience Nodes</p>
              {experience.slice(0, 2).map((exp, i) => (
                <div key={i} className="flex items-center gap-3 bg-slate-800/40 rounded-lg px-3 py-2 border border-slate-700/30">
                  <div className="w-2 h-2 rounded-full bg-indigo-400 flex-shrink-0" />
                  <div className="min-w-0">
                    <span className="text-sm font-semibold text-slate-200 truncate block">{exp.role || exp.title}</span>
                    <span className="text-xs text-slate-500">{exp.company} {exp.duration ? `· ${exp.duration}` : ""}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right: CTAs */}
        <div className="flex flex-col gap-3 flex-shrink-0 lg:w-44">
          <Link href="/tailor">
            <button className="w-full px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-bold hover:from-indigo-600 hover:to-purple-700 shadow-lg shadow-indigo-500/20 transition-all hover:scale-105">
              ⚡ Tailor Resume
            </button>
          </Link>
          <button
            onClick={onUploadClick}
            className="w-full px-4 py-2.5 rounded-xl bg-slate-800 text-slate-300 text-sm font-semibold border border-slate-700 hover:bg-slate-700 hover:text-slate-100 transition-colors"
          >
            ↑ Update Profile
          </button>
          {memory.target_roles_history?.length > 0 && (
            <div className="mt-1 p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Last Target</p>
              <p className="text-sm font-bold text-slate-200 truncate">
                {memory.target_roles_history[memory.target_roles_history.length - 1]?.role}
              </p>
              <p className="text-xs text-slate-500 truncate">
                {memory.target_roles_history[memory.target_roles_history.length - 1]?.company}
              </p>
            </div>
          )}
        </div>
      </div>
    </GlassCard>
  );
}

// ── Stats Row ─────────────────────────────────────────────────────────────────
function StatsRow({ profile, historyItems }) {
  const memory = profile?.profile_memory || {};
  const analytics = profile?.analytics || {};
  const hasProfile = profile?.has_profile;

  const scores = historyItems.map((i) => i.overall_score || 0).filter(Boolean);
  const bestScore = scores.length ? Math.max(...scores) : 0;
  const avgScore = scores.length
    ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
    : memory.average_ats_score || 0;

  const stats = [
    {
      label: "Versions Tailored",
      value: memory.tailored_counts || historyItems.length || 0,
      icon: <ZapIcon />,
      color: "from-indigo-500/20 to-indigo-600/5",
      border: "border-indigo-500/20",
      iconColor: "text-indigo-400",
      bg: "bg-indigo-500/10",
    },
    {
      label: "Best ATS Score",
      value: `${bestScore}%`,
      icon: <TrophyIcon />,
      color: "from-amber-500/20 to-amber-600/5",
      border: "border-amber-500/20",
      iconColor: "text-amber-400",
      bg: "bg-amber-500/10",
    },
    {
      label: "Avg ATS Score",
      value: `${Math.round(avgScore)}%`,
      icon: <ChartIcon />,
      color: "from-teal-500/20 to-teal-600/5",
      border: "border-teal-500/20",
      iconColor: "text-teal-400",
      bg: "bg-teal-500/10",
    },
    {
      label: "Apps Tracked",
      value: analytics.total_applied || 0,
      icon: <TargetIcon />,
      color: "from-purple-500/20 to-purple-600/5",
      border: "border-purple-500/20",
      iconColor: "text-purple-400",
      bg: "bg-purple-500/10",
    },
    {
      label: "Callbacks Earned",
      value: analytics.callbacks || 0,
      icon: <CheckIcon />,
      color: "from-emerald-500/20 to-emerald-600/5",
      border: "border-emerald-500/20",
      iconColor: "text-emerald-400",
      bg: "bg-emerald-500/10",
    },
    {
      label: "Success Rate",
      value: `${Math.round((analytics.success_rate || 0) * 100)}%`,
      icon: <FlameIcon />,
      color: "from-rose-500/20 to-rose-600/5",
      border: "border-rose-500/20",
      iconColor: "text-rose-400",
      bg: "bg-rose-500/10",
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
      {stats.map((s) => (
        <div
          key={s.label}
          className={cn(
            "rounded-2xl border p-4 flex flex-col gap-3 bg-gradient-to-br",
            s.color, s.border,
            "backdrop-blur-sm transition-all hover:scale-105 hover:shadow-lg duration-200"
          )}
        >
          <div className={cn("w-9 h-9 rounded-xl flex items-center justify-center", s.bg)}>
            <div className={s.iconColor}>{s.icon}</div>
          </div>
          <div>
            <div className="text-2xl font-black text-slate-100 tracking-tight">{s.value}</div>
            <div className="text-xs font-semibold text-slate-500 mt-0.5">{s.label}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Application Tracker ───────────────────────────────────────────────────────
function ApplicationTracker({ profile, onLog, onStatusUpdate }) {
  const apps = profile?.applications_log?.applications || [];
  const [selected, setSelected] = useState(null);

  const statuses = ["applied", "callback", "oa_invite", "interview", "offer", "rejected"];

  if (apps.length === 0) {
    return (
      <GlassCard className="flex flex-col gap-4 p-6 h-full">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-purple-500/10 flex items-center justify-center">
              <div className="text-purple-400"><TargetIcon /></div>
            </div>
            <h3 className="text-sm font-bold text-slate-200">Application Tracker</h3>
          </div>
          <button
            onClick={onLog}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-500/10 text-indigo-400 text-xs font-bold border border-indigo-500/20 hover:bg-indigo-500/20 transition-colors"
          >
            <PlusIcon /> Log
          </button>
        </div>
        <div className="flex-1 flex flex-col items-center justify-center gap-3 py-6">
          <div className="w-14 h-14 rounded-2xl bg-slate-800/80 border border-slate-700/40 flex items-center justify-center">
            <div className="text-slate-600"><MapIcon /></div>
          </div>
          <p className="text-sm text-slate-500 text-center">No applications tracked yet.<br />Log your first application to begin.</p>
          <button
            onClick={onLog}
            className="px-4 py-2 rounded-xl bg-indigo-500/10 text-indigo-400 text-xs font-bold border border-indigo-500/20 hover:bg-indigo-500/20 transition-colors"
          >
            + Track First Application
          </button>
        </div>
      </GlassCard>
    );
  }

  return (
    <GlassCard className="flex flex-col h-full">
      <div className="p-5 border-b border-slate-700/40">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-purple-500/10 flex items-center justify-center">
              <div className="text-purple-400"><TargetIcon /></div>
            </div>
            <h3 className="text-sm font-bold text-slate-200">Application Tracker</h3>
            <span className="ml-1 px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 text-xs font-bold border border-slate-700">
              {apps.length}
            </span>
          </div>
          <button
            onClick={onLog}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-500/10 text-indigo-400 text-xs font-bold border border-indigo-500/20 hover:bg-indigo-500/20 transition-colors"
          >
            <PlusIcon /> Log
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto max-h-72 custom-scrollbar divide-y divide-slate-700/30">
        {[...apps].reverse().slice(0, 12).map((app) => (
          <div key={app.id} className="flex items-center gap-3 px-5 py-3 hover:bg-slate-800/30 transition-colors group">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-slate-200 truncate">{app.job_title}</span>
              </div>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="text-xs text-slate-500">{app.company}</span>
                <span className="text-slate-700">·</span>
                <span className="text-xs text-slate-600">{formatDate(app.logged_at)}</span>
              </div>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <AppStatusBadge status={app.status} />
              <select
                className="opacity-0 group-hover:opacity-100 transition-opacity text-xs bg-slate-800 border border-slate-600 rounded-lg px-2 py-1 text-slate-300 focus:outline-none focus:border-indigo-500"
                value={app.status}
                onChange={(e) => onStatusUpdate(app.id, e.target.value)}
              >
                {statuses.map((s) => (
                  <option key={s} value={s}>{s.replace("_", " ")}</option>
                ))}
              </select>
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}

// ── Career Intelligence Panel ─────────────────────────────────────────────────
function CareerIntelPanel({ profile }) {
  const memory = profile?.profile_memory || {};
  const rolesHistory = memory.target_roles_history || [];

  const progressionSteps = [
    { title: "Junior Developer", description: "Build core skills, land first internship", status: "done" },
    { title: "Mid-Level Engineer", description: "Production systems, team contributions", status: "active" },
    { title: "Senior / Lead", description: "Architecture ownership, mentorship", status: "future" },
    { title: "Staff / Principal", description: "Cross-team impact, technical strategy", status: "future" },
  ];

  return (
    <GlassCard className="flex flex-col h-full">
      <div className="p-5 border-b border-slate-700/40">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-teal-500/10 flex items-center justify-center">
            <div className="text-teal-400"><MapIcon /></div>
          </div>
          <h3 className="text-sm font-bold text-slate-200">Career Timeline</h3>
        </div>
      </div>
      <div className="p-5 flex flex-col gap-4">
        {/* Progression steps */}
        <div className="flex flex-col gap-3">
          {progressionSteps.map((step, i) => (
            <div key={i} className="flex items-start gap-3">
              <div className="flex flex-col items-center mt-1">
                <div
                  className={cn(
                    "w-3.5 h-3.5 rounded-full border-2 flex-shrink-0",
                    step.status === "done"
                      ? "bg-emerald-400 border-emerald-400"
                      : step.status === "active"
                      ? "bg-indigo-400 border-indigo-400 ring-2 ring-indigo-400/30"
                      : "bg-slate-700 border-slate-600"
                  )}
                />
                {i < progressionSteps.length - 1 && (
                  <div className={cn("w-0.5 h-6 mt-1", step.status === "done" ? "bg-emerald-400/40" : "bg-slate-700")} />
                )}
              </div>
              <div className="pb-2">
                <div className={cn("text-sm font-bold", step.status === "future" ? "text-slate-500" : "text-slate-200")}>
                  {step.title}
                  {step.status === "active" && (
                    <span className="ml-2 text-xs font-bold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded-full border border-indigo-500/20">
                      You are here
                    </span>
                  )}
                </div>
                <div className="text-xs text-slate-500 mt-0.5">{step.description}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Roles history */}
        {rolesHistory.length > 0 && (
          <div className="border-t border-slate-700/40 pt-4">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Targeted Roles</p>
            <div className="flex flex-col gap-1.5">
              {rolesHistory.slice(-4).reverse().map((r, i) => (
                <div key={i} className="flex items-center justify-between gap-2 text-xs">
                  <span className="text-slate-300 truncate">{r.role} @ {r.company}</span>
                  <span className={cn("font-bold flex-shrink-0", getScoreColor(r.score))}>{r.score}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </GlassCard>
  );
}

// ── Score Trend Sparkline ─────────────────────────────────────────────────────
function ScoreTrend({ items }) {
  if (!items.length) return null;

  const scores = items.slice(0, 10).reverse().map((i) => i.overall_score || 0);
  const max = Math.max(...scores, 1);
  const min = Math.min(...scores, 0);
  const range = max - min || 1;

  const w = 280;
  const h = 60;
  const pts = scores.map((s, i) => {
    const x = (i / (scores.length - 1)) * w;
    const y = h - ((s - min) / range) * (h - 8) - 4;
    return `${x},${y}`;
  });

  const polyline = pts.join(" ");
  const areaPath = `M${pts[0]} L${polyline.split(" ").slice(1).join(" L")} L${w},${h} L0,${h} Z`;

  return (
    <GlassCard className="p-5">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-indigo-500/10 flex items-center justify-center">
            <div className="text-indigo-400"><TrendUpIcon /></div>
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-200">ATS Score Trend</h3>
            <p className="text-xs text-slate-500">{items.length} tailoring sessions</p>
          </div>
        </div>
        <div className={cn("text-2xl font-black", getScoreColor(scores[scores.length - 1] || 0))}>
          {scores[scores.length - 1] || 0}%
        </div>
      </div>
      <svg viewBox={`0 0 ${w} ${h}`} className="w-full h-16" preserveAspectRatio="none">
        <defs>
          <linearGradient id="scoreGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6366f1" stopOpacity="0.3" />
            <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d={areaPath} fill="url(#scoreGrad)" />
        <polyline
          points={polyline}
          fill="none"
          stroke="#6366f1"
          strokeWidth="2.5"
          strokeLinejoin="round"
          strokeLinecap="round"
        />
        {scores.map((s, i) => (
          <circle
            key={i}
            cx={(i / (scores.length - 1)) * w}
            cy={h - ((s - min) / range) * (h - 8) - 4}
            r="3.5"
            fill="#6366f1"
          />
        ))}
      </svg>
    </GlassCard>
  );
}

// ── Recent Optimizations Table ────────────────────────────────────────────────
function RecentOptimizations({ items, onDelete }) {
  if (!items.length) {
    return (
      <GlassCard className="p-6 flex flex-col items-center justify-center gap-4 py-12">
        <div className="w-16 h-16 rounded-2xl bg-slate-800/80 border border-slate-700/40 flex items-center justify-center">
          <div className="text-slate-600"><RocketIcon /></div>
        </div>
        <div className="text-center">
          <h3 className="text-slate-300 font-bold text-sm">No Tailored Resumes Yet</h3>
          <p className="text-slate-500 text-xs mt-1">Start by tailoring a resume to a job description.</p>
        </div>
        <Link href="/tailor">
          <button className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-500 text-white text-sm font-bold shadow-lg shadow-indigo-500/20 hover:scale-105 transition-all">
            Tailor First Resume →
          </button>
        </Link>
      </GlassCard>
    );
  }

  return (
    <GlassCard>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700/40">
              <th className="px-5 py-3.5 text-left text-xs font-bold text-slate-500 uppercase tracking-widest">Role</th>
              <th className="px-5 py-3.5 text-left text-xs font-bold text-slate-500 uppercase tracking-widest hidden md:table-cell">Company</th>
              <th className="px-5 py-3.5 text-center text-xs font-bold text-slate-500 uppercase tracking-widest">ATS Score</th>
              <th className="px-5 py-3.5 text-left text-xs font-bold text-slate-500 uppercase tracking-widest hidden lg:table-cell">Template</th>
              <th className="px-5 py-3.5 text-left text-xs font-bold text-slate-500 uppercase tracking-widest hidden sm:table-cell">Date</th>
              <th className="px-5 py-3.5 text-right text-xs font-bold text-slate-500 uppercase tracking-widest">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/20">
            {items.slice(0, 8).map((item) => {
              const score = item.overall_score || 0;
              return (
                <tr key={item.id} className="hover:bg-slate-800/30 transition-colors group">
                  <td className="px-5 py-3.5">
                    <span className="text-sm font-semibold text-slate-200">{item.job_title || "Unknown Role"}</span>
                  </td>
                  <td className="px-5 py-3.5 hidden md:table-cell">
                    <span className="text-sm text-slate-400">{item.company || "—"}</span>
                  </td>
                  <td className="px-5 py-3.5">
                    <div className="flex items-center justify-center gap-2">
                      <div className="relative flex-shrink-0">
                        <ScoreRing score={score} size={42} />
                        <span className={cn("absolute inset-0 flex items-center justify-center text-xs font-black", getScoreColor(score))}>
                          {score}
                        </span>
                      </div>
                    </div>
                  </td>
                  <td className="px-5 py-3.5 hidden lg:table-cell">
                    <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-slate-800 text-slate-400 border border-slate-700 capitalize">
                      {item.template || "classic"}
                    </span>
                  </td>
                  <td className="px-5 py-3.5 hidden sm:table-cell">
                    <span className="text-xs text-slate-500">{formatDate(item.created_at)}</span>
                  </td>
                  <td className="px-5 py-3.5">
                    <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Link href={`/tailor?id=${item.id}`}>
                        <button className="p-1.5 rounded-lg hover:bg-indigo-500/10 text-slate-500 hover:text-indigo-400 transition-colors">
                          <EyeIcon />
                        </button>
                      </Link>
                      <button
                        onClick={() => onDelete(item.id)}
                        className="p-1.5 rounded-lg hover:bg-rose-500/10 text-slate-500 hover:text-rose-400 transition-colors"
                      >
                        <TrashIcon />
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </GlassCard>
  );
}

// ── Market Intelligence Snippet ───────────────────────────────────────────────
function MarketIntelPanel({ evidence }) {
  const rawSkills = evidence?.skills || [];
  const skills = Array.isArray(rawSkills)
    ? rawSkills
    : Object.values(rawSkills).flat().filter(Boolean);

  const trendingTech = [
    { name: "Python", demand: 94, trend: "+12%" },
    { name: "TypeScript", demand: 89, trend: "+18%" },
    { name: "Kubernetes", demand: 82, trend: "+22%" },
    { name: "React", demand: 87, trend: "+8%" },
    { name: "FastAPI", demand: 76, trend: "+31%" },
    { name: "LLM/AI", demand: 91, trend: "+85%" },
  ];

  const yourSkillSet = new Set(skills.map((s) => s.toLowerCase()));
  const enriched = trendingTech.map((t) => ({
    ...t,
    hasSkill: yourSkillSet.has(t.name.toLowerCase()) ||
      skills.some((s) => s.toLowerCase().includes(t.name.toLowerCase())),
  }));

  return (
    <GlassCard className="flex flex-col h-full">
      <div className="p-5 border-b border-slate-700/40">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-amber-500/10 flex items-center justify-center">
            <div className="text-amber-400"><TrendUpIcon /></div>
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-200">Market Intelligence</h3>
            <p className="text-xs text-slate-500">2025 trending technologies</p>
          </div>
        </div>
      </div>
      <div className="p-5 flex flex-col gap-3">
        {enriched.map((tech) => (
          <div key={tech.name} className="flex items-center gap-3">
            <div className="w-24 flex-shrink-0">
              <span className={cn("text-sm font-semibold", tech.hasSkill ? "text-slate-200" : "text-slate-500")}>
                {tech.name}
              </span>
            </div>
            <div className="flex-1 bg-slate-800/60 rounded-full h-2 overflow-hidden">
              <div
                className={cn("h-full rounded-full transition-all duration-700", tech.hasSkill ? "bg-gradient-to-r from-indigo-500 to-purple-500" : "bg-slate-600")}
                style={{ width: `${tech.demand}%` }}
              />
            </div>
            <div className="w-12 flex-shrink-0 text-right">
              <span className="text-xs font-bold text-emerald-400">{tech.trend}</span>
            </div>
            <div className="w-6 flex-shrink-0 text-center">
              {tech.hasSkill ? (
                <span className="text-xs text-emerald-400">✓</span>
              ) : (
                <span className="text-xs text-slate-600">–</span>
              )}
            </div>
          </div>
        ))}
        <div className="pt-2 border-t border-slate-700/40 flex items-center justify-between text-xs">
          <span className="text-slate-500">
            <span className="text-emerald-400 font-bold">{enriched.filter((t) => t.hasSkill).length}</span>/{enriched.length} in your profile
          </span>
          <span className="text-indigo-400 font-bold cursor-pointer hover:underline">View Full Report →</span>
        </div>
      </div>
    </GlassCard>
  );
}

// ── Main Dashboard Page ───────────────────────────────────────────────────────
export default function DashboardPage() {
  const router = useRouter();

  const [profile, setProfile] = useState(null);
  const [historyItems, setHistoryItems] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showLogModal, setShowLogModal] = useState(false);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [profileRes, historyRes, resumesRes] = await Promise.allSettled([
        api.get("/tailor/profile/master"),
        api.get("/tailor/history"),
        api.get("/resumes/"),
      ]);

      if (profileRes.status === "fulfilled") setProfile(profileRes.value);
      if (historyRes.status === "fulfilled") setHistoryItems(historyRes.value.items || []);
      if (resumesRes.status === "fulfilled") setResumes(resumesRes.value.resumes || []);
    } catch (err) {
      console.error("Dashboard load error:", err);
      setError("Failed to load dashboard data. Please refresh.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleDelete = async (id) => {
    if (!confirm("Delete this tailoring entry?")) return;
    try {
      await api.delete(`/tailor/${id}`);
      setHistoryItems((prev) => prev.filter((i) => i.id !== id));
    } catch {
      setHistoryItems((prev) => prev.filter((i) => i.id !== id));
    }
  };

  const handleLogApp = async (form) => {
    try {
      await api.post("/tailor/applications", form);
      setShowLogModal(false);
      // Reload profile to get updated apps
      const profileRes = await api.get("/tailor/profile/master");
      setProfile(profileRes);
    } catch (err) {
      // Optimistic local update
      const newApp = {
        id: Date.now().toString(),
        ...form,
        logged_at: new Date().toISOString(),
      };
      setProfile((prev) => ({
        ...prev,
        has_profile: true,
        applications_log: {
          applications: [...(prev?.applications_log?.applications || []), newApp],
        },
        analytics: {
          ...(prev?.analytics || {}),
          total_applied: (prev?.analytics?.total_applied || 0) + 1,
        },
      }));
      setShowLogModal(false);
    }
  };

  const handleStatusUpdate = async (appId, newStatus) => {
    try {
      await api.put(`/tailor/applications/${appId}`, { status: newStatus });
      setProfile((prev) => {
        const apps = (prev?.applications_log?.applications || []).map((a) =>
          a.id === appId ? { ...a, status: newStatus } : a
        );
        return { ...prev, applications_log: { applications: apps } };
      });
    } catch {
      // silent fail
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-[70vh] w-full items-center justify-center flex-col gap-4">
        <Spinner size="lg" color="indigo" />
        <span className="text-xs text-slate-500 font-bold uppercase tracking-widest animate-pulse">
          Loading Career Intelligence...
        </span>
      </div>
    );
  }

  const evidence = profile?.structured_evidence || {};

  return (
    <div className="flex flex-col gap-7 w-full pb-8">
      {/* ── Header ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-100 tracking-tight">
            Career Command Center
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Your AI-powered employability dashboard — master profile, applications & intelligence
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowLogModal(true)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700 text-sm font-semibold transition-colors"
          >
            <div className="w-4 h-4"><PlusIcon /></div>
            Log Application
          </button>
          <Link href="/tailor">
            <button className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white text-sm font-bold shadow-xl shadow-purple-500/20 hover:scale-105 transition-all duration-200">
              <div className="w-4 h-4"><ZapIcon /></div>
              Tailor Resume
            </button>
          </Link>
        </div>
      </div>

      {error && (
        <div className="px-5 py-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-sm font-semibold">
          ⚠ {error}
        </div>
      )}

      {/* ── Master Resume Hero ── */}
      <MasterResumeHero
        profile={profile}
        resumes={resumes}
        onUploadClick={() => router.push("/tailor")}
      />

      {/* ── Stats Row ── */}
      <StatsRow profile={profile} historyItems={historyItems} />

      {/* ── Three-column intelligence grid ── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <ApplicationTracker
          profile={profile}
          onLog={() => setShowLogModal(true)}
          onStatusUpdate={handleStatusUpdate}
        />
        <CareerIntelPanel profile={profile} />
        <MarketIntelPanel evidence={evidence} />
      </div>

      {/* ── Score Trend ── */}
      {historyItems.length > 1 && <ScoreTrend items={historyItems} />}

      {/* ── Recent Optimizations ── */}
      <div className="flex flex-col gap-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-indigo-500/10 flex items-center justify-center">
              <div className="text-indigo-400"><RocketIcon /></div>
            </div>
            <h2 className="text-sm font-bold text-slate-200">Recent Optimizations</h2>
            {historyItems.length > 0 && (
              <span className="px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 text-xs font-bold border border-slate-700">
                {historyItems.length}
              </span>
            )}
          </div>
          {historyItems.length > 0 && (
            <Link href="/history" className="text-xs font-bold text-indigo-400 hover:text-indigo-300 hover:underline transition-colors">
              View All →
            </Link>
          )}
        </div>
        <RecentOptimizations items={historyItems} onDelete={handleDelete} />
      </div>

      {/* ── Log App Modal ── */}
      {showLogModal && (
        <LogAppModal onClose={() => setShowLogModal(false)} onSubmit={handleLogApp} />
      )}
    </div>
  );
}
