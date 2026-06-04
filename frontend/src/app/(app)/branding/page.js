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

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);
  const handle = () => {
    navigator.clipboard?.writeText(text).catch(() => {});
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };
  return (
    <button onClick={handle}
      className={`text-xs px-2.5 py-1 rounded-lg border font-bold transition-all ${copied ? "bg-emerald-500/15 border-emerald-500/25 text-emerald-400" : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200 hover:border-slate-600"}`}>
      {copied ? "✓ Copied" : "Copy"}
    </button>
  );
}

function BrandingCard({ icon, title, content, accent = "indigo", editable = true }) {
  const [val, setVal] = useState(content || "");
  useEffect(() => { setVal(content || ""); }, [content]);
  const accentBorder = { indigo: "border-l-indigo-500", teal: "border-l-teal-500", purple: "border-l-purple-500", sky: "border-l-sky-500", amber: "border-l-amber-500" };
  const accentText = { indigo: "text-indigo-400", teal: "text-teal-400", purple: "text-purple-400", sky: "text-sky-400", amber: "text-amber-400" };

  return (
    <div className={`p-5 rounded-xl bg-slate-800/50 border border-slate-700/40 border-l-4 ${accentBorder[accent] || accentBorder.indigo}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-lg">{icon}</span>
          <h3 className={`text-xs font-bold uppercase tracking-widest ${accentText[accent] || accentText.indigo}`}>{title}</h3>
        </div>
        {val && <CopyButton text={val} />}
      </div>
      {editable ? (
        <textarea
          value={val}
          onChange={e => setVal(e.target.value)}
          rows={val && val.length > 120 ? 4 : 2}
          className="w-full bg-transparent text-slate-200 text-sm leading-relaxed focus:outline-none resize-none placeholder-slate-600"
          placeholder="Generate to populate this field..."
        />
      ) : (
        <p className="text-sm text-slate-200 leading-relaxed">{val || <span className="text-slate-600">Generate to populate...</span>}</p>
      )}
    </div>
  );
}

const PLATFORM_TABS = ["LinkedIn", "GitHub", "Portfolio", "Twitter/X"];

const PLATFORM_ICONS = {
  LinkedIn: "🔗",
  GitHub: "🐙",
  "Portfolio": "🌐",
  "Twitter/X": "🐦",
};

export default function BrandingPage() {
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [activePlatform, setActivePlatform] = useState("LinkedIn");
  const [targetRole, setTargetRole] = useState("");
  const [tone, setTone] = useState("professional");
  const [branding, setBranding] = useState(null);
  const [generated, setGenerated] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const p = await api.get("/tailor/profile/master");
        setProfile(p);
        const lastRole = p?.profile_memory?.target_roles_history?.slice(-1)?.[0];
        if (lastRole?.role) setTargetRole(lastRole.role);
      } catch {}
      finally { setIsLoading(false); }
    })();
  }, []);

  const handleGenerate = async () => {
    setIsGenerating(true);
    await new Promise(r => setTimeout(r, 1800));

    const evidence = profile?.structured_evidence || {};
    const skills = Array.isArray(evidence.skills) ? evidence.skills : Object.values(evidence.skills || {}).flat();
    const exp = evidence.experience || [];
    const name = evidence.contact_info?.name || "Developer";
    const role = targetRole || "Software Engineer";
    const topSkills = skills.slice(0, 4).join(", ") || "Python, Backend, APIs";
    const company = exp[0]?.company || "a tech company";
    const years = exp.length;

    const toneAdj = tone === "casual" ? "I build" : tone === "creative" ? "⚡ Building" : "Experienced";

    setBranding({
      linkedin: {
        headline: `${role} · ${topSkills.split(", ").slice(0, 2).join(" & ")} Engineer · Building scalable systems`,
        about: `${toneAdj} backend systems and APIs at ${company}. Experienced across ${topSkills}. ${years > 1 ? `${years}+ years building production-grade software. ` : ""}Currently seeking roles in ${role.toLowerCase()} and ${skills[1] || "distributed systems"}.\n\nLet's connect if you're working on challenging engineering problems.`,
        summary_tips: [
          "Start with your strongest skill or recent achievement",
          `Include: ${skills.slice(0, 3).join(", ")} in your featured section`,
          "Add your GitHub link as a custom URL on your profile",
          "Use LinkedIn's 'Open to Work' for backend/AI roles selectively",
        ],
      },
      github: {
        bio: `${role} · ${topSkills.split(", ").slice(0, 2).join(" & ")} · ${tone === "casual" ? "Building cool stuff" : "Building production-grade systems"}`,
        profile_readme: `## Hi, I'm ${name} 👋\n\n${toneAdj} backend systems and intelligent software. Currently focused on ${role.toLowerCase()}.\n\n**Tech Stack:** ${skills.slice(0,6).join(" · ")}\n\n**Currently:** Looking for ${role} opportunities\n\n[![GitHub](https://img.shields.io/badge/Open%20to%20Work-6366f1)](${evidence.contact_info?.linkedin || "#"})`,
        pinned_tip: `Pin your most technically complex project. Recruiters look at this first.`,
        readme_tip: `Your GitHub README is your second resume. Keep it updated.`,
      },
      portfolio: {
        hero_tagline: `${role} who builds ${topSkills.split(", ")[0]} systems at scale`,
        about_blurb: `I specialize in ${topSkills.split(", ").slice(0,3).join(", ")}. My work focuses on building reliable, performant, and maintainable software that solves real problems.`,
        projects_cta: `Featured Projects — where engineering meets impact`,
        contact_cta: `Available for ${role} roles · ${tone === "casual" ? "Let's chat" : "Schedule a call"}`,
      },
      twitter: {
        bio: `${role} · ${topSkills.split(", ")[0]} engineer · ${tone === "casual" ? "writing code and threads" : "building in public"} · ${evidence.contact_info?.linkedin ? "LinkedIn ↓" : "Open to work"}`,
        pinned_tweet_idea: `"Just published: How I built [your project] with ${topSkills.split(", ")[0]} — a technical breakdown thread 🧵"`,
        posting_strategy: [
          "Post 1–2 technical threads per week about problems you've solved",
          `Share ${skills[0] || "backend"} tips — this attracts engineering recruiters`,
          "Engage with engineering leaders at your target companies",
        ],
      },
    });
    setGenerated(true);
    setIsGenerating(false);
  };

  if (isLoading) return (
    <div className="flex h-[70vh] items-center justify-center flex-col gap-4">
      <Spinner size="lg" color="indigo" />
      <span className="text-xs text-slate-500 font-bold uppercase tracking-widest animate-pulse">Loading Branding Engine...</span>
    </div>
  );

  const evidence = profile?.structured_evidence || {};
  const skills = Array.isArray(evidence.skills) ? evidence.skills : Object.values(evidence.skills || {}).flat();
  const name = evidence.contact_info?.name || "Your Name";
  const b = branding || {};

  return (
    <div className="flex flex-col gap-7 w-full pb-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-100 tracking-tight">Personal Branding</h1>
          <p className="text-sm text-slate-500 mt-0.5">LinkedIn · GitHub · Portfolio · Twitter — optimized from your evidence</p>
        </div>
        <Link href="/tailor">
          <button className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-bold shadow-lg hover:scale-105 transition-all">
            ⚡ Tailor Resume
          </button>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Config Panel */}
        <GCard className="p-5 flex flex-col gap-5 lg:col-span-1">
          <h3 className="text-sm font-bold text-slate-200">Branding Setup</h3>

          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">Target Role</label>
            <input value={targetRole} onChange={e => setTargetRole(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-800 border border-slate-700 text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              placeholder="e.g. Backend Engineer" />
          </div>

          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5 block">Brand Tone</label>
            <div className="flex flex-col gap-1.5">
              {[
                { id: "professional", label: "🤝 Professional", desc: "Corporate, authoritative" },
                { id: "casual",       label: "😊 Casual", desc: "Friendly, approachable" },
                { id: "creative",     label: "✨ Creative", desc: "Bold, energetic" },
              ].map(t => (
                <div key={t.id} onClick={() => setTone(t.id)}
                  className={`px-3.5 py-2.5 rounded-xl border cursor-pointer transition-all ${tone === t.id ? "border-indigo-500 bg-indigo-500/8" : "border-slate-700 hover:border-slate-600"}`}>
                  <div className="text-sm font-semibold text-slate-200">{t.label}</div>
                  <div className="text-xs text-slate-500">{t.desc}</div>
                </div>
              ))}
            </div>
          </div>

          <button onClick={handleGenerate} disabled={isGenerating}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-bold disabled:opacity-50 hover:scale-[1.02] transition-all shadow-lg shadow-indigo-500/20">
            {isGenerating ? (
              <span className="flex items-center justify-center gap-2">
                <div className="w-3.5 h-3.5 border border-white/30 border-t-white rounded-full animate-spin" /> Generating...
              </span>
            ) : generated ? "🔄 Regenerate" : "✨ Generate Branding"}
          </button>

          {/* Profile Evidence Preview */}
          <div className="border-t border-slate-700/40 pt-4">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Your Evidence</h4>
            <div className="text-sm font-bold text-slate-300 mb-1">{name}</div>
            <div className="flex flex-wrap gap-1">
              {skills.slice(0, 6).map((s, i) => (
                <span key={i} className="px-2 py-0.5 rounded-lg bg-slate-800 text-slate-400 text-xs border border-slate-700">{s}</span>
              ))}
              {skills.length === 0 && <p className="text-xs text-slate-600">Upload resume to load evidence.</p>}
            </div>
          </div>
        </GCard>

        {/* Branding Output */}
        <div className="lg:col-span-3 flex flex-col gap-4">
          {/* Platform Tabs */}
          <div className="flex gap-2 flex-wrap">
            {PLATFORM_TABS.map(p => (
              <button key={p} onClick={() => setActivePlatform(p)}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-xl border text-xs font-bold transition-all ${
                  activePlatform === p ? "bg-indigo-500/15 border-indigo-500/30 text-indigo-400" : "border-slate-700 text-slate-500 hover:border-slate-600 hover:text-slate-400"
                }`}>
                {PLATFORM_ICONS[p]} {p}
              </button>
            ))}
          </div>

          {/* Empty state */}
          {!generated && (
            <GCard className="p-12 flex flex-col items-center justify-center gap-4 text-center">
              <div className="w-16 h-16 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-3xl">✨</div>
              <div>
                <h3 className="text-lg font-bold text-slate-300 mb-1">Generate Your Personal Brand</h3>
                <p className="text-sm text-slate-500 max-w-sm">Configure your target role and tone on the left, then click Generate to create optimized branding across all platforms.</p>
              </div>
              <button onClick={handleGenerate} disabled={isGenerating}
                className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-sm font-bold hover:scale-105 transition-all shadow-lg shadow-indigo-500/20 disabled:opacity-50">
                {isGenerating ? "Generating..." : "✨ Generate Now"}
              </button>
            </GCard>
          )}

          {/* LinkedIn */}
          {generated && activePlatform === "LinkedIn" && b.linkedin && (
            <div className="flex flex-col gap-4">
              <GCard className="p-5">
                <h3 className="text-sm font-bold text-slate-200 mb-4 flex items-center gap-2">🔗 LinkedIn Optimization</h3>
                <div className="flex flex-col gap-4">
                  <BrandingCard icon="💼" title="Headline" content={b.linkedin.headline} accent="indigo" />
                  <BrandingCard icon="📝" title="About / Summary" content={b.linkedin.about} accent="teal" />
                  <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/40">
                    <h4 className="text-xs font-bold text-amber-400 uppercase tracking-widest mb-3">💡 Profile Optimization Tips</h4>
                    <ul className="flex flex-col gap-2">
                      {b.linkedin.summary_tips?.map((tip, i) => (
                        <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                          <span className="text-indigo-400 font-bold flex-shrink-0">{i + 1}.</span> {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </GCard>
            </div>
          )}

          {/* GitHub */}
          {generated && activePlatform === "GitHub" && b.github && (
            <div className="flex flex-col gap-4">
              <GCard className="p-5">
                <h3 className="text-sm font-bold text-slate-200 mb-4 flex items-center gap-2">🐙 GitHub Profile Optimization</h3>
                <div className="flex flex-col gap-4">
                  <BrandingCard icon="📌" title="Profile Bio" content={b.github.bio} accent="purple" />
                  <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/40">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-xs font-bold text-purple-400 uppercase tracking-widest">Profile README.md</h4>
                      <CopyButton text={b.github.profile_readme} />
                    </div>
                    <pre className="text-xs text-slate-300 whitespace-pre-wrap font-mono leading-relaxed bg-slate-900/60 rounded-lg p-3 overflow-x-auto">{b.github.profile_readme}</pre>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700/30">
                      <div className="text-xs font-bold text-teal-400 mb-1.5">📌 Pinned Repos</div>
                      <p className="text-xs text-slate-400">{b.github.pinned_tip}</p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700/30">
                      <div className="text-xs font-bold text-indigo-400 mb-1.5">📖 README Strategy</div>
                      <p className="text-xs text-slate-400">{b.github.readme_tip}</p>
                    </div>
                  </div>
                </div>
              </GCard>
            </div>
          )}

          {/* Portfolio */}
          {generated && activePlatform === "Portfolio" && b.portfolio && (
            <GCard className="p-5 flex flex-col gap-4">
              <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">🌐 Portfolio Copy</h3>
              <BrandingCard icon="🎯" title="Hero Tagline" content={b.portfolio.hero_tagline} accent="sky" />
              <BrandingCard icon="👤" title="About Section" content={b.portfolio.about_blurb} accent="teal" />
              <BrandingCard icon="🚀" title="Projects Section Header" content={b.portfolio.projects_cta} accent="indigo" />
              <BrandingCard icon="📬" title="Contact CTA" content={b.portfolio.contact_cta} accent="amber" />
            </GCard>
          )}

          {/* Twitter/X */}
          {generated && activePlatform === "Twitter/X" && b.twitter && (
            <GCard className="p-5 flex flex-col gap-4">
              <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2">🐦 Twitter/X Strategy</h3>
              <BrandingCard icon="📌" title="Bio (max 160 chars)" content={b.twitter.bio} accent="sky" />
              <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/40">
                <h4 className="text-xs font-bold text-sky-400 uppercase tracking-widest mb-2">📌 Pinned Tweet Idea</h4>
                <p className="text-sm text-slate-300 italic">"{b.twitter.pinned_tweet_idea}"</p>
              </div>
              <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/40">
                <h4 className="text-xs font-bold text-amber-400 uppercase tracking-widest mb-3">📊 Content Strategy</h4>
                <ul className="flex flex-col gap-2">
                  {b.twitter.posting_strategy?.map((tip, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                      <span className="text-amber-400 font-bold flex-shrink-0">→</span> {tip}
                    </li>
                  ))}
                </ul>
              </div>
            </GCard>
          )}
        </div>
      </div>
    </div>
  );
}
