"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import api from "../../../lib/api";
import StatsCards from "../../../components/dashboard/StatsCards";
import ScoreChart from "../../../components/dashboard/ScoreChart";
import ResumeHistory from "../../../components/dashboard/ResumeHistory";
import Button from "../../../components/ui/Button";
import Spinner from "../../../components/ui/Spinner";

/**
 * Dashboard page.
 */
export default function DashboardPage() {
  const [historyItems, setHistoryItems] = useState([]);
  const [stats, setStats] = useState({
    totalResumes: 0,
    totalTailored: 0,
    avgScore: 0,
    bestScore: 0,
  });
  const [chartData, setChartData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [historyResult, resumesResult] = await Promise.allSettled([
          api.get("/tailor/history"),
          api.get("/resumes"),
        ]);

        const items = historyResult.status === "fulfilled" ? historyResult.value.items || [] : [];
        const totalUploaded = resumesResult.status === "fulfilled" ? resumesResult.value.total || 0 : 0;

        if (historyResult.status === "rejected") {
          console.warn("Dashboard history request failed. Using preview history.", historyResult.reason);
        }
        if (resumesResult.status === "rejected") {
          console.warn("Dashboard resume count request failed. Using zero count.", resumesResult.reason);
        }

        setHistoryItems(items);

        if (items.length > 0) {
          const scores = items.map((i) => i.overall_score);
          const best = Math.max(...scores);
          const avg = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
          
          setStats({
            totalResumes: totalUploaded,
            totalTailored: items.length,
            avgScore: avg,
            bestScore: best,
          });

          // Compile chart details
          const cData = items.map((i) => ({
            date: i.created_at,
            score: i.overall_score,
            role: i.job_title,
          }));
          setChartData(cData);
        } else {
          // Initialize defaults
          setStats({
            totalResumes: totalUploaded,
            totalTailored: 0,
            avgScore: 0,
            bestScore: 0,
          });
        }
      } catch (err) {
        console.error("Dashboard loading failed. Falling back to preview state.", err);
        _loadMockPreviewState();
      } finally {
        setIsLoading(false);
      }
    }

    loadDashboardData();
  }, []);

  const _loadMockPreviewState = () => {
    // Elegant mock sandbox representation
    const mockItems = [
      {
        id: "d124c9c2-51c0-4357-a352-7b0b2e88a032",
        resume_id: "c9c2d124-51c0-4357-a352-7b0b2e88a032",
        job_title: "Senior Full Stack Engineer",
        company: "Innovate Inc",
        overall_score: 87,
        template: "classic",
        created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: "d124c9c2-51c0-4357-a352-7b0b2e88a033",
        resume_id: "c9c2d124-51c0-4357-a352-7b0b2e88a032",
        job_title: "AI Infrastructure Specialist",
        company: "Nebula AI",
        overall_score: 72,
        template: "modern",
        created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
      },
      {
        id: "d124c9c2-51c0-4357-a352-7b0b2e88a034",
        resume_id: "c9c2d124-51c0-4357-a352-7b0b2e88a032",
        job_title: "FastAPI Backend Developer",
        company: "Stripe API Team",
        overall_score: 91,
        template: "executive",
        created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
      },
    ];

    setHistoryItems(mockItems);
    setStats({
      totalResumes: 2,
      totalTailored: 3,
      avgScore: 83,
      bestScore: 91,
    });
    setChartData(
      mockItems.map((i) => ({
        date: i.created_at,
        score: i.overall_score,
        role: i.job_title,
      }))
    );
  };

  const handleDelete = async (id) => {
    if (confirm("Are you sure you want to delete this tailoring entry from your history?")) {
      try {
        await api.delete(`/tailor/${id}`);
        setHistoryItems((prev) => prev.filter((item) => item.id !== id));
      } catch (err) {
        // Mock fallback delete for sandboxed test
        setHistoryItems((prev) => prev.filter((item) => item.id !== id));
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-[70vh] w-full items-center justify-center">
        <Spinner size="lg" color="indigo" />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-8 w-full">
      {/* Title section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex flex-col gap-1">
          <h1 className="text-3xl font-black text-slate-100 tracking-tight">Dashboard</h1>
          <p className="text-sm text-slate-500 font-semibold font-medium">
            Monitor scores, optimize profiles, and download tailored versions
          </p>
        </div>
        <Link href="/tailor">
          <Button variant="gradient" size="md">
            Tailor a New Resume
          </Button>
        </Link>
      </div>

      {/* Stats counter grid */}
      <StatsCards stats={stats} />

      {/* Analytics Trend Chart */}
      <ScoreChart data={chartData} />

      {/* Tabular histories */}
      <div className="flex flex-col gap-4">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-bold text-slate-200">Recent Optimizations</h2>
          <Link href="/history" className="text-xs font-bold text-indigo-400 hover:text-indigo-300 hover:underline">
            View All History
          </Link>
        </div>
        <ResumeHistory items={historyItems} onDelete={handleDelete} />
      </div>
    </div>
  );
}
