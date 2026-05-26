"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "../../contexts/AuthContext";
import { motion, useScroll, useTransform } from "framer-motion";
import {
  LayoutDashboard,
  Zap,
  Clock,
  TrendingUp,
  Users,
  Sparkles,
  LogOut,
  Sun,
  Moon,
} from "lucide-react";
import { useTheme } from "next-themes";
import api from "../../lib/api";
import { useState, useEffect } from "react";

const navItems = [
  {
    group: "Core",
    items: [
      { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard, accent: "indigo" },
      { name: "Tailor Resume", path: "/tailor", icon: Zap, accent: "purple", badge: "AI" },
      { name: "History", path: "/history", icon: Clock, accent: "zinc" },
    ],
  },
  {
    group: "Intelligence",
    items: [
      { name: "Career Intel", path: "/career", icon: TrendingUp, accent: "cyan" },
      { name: "Interview Prep", path: "/interview", icon: Users, accent: "amber", badge: "New" },
      { name: "Branding", path: "/branding", icon: Sparkles, accent: "pink", badge: "New" },
    ],
  },
];

const accentStyles = {
  indigo: { active: "bg-indigo-500/10 border-indigo-500/20 text-indigo-400", indicator: "bg-indigo-500" },
  purple: { active: "bg-purple-500/10 border-purple-500/20 text-purple-400", indicator: "bg-purple-500" },
  zinc:   { active: "bg-zinc-700/40 border-zinc-600/30 text-zinc-300", indicator: "bg-zinc-500" },
  cyan:   { active: "bg-cyan-500/10 border-cyan-500/20 text-cyan-400", indicator: "bg-cyan-500" },
  amber:  { active: "bg-amber-500/10 border-amber-500/20 text-amber-400", indicator: "bg-amber-500" },
  pink:   { active: "bg-pink-500/10 border-pink-500/20 text-pink-400", indicator: "bg-pink-500" },
};

const badgeStyles = {
  AI:  "bg-purple-500/15 text-purple-400 border-purple-500/25",
  New: "bg-emerald-500/15 text-emerald-400 border-emerald-500/25",
};

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const [empScore, setEmpScore] = useState(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => { setMounted(true); }, []);

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

  const scoreColor = empScore >= 85 ? "text-emerald-400" : empScore >= 70 ? "text-cyan-400" : empScore >= 55 ? "text-amber-400" : "text-rose-400";

  return (
    <aside className="w-[240px] flex-shrink-0 border-r border-zinc-800/60 bg-[#09090b] flex flex-col h-full">
      {/* ── Brand ────────────────────────────────────────────── */}
      <div className="px-5 py-5 border-b border-zinc-800/40">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:shadow-indigo-500/30 transition-all duration-300">
            <Zap className="w-4 h-4 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-sm text-zinc-100 leading-tight tracking-tight">
              Resume<span className="text-indigo-400">Pilot</span>
            </span>
            <span className="text-[10px] text-zinc-600 font-medium leading-tight">
              Career OS v4
            </span>
          </div>
        </Link>
      </div>

      {/* ── Navigation ──────────────────────────────────────── */}
      <nav className="flex-1 px-3 py-4 flex flex-col gap-6 overflow-y-auto custom-scrollbar">
        {navItems.map((group) => (
          <div key={group.group} className="flex flex-col gap-0.5">
            <p className="text-[10px] font-semibold text-zinc-600 uppercase tracking-[0.15em] px-3 mb-1.5">
              {group.group}
            </p>
            {group.items.map((item) => {
              const isActive = pathname === item.path || (item.path !== "/dashboard" && pathname.startsWith(item.path));
              const accent = accentStyles[item.accent] || accentStyles.zinc;
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  href={item.path}
                  className={`relative flex items-center gap-3 px-3 py-2 rounded-lg border transition-all duration-200 group ${
                    isActive
                      ? `${accent.active}`
                      : "border-transparent text-zinc-500 hover:text-zinc-200 hover:bg-zinc-800/40"
                  }`}
                >
                  {isActive && (
                    <motion.div
                      layoutId="sidebar-active"
                      className={`absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5 rounded-r-full ${accent.indicator}`}
                      transition={{ type: "spring", stiffness: 500, damping: 35 }}
                    />
                  )}
                  <Icon className="w-[16px] h-[16px] flex-shrink-0" />
                  <span className="text-[13px] font-medium flex-1">{item.name}</span>
                  {item.badge && (
                    <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded-md border ${badgeStyles[item.badge]}`}>
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </div>
        ))}
      </nav>

      {/* ── ATS Score Widget ─────────────────────────────────── */}
      {empScore !== null && (
        <div className="mx-3 mb-3 p-3 rounded-xl bg-zinc-900/80 border border-zinc-800/60">
          <div className="flex items-center gap-3">
            <div className="relative w-9 h-9 flex-shrink-0">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                <path stroke="#27272a" strokeWidth="3" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path stroke="#6366f1" strokeWidth="3" strokeLinecap="round" fill="none"
                  strokeDasharray={`${empScore}, 100`}
                  className="score-ring-enter"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className={`text-[10px] font-bold ${scoreColor}`}>{empScore}</span>
              </div>
            </div>
            <div className="min-w-0">
              <div className="text-[11px] font-semibold text-zinc-300">Avg ATS Score</div>
              <div className="text-[10px] text-zinc-600">from history</div>
            </div>
          </div>
        </div>
      )}

      {/* ── Theme Toggle + User ──────────────────────────────── */}
      <div className="px-3 pb-4 border-t border-zinc-800/40 pt-3 flex flex-col gap-2">
        {/* Theme Toggle */}
        {mounted && (
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="flex items-center gap-3 px-3 py-2 rounded-lg text-zinc-500 hover:text-zinc-200 hover:bg-zinc-800/40 transition-all duration-200 w-full"
          >
            {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            <span className="text-[13px] font-medium">
              {theme === "dark" ? "Light Mode" : "Dark Mode"}
            </span>
          </button>
        )}

        {/* User */}
        <div className="flex items-center gap-2.5 px-3 py-2">
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/15 flex items-center justify-center font-semibold text-indigo-400 text-xs flex-shrink-0">
            {user?.full_name?.charAt(0)?.toUpperCase() || "U"}
          </div>
          <div className="flex flex-col min-w-0">
            <span className="text-[11px] font-semibold text-zinc-300 truncate">{user?.full_name || "User"}</span>
            <span className="text-[10px] text-zinc-600 truncate">{user?.email || ""}</span>
          </div>
        </div>

        {/* Sign Out */}
        <button
          onClick={logout}
          className="flex items-center justify-center gap-2 w-full py-2 rounded-lg text-zinc-500 hover:text-rose-400 hover:bg-rose-950/20 border border-transparent hover:border-rose-900/30 text-xs font-medium transition-all duration-200"
        >
          <LogOut className="w-3.5 h-3.5" />
          Sign Out
        </button>
      </div>
    </aside>
  );
}
