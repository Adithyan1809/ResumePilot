"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "../../contexts/AuthContext";
import api from "../../lib/api";

const NavIcon = ({ d }) => (
  <svg className="w-4.5 h-4.5 w-[18px] h-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={d} />
  </svg>
);

const navItems = [
  {
    group: "Core",
    items: [
      {
        name: "Dashboard",
        path: "/dashboard",
        icon: "M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z",
        accent: "indigo",
      },
      {
        name: "Tailor Resume",
        path: "/tailor",
        icon: "M13 10V3L4 14h7v7l9-11h-7z",
        accent: "purple",
        badge: "AI",
      },
      {
        name: "History",
        path: "/history",
        icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
        accent: "slate",
      },
    ],
  },
  {
    group: "Career Intelligence",
    items: [
      {
        name: "Career Intel",
        path: "/career",
        icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z",
        accent: "teal",
      },
      {
        name: "Interview Prep",
        path: "/interview",
        icon: "M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z",
        accent: "amber",
        badge: "New",
      },
      {
        name: "Branding",
        path: "/branding",
        icon: "M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z",
        accent: "pink",
        badge: "New",
      },
    ],
  },
];

const accentMap = {
  indigo: { active: "bg-indigo-600/15 border-indigo-500/25 text-indigo-400", dot: "bg-indigo-500", glow: "shadow-indigo-500/10" },
  purple: { active: "bg-purple-600/15 border-purple-500/25 text-purple-400", dot: "bg-purple-500", glow: "shadow-purple-500/10" },
  slate:  { active: "bg-slate-700/50 border-slate-600/50 text-slate-300",   dot: "bg-slate-500", glow: "" },
  teal:   { active: "bg-teal-600/15 border-teal-500/25 text-teal-400",     dot: "bg-teal-500",  glow: "shadow-teal-500/10" },
  amber:  { active: "bg-amber-600/15 border-amber-500/25 text-amber-400",  dot: "bg-amber-500", glow: "shadow-amber-500/10" },
  pink:   { active: "bg-pink-600/15 border-pink-500/25 text-pink-400",     dot: "bg-pink-500",  glow: "shadow-pink-500/10" },
};

const badgeColors = {
  AI:  "bg-purple-500/20 text-purple-400 border-purple-500/30",
  New: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
};

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [empScore, setEmpScore] = useState(null);

  // Load employability score for the sidebar widget
  useEffect(() => {
    (async () => {
      try {
        const p = await api.get("/tailor/profile/master");
        if (p?.has_profile && p?.profile_memory?.average_ats_score) {
          setEmpScore(Math.round(p.profile_memory.average_ats_score));
        }
      } catch { /* silent */ }
    })();
  }, []);

  const scoreColor = empScore >= 85 ? "text-emerald-400" : empScore >= 70 ? "text-teal-400" : empScore >= 55 ? "text-amber-400" : "text-rose-400";
  const scoreArc = empScore ? `${empScore}, 100` : "0, 100";

  return (
    <aside className="w-60 flex-shrink-0 border-r border-slate-800/80 bg-slate-950 flex flex-col h-full">
      {/* Brand */}
      <div className="px-5 py-5 border-b border-slate-800/60">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 group-hover:shadow-indigo-500/30 transition-all duration-300">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div className="flex flex-col">
            <span className="font-extrabold text-sm text-slate-100 leading-tight">
              Resume<span className="text-indigo-400">Pilot</span>
            </span>
            <span className="text-xs text-slate-600 font-medium leading-tight">Career OS v4</span>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 flex flex-col gap-5 overflow-y-auto custom-scrollbar">
        {navItems.map((group) => (
          <div key={group.group} className="flex flex-col gap-1">
            <p className="text-xs font-bold text-slate-600 uppercase tracking-widest px-3 mb-1">{group.group}</p>
            {group.items.map((item) => {
              const isActive = pathname === item.path || (item.path !== "/dashboard" && pathname.startsWith(item.path));
              const accent = accentMap[item.accent] || accentMap.slate;
              return (
                <Link key={item.name} href={item.path}
                  className={`flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-all duration-200 group ${
                    isActive
                      ? `${accent.active} shadow-md ${accent.glow}`
                      : "border-transparent text-slate-500 hover:text-slate-200 hover:bg-slate-800/50"
                  }`}>
                  {/* Active indicator dot */}
                  <div className="relative flex-shrink-0">
                    {isActive && (
                      <div className={`absolute -left-1 top-1/2 -translate-y-1/2 w-1 h-4 rounded-r-full ${accent.dot}`} />
                    )}
                    <NavIcon d={item.icon} />
                  </div>
                  <span className="text-sm font-semibold flex-1">{item.name}</span>
                  {item.badge && (
                    <span className={`text-xs font-bold px-1.5 py-0.5 rounded-full border ${badgeColors[item.badge] || ""}`}>
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </div>
        ))}
      </nav>

      {/* Employability Score Widget */}
      {empScore !== null && (
        <div className="mx-3 mb-3 p-3.5 rounded-2xl bg-slate-900 border border-slate-800/80">
          <div className="flex items-center gap-3">
            <div className="relative w-10 h-10 flex-shrink-0">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                <path stroke="#1e293b" strokeWidth="3.5" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path stroke="#6366f1" strokeWidth="3.5" strokeLinecap="round" fill="none"
                  strokeDasharray={scoreArc}
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className={`text-xs font-black ${scoreColor}`}>{empScore}</span>
              </div>
            </div>
            <div className="min-w-0">
              <div className="text-xs font-bold text-slate-300 truncate">Avg ATS Score</div>
              <div className="text-xs text-slate-600">from your tailoring history</div>
            </div>
          </div>
        </div>
      )}

      {/* User Profile + Logout */}
      <div className="px-3 pb-4 border-t border-slate-800/60 pt-3 flex flex-col gap-2">
        <div className="flex items-center gap-2.5 px-3 py-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/20 flex items-center justify-center font-bold text-indigo-400 text-sm flex-shrink-0">
            {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
          </div>
          <div className="flex flex-col min-w-0">
            <span className="text-xs font-bold text-slate-300 truncate">{user?.full_name || "User Account"}</span>
            <span className="text-xs text-slate-600 truncate">{user?.email || ""}</span>
          </div>
        </div>
        <button onClick={logout}
          className="flex items-center justify-center gap-2 w-full py-2 rounded-xl text-slate-500 hover:text-rose-400 hover:bg-rose-950/20 border border-transparent hover:border-rose-900/40 text-xs font-semibold transition-all duration-200">
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          Sign Out
        </button>
      </div>
    </aside>
  );
}
