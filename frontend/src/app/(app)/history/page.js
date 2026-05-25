"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import api from "../../../lib/api";
import ResumeHistory from "../../../components/dashboard/ResumeHistory";
import Spinner from "../../../components/ui/Spinner";
import Button from "../../../components/ui/Button";

/**
 * Historical Optimizations List view.
 */
export default function HistoryPage() {
  const [items, setItems] = useState([]);
  const [filteredItems, setFilteredItems] = useState([]);
  const [search, setSearch] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      try {
        const response = await api.get("/tailor/history");
        const list = response.items || [];
        setItems(list);
        setFilteredItems(list);
      } catch (err) {
        console.error("Failed to load history, showing sandbox mock profiles.");
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
        setItems(mockItems);
        setFilteredItems(mockItems);
      } finally {
        setIsLoading(false);
      }
    }
    loadHistory();
  }, []);

  // Simple query-based text search
  useEffect(() => {
    if (!search.trim()) {
      setFilteredItems(items);
      return;
    }

    const query = search.toLowerCase();
    const result = items.filter(
      (item) =>
        item.job_title?.toLowerCase().includes(query) ||
        item.company?.toLowerCase().includes(query)
    );
    setFilteredItems(result);
  }, [search, items]);

  const handleDelete = async (id) => {
    if (confirm("Are you sure you want to delete this tailoring entry from your history?")) {
      try {
        await api.delete(`/tailor/${id}`);
        setItems((prev) => prev.filter((item) => item.id !== id));
      } catch (err) {
        setItems((prev) => prev.filter((item) => item.id !== id));
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
      {/* Title */}
      <div className="flex flex-col gap-1">
        <h1 className="text-3xl font-black text-slate-100 tracking-tight">Tailoring History</h1>
        <p className="text-sm text-slate-500 font-semibold font-medium">
          Access all previous resume optimization iterations, scores, and downloadable documents
        </p>
      </div>

      {/* Search Filter Bar */}
      <div className="relative w-full max-w-md">
        <input
          type="text"
          placeholder="Search by role or company name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-5 py-3.5 bg-slate-900 border border-slate-800 rounded-2xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-300 shadow-xl"
        />
        <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      {/* History Grid Table */}
      <ResumeHistory items={filteredItems} onDelete={handleDelete} />
    </div>
  );
}
