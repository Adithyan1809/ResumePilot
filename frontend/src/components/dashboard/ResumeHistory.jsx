"use client";

import React from "react";
import Link from "next/link";
import Badge from "../ui/Badge";
import Button from "../ui/Button";

/**
 * Historical list of tailored resumes for dashboard display.
 */
export default function ResumeHistory({ items = [], onDelete }) {
  if (items.length === 0) {
    return (
      <div className="p-8 bg-slate-900/10 border border-slate-800 rounded-3xl text-center">
        <svg className="w-10 h-10 text-slate-600 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.8" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p className="text-sm text-slate-400 font-semibold mb-1">No tailoring history found</p>
        <p className="text-xs text-slate-500 max-w-xs mx-auto mb-4">You haven't tailored any resumes yet. Start optimization to begin tracking.</p>
        <Link href="/tailor">
          <Button variant="primary" size="sm">
            Optimize Now
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full overflow-x-auto border border-slate-800/80 rounded-2xl bg-slate-950/20">
      <table className="w-full border-collapse text-left">
        <thead>
          <tr className="border-b border-slate-800 text-xs font-bold text-slate-500 uppercase tracking-wider bg-slate-950/65">
            <th className="px-6 py-4">Job Title</th>
            <th className="px-6 py-4">Company</th>
            <th className="px-6 py-4">ATS Match</th>
            <th className="px-6 py-4">Template</th>
            <th className="px-6 py-4">Date</th>
            <th className="px-6 py-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-850 text-sm">
          {items.map((item) => {
            let scoreVariant = "rose";
            if (item.overall_score >= 70) scoreVariant = "emerald";
            else if (item.overall_score >= 40) scoreVariant = "amber";

            return (
              <tr key={item.id} className="hover:bg-slate-900/30 transition-colors">
                <td className="px-6 py-4.5 font-bold text-slate-200">{item.job_title}</td>
                <td className="px-6 py-4.5 text-slate-400 font-medium">{item.company}</td>
                <td className="px-6 py-4.5">
                  <Badge variant={scoreVariant}>{item.overall_score}%</Badge>
                </td>
                <td className="px-6 py-4.5">
                  <Badge variant="slate" className="text-[10px]">
                    {item.template}
                  </Badge>
                </td>
                <td className="px-6 py-4.5 text-xs text-slate-500 font-semibold font-mono">
                  {new Date(item.created_at).toLocaleDateString(undefined, {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  })}
                </td>
                <td className="px-6 py-4.5 text-right flex items-center justify-end gap-2">
                  <Link href={`/tailor?id=${item.id}`}>
                    <Button variant="ghost" size="sm" className="py-1 px-3">
                      View
                    </Button>
                  </Link>
                  {onDelete && (
                    <button
                      onClick={() => onDelete(item.id)}
                      className="p-2 text-slate-600 hover:text-rose-400 hover:bg-rose-500/10 rounded-xl transition-all"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
