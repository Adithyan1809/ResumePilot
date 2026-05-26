"use client";

import React, { useRef } from "react";
import Link from "next/link";
import { useAuth } from "../contexts/AuthContext";
import {
  motion,
  useScroll,
  useTransform,
  useInView,
} from "framer-motion";
import {
  Brain,
  BarChart3,
  Eye,
  TrendingUp,
  MessageSquare,
  ShieldCheck,
  Sparkles,
  ArrowRight,
  ChevronRight,
  Zap,
  Play,
} from "lucide-react";

/* ═══════════════════════════════════════════════════════════════════════
   DATA
   ═══════════════════════════════════════════════════════════════════════ */

const NAV_LINKS = ["Features", "Intelligence", "Pricing"];

const FEATURES = [
  {
    icon: Brain,
    title: "Evidence Graph Engine",
    description:
      "Maps every claim in your resume to concrete evidence — metrics, projects, and accomplishments — eliminating unsubstantiated assertions.",
    color: "text-indigo-400",
    bg: "bg-indigo-500/10",
  },
  {
    icon: BarChart3,
    title: "ATS Simulation",
    description:
      "Runs your resume through 75+ real-world ATS parsing engines, scoring keyword density, formatting compliance, and section hierarchy.",
    color: "text-purple-400",
    bg: "bg-purple-500/10",
  },
  {
    icon: Eye,
    title: "Recruiter Simulation",
    description:
      "Simulates the 6-second recruiter scan pattern. Heatmap overlays reveal exactly what gets noticed — and what gets skipped.",
    color: "text-violet-400",
    bg: "bg-violet-500/10",
  },
  {
    icon: TrendingUp,
    title: "Career Intelligence",
    description:
      "Analyzes market trajectory, salary benchmarks, and role transitions to position your narrative for maximum career velocity.",
    color: "text-cyan-400",
    bg: "bg-cyan-500/10",
  },
  {
    icon: MessageSquare,
    title: "Interview Readiness",
    description:
      "Generates probable interview questions from your resume content and prepares evidence-backed talking points for each.",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
  },
  {
    icon: ShieldCheck,
    title: "Zero Hallucination",
    description:
      "Every suggestion is grounded in your actual experience. No fabricated metrics, no invented achievements, no embellished claims.",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
  },
];

const STATS = [
  { value: "75+", label: "AI Engines" },
  { value: "6-Stage", label: "Pipeline" },
  { value: "Zero", label: "Hallucinations" },
  { value: "Recruiter", label: "Grade Output" },
];

const MARQUEE_ITEMS = [
  "ATS Optimization",
  "Evidence Grounding",
  "Career Mapping",
  "Recruiter Simulation",
  "Metric Realism",
  "Voice Preservation",
  "Story Flow",
  "Project Ranking",
];

const BROWSER_CARDS = [
  {
    label: "94%",
    title: "ATS Match Score",
    desc: "Real-time keyword and formatting compliance across 75+ parsing engines.",
    accent: "text-indigo-400",
    accentBg: "bg-indigo-500/10",
  },
  {
    label: "AI",
    title: "Evidence Engine",
    desc: "Maps every bullet to measurable outcomes — no unsubstantiated claims.",
    accent: "text-purple-400",
    accentBg: "bg-purple-500/10",
  },
  {
    label: "6s",
    title: "Recruiter Scan",
    desc: "Simulates the recruiter heatmap to optimize visual hierarchy and flow.",
    accent: "text-cyan-400",
    accentBg: "bg-cyan-500/10",
  },
];

/* ═══════════════════════════════════════════════════════════════════════
   ANIMATION VARIANTS
   ═══════════════════════════════════════════════════════════════════════ */

const spring = { type: "spring", stiffness: 100, damping: 30 };

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.7, ease: [0.16, 1, 0.3, 1] },
  }),
};

const staggerContainer = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.08, delayChildren: 0.1 },
  },
};

const wordReveal = {
  hidden: { opacity: 0, y: 20, filter: "blur(8px)" },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: {
      delay: 0.3 + i * 0.1,
      duration: 0.8,
      ease: [0.16, 1, 0.3, 1],
    },
  }),
};

/* ═══════════════════════════════════════════════════════════════════════
   HELPERS
   ═══════════════════════════════════════════════════════════════════════ */

function AnimatedWords({ text, className }) {
  const words = text.split(" ");
  return (
    <span className={className}>
      {words.map((word, i) => (
        <motion.span
          key={i}
          custom={i}
          variants={wordReveal}
          initial="hidden"
          animate="visible"
          className="inline-block mr-[0.3em]"
        >
          {word}
        </motion.span>
      ))}
    </span>
  );
}

