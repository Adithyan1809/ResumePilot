"use client";

import React from "react";
import Link from "next/link";
import { useAuth } from "../contexts/AuthContext";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import Navbar from "../components/layout/Navbar";

/**
 * Premium SaaS Landing Page.
 */
export default function LandingPage() {
  const { user } = useAuth();

  const features = [
    {
      title: "Grok 3 AI Engine",
      description:
        "Powered by xAI's elite Grok models. Intelligently tailors summaries, experience bullets, and skills alignment.",
      icon: (
        <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
    },
    {
      title: "ATS Score Compatibility",
      description:
        "Evaluate your resume across 7 distinct dimensions including TF-IDF keyword overlap, action verbs, and achievements.",
      icon: (
        <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
    },
    {
      title: "Actionable suggestions",
      description:
        "Get a prioritized, step-by-step career checklist to format issues, optimize keywords, and boost response rates.",
      icon: (
        <svg className="w-6 h-6 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      ),
    },
    {
      title: "ATS-Friendly Templates",
      description:
        "Export beautiful Classic, Modern, and Executive layouts that open cleanly on both PDF and DOCX parsers.",
      icon: (
        <svg className="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
      ),
    },
    {
      title: "Diff Highlights Reviewer",
      description:
        "Scan changes side-by-side. Our split view explicitly highlights new keywords, rephrasings, and additions.",
      icon: (
        <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
        </svg>
      ),
    },
    {
      title: "Cover Letter Generator",
      description:
        "Auto-draft tailored cover letters corresponding directly to the target role with professional, conversational, or enthusiastic tones.",
      icon: (
        <svg className="w-6 h-6 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
    },
  ];

  return (
    <div className="min-h-screen bg-[#020617] text-slate-100 relative overflow-hidden flex flex-col justify-between">
      {/* Dynamic background lights */}
      <div className="absolute top-0 left-1/4 -translate-x-1/2 w-[45rem] h-[45rem] rounded-full bg-indigo-500/5 blur-[120px] pointer-events-none" />
      <div className="absolute top-1/3 right-1/4 translate-x-1/2 w-[35rem] h-[35rem] rounded-full bg-purple-500/5 blur-[100px] pointer-events-none" />
      
      <div className="relative z-10">
        {/* Navigation Navbar */}
        <Navbar />

        {/* Hero Section */}
        <section className="max-w-7xl mx-auto px-6 pt-20 md:pt-32 pb-24 text-center flex flex-col items-center gap-8">
          {/* Badge accent */}
          <Badge variant="indigo" className="py-1 px-4 text-xs shadow-md border-indigo-500/25">
            ⚡ Powered by Grok AI Engine
          </Badge>

          <h2 className="text-4xl md:text-6xl font-black tracking-tight leading-tight max-w-4xl bg-gradient-to-r from-slate-100 via-slate-200 to-slate-400 bg-clip-text text-transparent">
            Optimize your resume for ATS <br />
            and tailor it in seconds with AI
          </h2>

          <p className="text-sm md:text-lg text-slate-400 max-w-2xl leading-relaxed">
            Stop sending generic applications. Tailor your work experience, reorder skills, match key terms, and get comprehensive ATS audits to secure more interviews.
          </p>

          {/* Action buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mt-4">
            <Link href={user ? "/dashboard" : "/signup"}>
              <Button variant="gradient" size="lg" className="w-full sm:w-auto font-bold shadow-xl">
                {user ? "Go to Dashboard" : "Get Started for Free"}
              </Button>
            </Link>
            <a href="#features">
              <Button variant="outline" size="lg" className="w-full sm:w-auto font-semibold">
                Explore Features
              </Button>
            </a>
          </div>

          {/* Double floating dashboard previews mockup */}
          <div className="w-full max-w-4xl mt-12 rounded-3xl border border-slate-800/80 bg-slate-950/40 p-4 backdrop-blur-sm shadow-2xl relative">
            <div className="absolute inset-x-0 -top-px h-px bg-gradient-to-r from-transparent via-indigo-500/40 to-transparent" />
            
            {/* Header circles */}
            <div className="flex gap-1.5 pb-4 pl-2 border-b border-slate-850">
              <div className="w-3 h-3 rounded-full bg-slate-800" />
              <div className="w-3 h-3 rounded-full bg-slate-800" />
              <div className="w-3 h-3 rounded-full bg-slate-800" />
            </div>

            {/* Grid preview mock */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-6 p-2 text-left">
              <Card variant="outline" className="p-5 border-slate-850 flex flex-col gap-3">
                <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center font-bold text-indigo-400 text-xs">
                  84%
                </div>
                <h5 className="font-bold text-slate-200 text-sm">ATS Scored Matching</h5>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Real-time matching audits scanning keyword frequency, formatting parsing, and achievements.
                </p>
              </Card>

              <Card variant="outline" className="p-5 border-slate-850 flex flex-col gap-3">
                <div className="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center font-bold text-purple-400 text-xs">
                  AI
                </div>
                <h5 className="font-bold text-slate-200 text-sm">Smart Bullet Rephrase</h5>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Converts passive roles into metrics-quantified, high-impact accomplishments automatically.
                </p>
              </Card>

              <Card variant="outline" className="p-5 border-slate-850 flex flex-col gap-3">
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center font-bold text-emerald-400 text-xs">
                  Doc
                </div>
                <h5 className="font-bold text-slate-200 text-sm">Dual Format Export</h5>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Render to beautiful, perfectly formatted, print-optimized PDF or standard Word DOCX files.
                </p>
              </Card>
            </div>
          </div>
        </section>

        {/* Features Showcase Grid Section */}
        <section id="features" className="max-w-7xl mx-auto px-6 py-24 border-t border-slate-900 flex flex-col gap-12">
          <div className="text-center flex flex-col gap-3">
            <h3 className="text-3xl font-black text-slate-100 tracking-tight">
              SaaS Capabilities
            </h3>
            <p className="text-sm text-slate-500 font-semibold uppercase tracking-wider">
              Complete tools to optimize your career path
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feat, idx) => (
              <Card
                key={idx}
                variant="interactive"
                className="p-6 md:p-8 flex flex-col gap-4"
              >
                {/* Icon wrapper */}
                <div className="w-12 h-12 rounded-xl bg-slate-950/80 border border-slate-800 flex items-center justify-center">
                  {feat.icon}
                </div>
                <h4 className="text-lg font-bold text-slate-200">{feat.title}</h4>
                <p className="text-sm text-slate-400 leading-relaxed">
                  {feat.description}
                </p>
              </Card>
            ))}
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="w-full border-t border-slate-900/60 bg-slate-950/40 py-8 relative z-10">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4 text-xs font-semibold text-slate-500">
          <span>&copy; {new Date().getFullYear()} ResumeAI Inc. All rights reserved.</span>
          <div className="flex gap-6 uppercase tracking-wider text-[10px]">
            <a href="#" className="hover:text-slate-300">Privacy Policy</a>
            <a href="#" className="hover:text-slate-300">Terms of Service</a>
            <a href="#" className="hover:text-slate-300">Support</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