function FeatureCard({ feature, index }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-60px" });
  const Icon = feature.icon;

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
      transition={{
        delay: index * 0.08,
        duration: 0.7,
        ease: [0.16, 1, 0.3, 1],
      }}
      className="glass-card rounded-2xl p-6 md:p-8 flex flex-col gap-5 group"
    >
      <div
        className={`w-12 h-12 rounded-xl ${feature.bg} flex items-center justify-center transition-transform duration-500 group-hover:scale-110`}
      >
        <Icon className={`w-6 h-6 ${feature.color}`} strokeWidth={1.8} />
      </div>
      <h4 className="text-lg font-semibold text-zinc-100 tracking-tight">
        {feature.title}
      </h4>
      <p className="text-sm text-zinc-400 leading-relaxed">
        {feature.description}
      </p>
    </motion.div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════
   LANDING PAGE
   ═══════════════════════════════════════════════════════════════════════ */

export default function LandingPage() {
  const { user } = useAuth();
  const containerRef = useRef(null);

  /* ── Scroll-reactive navbar ────────────────────────────────────────── */
  const { scrollY } = useScroll();
  const navBg = useTransform(
    scrollY,
    [0, 80],
    ["rgba(9,9,11,0)", "rgba(9,9,11,0.85)"]
  );
  const navBlur = useTransform(scrollY, [0, 80], ["blur(0px)", "blur(20px)"]);
  const navBorder = useTransform(
    scrollY,
    [0, 80],
    ["rgba(63,63,70,0)", "rgba(63,63,70,0.4)"]
  );

  /* ── Hero section scroll effects ───────────────────────────────────── */
  const heroRef = useRef(null);
  const { scrollYProgress: heroProgress } = useScroll({
    target: heroRef,
    offset: ["start start", "end start"],
  });
  const heroOpacity = useTransform(heroProgress, [0, 0.5], [1, 0]);
  const heroScale = useTransform(heroProgress, [0, 0.5], [1, 0.97]);
  const heroY = useTransform(heroProgress, [0, 0.5], [0, 60]);

  return (
    <div
      ref={containerRef}
      className="min-h-screen bg-[#09090b] text-zinc-100 relative overflow-x-hidden"
    >
      {/* ══════════════════════════════════════════════════════════════════
          SECTION 1 — NAVBAR
          ══════════════════════════════════════════════════════════════════ */}
      <motion.nav
        style={{
          backgroundColor: navBg,
          backdropFilter: navBlur,
          WebkitBackdropFilter: navBlur,
          borderBottomColor: navBorder,
        }}
        className="fixed top-0 inset-x-0 z-50 border-b border-transparent"
      >
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center group-hover:bg-indigo-500/20 transition-colors duration-300">
              <Sparkles className="w-4 h-4 text-indigo-400" strokeWidth={2} />
            </div>
            <span className="text-lg font-bold tracking-tight text-zinc-100">
              Resume<span className="text-indigo-400">Pilot</span>
            </span>
          </Link>

          {/* Nav links */}
          <div className="hidden md:flex items-center gap-8">
            {NAV_LINKS.map((link) => (
              <a
                key={link}
                href={`#${link.toLowerCase()}`}
                className="text-sm text-zinc-400 hover:text-zinc-100 transition-colors duration-300 tracking-wide"
              >
                {link}
              </a>
            ))}
          </div>

          {/* Auth buttons */}
          <div className="flex items-center gap-3">
            {user ? (
              <Link
                href="/dashboard"
                className="btn-gradient px-5 py-2 rounded-lg text-sm font-semibold text-white"
              >
                <span className="flex items-center gap-2">
                  Dashboard <ArrowRight className="w-4 h-4" />
                </span>
              </Link>
            ) : (
              <>
                <Link
                  href="/login"
                  className="text-sm text-zinc-400 hover:text-zinc-100 transition-colors duration-300 px-4 py-2"
                >
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  className="btn-gradient px-5 py-2 rounded-lg text-sm font-semibold text-white"
                >
                  <span className="flex items-center gap-2">
                    Get Started <ChevronRight className="w-4 h-4" />
                  </span>
                </Link>
              </>
            )}
          </div>
        </div>
      </motion.nav>

      {/* ══════════════════════════════════════════════════════════════════
          SECTION 2 — CINEMATIC HERO
          ══════════════════════════════════════════════════════════════════ */}
      <section ref={heroRef} className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden">
        {/* Background orbs */}
        <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
          <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 w-[40rem] h-[40rem] rounded-full bg-indigo-500/[0.07] blur-[120px]" />
          <div className="absolute top-1/3 right-1/4 translate-x-1/2 w-[35rem] h-[35rem] rounded-full bg-purple-500/[0.05] blur-[120px]" />
          <div className="absolute bottom-1/4 left-1/2 -translate-x-1/2 w-[30rem] h-[30rem] rounded-full bg-cyan-500/[0.04] blur-[120px]" />
        </div>

        <motion.div
          style={{ opacity: heroOpacity, scale: heroScale, y: heroY }}
          className="relative z-10 max-w-5xl mx-auto px-6 pt-32 pb-20 flex flex-col items-center text-center gap-8"
        >
          {/* Chip */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            className="flex items-center gap-2 px-4 py-1.5 rounded-full glass text-xs font-medium text-zinc-300 tracking-wide"
          >
            <Zap className="w-3.5 h-3.5 text-indigo-400" />
            <span>AI-Powered Employability Intelligence</span>
          </motion.div>

          {/* Headline */}
          <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight leading-[1.05] gradient-text-hero">
            <AnimatedWords text="AI Employability" />
            <br />
            <AnimatedWords text="Intelligence Infrastructure" />
          </h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
            className="text-base md:text-lg text-zinc-400 max-w-2xl leading-relaxed"
          >
            The complete career intelligence platform. Simulate ATS engines,
            ground every claim in evidence, and build recruiter-grade resumes
            with zero hallucinations.
          </motion.p>

          {/* CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1, duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
            className="flex flex-col sm:flex-row gap-4 mt-2"
          >
            <Link
              href={user ? "/dashboard" : "/signup"}
              className="btn-gradient px-8 py-3.5 rounded-xl text-sm font-semibold text-white glow-primary"
            >
              <span className="flex items-center gap-2.5">
                Launch Dashboard
                <ArrowRight className="w-4 h-4" />
              </span>
            </Link>
            <button className="flex items-center gap-2.5 px-8 py-3.5 rounded-xl text-sm font-semibold text-zinc-300 border border-zinc-800 hover:border-zinc-700 hover:text-zinc-100 transition-all duration-300 bg-transparent">
              <Play className="w-4 h-4 text-indigo-400" />
              Watch Demo
            </button>
          </motion.div>

          {/* Browser window mock */}
          <motion.div
            initial={{ opacity: 0, y: 40, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ delay: 1.3, duration: 1, ease: [0.16, 1, 0.3, 1] }}
            className="w-full max-w-4xl mt-16 rounded-2xl border border-zinc-800/80 bg-zinc-950/60 backdrop-blur-sm shadow-2xl relative overflow-hidden"
          >
            {/* Top edge glow */}
            <div className="absolute inset-x-0 -top-px h-px bg-gradient-to-r from-transparent via-indigo-500/40 to-transparent" />

            {/* Browser chrome */}
            <div className="flex items-center gap-2 px-5 py-4 border-b border-zinc-800/60">
              <div className="w-3 h-3 rounded-full bg-zinc-800" />
              <div className="w-3 h-3 rounded-full bg-zinc-800" />
              <div className="w-3 h-3 rounded-full bg-zinc-800" />
              <div className="flex-1 mx-4 h-7 rounded-lg bg-zinc-900/80 border border-zinc-800/50 flex items-center px-3">
                <span className="text-[11px] text-zinc-600 font-mono">
                  resumepilot.ai/dashboard
                </span>
              </div>
            </div>

            {/* Feature cards inside browser */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6">
              {BROWSER_CARDS.map((card, i) => (
                <motion.div
                  key={card.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    delay: 1.6 + i * 0.12,
                    duration: 0.7,
                    ease: [0.16, 1, 0.3, 1],
                  }}
                  className="glass-card rounded-xl p-5 flex flex-col gap-3 text-left"
                >
                  <div
                    className={`w-9 h-9 rounded-lg ${card.accentBg} flex items-center justify-center font-bold ${card.accent} text-xs`}
                  >
                    {card.label}
                  </div>
                  <h5 className="font-semibold text-zinc-200 text-sm">
                    {card.title}
                  </h5>
                  <p className="text-xs text-zinc-500 leading-relaxed">
                    {card.desc}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          SECTION 3 — FEATURE SHOWCASE
          ══════════════════════════════════════════════════════════════════ */}
      <section
        id="features"
        className="relative max-w-7xl mx-auto px-6 py-32"
      >
        {/* Section header */}
        <div className="text-center mb-20">
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-xs font-semibold uppercase tracking-[0.2em] text-indigo-400 mb-4"
          >
            Capabilities
          </motion.p>
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
            className="text-3xl md:text-5xl font-bold tracking-tight gradient-text-hero"
          >
            Everything you need.
            <br />
            Nothing you don&apos;t.
          </motion.h2>
        </div>

        {/* 3×2 grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((feature, index) => (
            <FeatureCard key={feature.title} feature={feature} index={index} />
          ))}
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          SECTION 4 — STATS BAR
          ══════════════════════════════════════════════════════════════════ */}
      <section className="relative py-20 border-y border-zinc-800/50">
        <div className="glass max-w-6xl mx-auto rounded-2xl px-6 py-12 md:py-16">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-40px" }}
            variants={staggerContainer}
            className="grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {STATS.map((stat, i) => (
              <motion.div
                key={stat.label}
                variants={fadeUp}
                custom={i}
                className="flex flex-col items-center text-center gap-2"
              >
                <span className="text-3xl md:text-4xl font-bold gradient-text-accent tracking-tight">
                  {stat.value}
                </span>
                <span className="text-sm text-zinc-400 font-medium tracking-wide">
                  {stat.label}
                </span>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          SECTION 5 — TRUST MARQUEE
          ══════════════════════════════════════════════════════════════════ */}
      <section className="relative py-20 overflow-hidden">
        <div className="mb-10 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-zinc-500">
            Intelligence Stack
          </p>
        </div>

        {/* Gradient edge masks */}
        <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-[#09090b] to-transparent z-10 pointer-events-none" />
        <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-[#09090b] to-transparent z-10 pointer-events-none" />

        <div className="flex overflow-hidden">
          <div className="flex animate-marquee whitespace-nowrap">
            {[...MARQUEE_ITEMS, ...MARQUEE_ITEMS].map((item, i) => (
              <span
                key={i}
                className="mx-4 inline-flex items-center gap-2 px-6 py-3 rounded-full border border-zinc-800 bg-zinc-950/60 text-sm text-zinc-300 font-medium whitespace-nowrap"
              >
                <Sparkles className="w-3.5 h-3.5 text-indigo-400/70" />
                {item}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          SECTION 6 — FINAL CTA
          ══════════════════════════════════════════════════════════════════ */}
      <section className="relative py-32 overflow-hidden">
        {/* Aurora background */}
        <div
          className="absolute inset-0 gradient-aurora opacity-[0.06] pointer-events-none"
          aria-hidden="true"
        />
        <div className="absolute inset-0 bg-[#09090b]/60 pointer-events-none" aria-hidden="true" />

        <div className="relative z-10 max-w-4xl mx-auto px-6 text-center flex flex-col items-center gap-8">
          <motion.h2
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight gradient-text-hero leading-[1.1]"
          >
            Build Your
            <br />
            Engineering Future
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{
              delay: 0.15,
              duration: 0.7,
              ease: [0.16, 1, 0.3, 1],
            }}
            className="text-base md:text-lg text-zinc-400 max-w-xl leading-relaxed"
          >
            Join thousands of engineers who&apos;ve transformed their career
            trajectory with recruiter-grade, evidence-backed resumes.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{
              delay: 0.3,
              duration: 0.7,
              ease: [0.16, 1, 0.3, 1],
            }}
          >
            <Link
              href={user ? "/dashboard" : "/signup"}
              className="btn-gradient px-10 py-4 rounded-xl text-base font-semibold text-white glow-primary inline-flex items-center gap-3"
            >
              <span className="flex items-center gap-2.5">
                Get Started — It&apos;s Free
                <ArrowRight className="w-5 h-5" />
              </span>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════════
          SECTION 7 — FOOTER
          ══════════════════════════════════════════════════════════════════ */}
      <footer className="border-t border-zinc-800/50 py-10">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-zinc-500">
          <span className="font-medium">
            &copy; 2026 ResumePilot. All rights reserved.
          </span>
          <div className="flex gap-6 text-zinc-500">
            <a
              href="#"
              className="hover:text-zinc-300 transition-colors duration-300"
            >
              Privacy
            </a>
            <a
              href="#"
              className="hover:text-zinc-300 transition-colors duration-300"
            >
              Terms
            </a>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-zinc-300 transition-colors duration-300"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
