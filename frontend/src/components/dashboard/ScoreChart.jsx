"use client";

import React from "react";
import Card from "../ui/Card";

/**
 * Pure SVG-based responsive line chart showing ATS scores trend.
 * Completely immune to external canvas package compile issues.
 */
export default function ScoreChart({ data = [] }) {
  // Ensure we have sorted scores chronologically
  const sortedData = [...data]
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(-7); // show last 7 tailored resumes

  const hasData = sortedData.length > 0;

  // Render SVG properties
  const width = 500;
  const height = 180;
  const padding = 35;
  const chartWidth = width - padding * 2;
  const chartHeight = height - padding * 2;

  // Generate points
  const points = [];
  if (hasData) {
    sortedData.forEach((item, index) => {
      const x = padding + (index / (Math.max(1, sortedData.length - 1))) * chartWidth;
      const y = padding + chartHeight - (item.score / 100) * chartHeight;
      points.push({ x, y, score: item.score, role: item.role });
    });
  }

  // Draw smooth cubic spline/path
  let pathD = "";
  if (points.length > 0) {
    pathD = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
      pathD += ` L ${points[i].x} ${points[i].y}`;
    }
  }

  return (
    <Card className="p-6 w-full flex flex-col gap-4">
      <div className="flex justify-between items-center border-b border-slate-800/80 pb-3">
        <h5 className="font-bold text-slate-200 text-sm">ATS Compatibility Trend</h5>
        <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">
          Last {sortedData.length || 0} Optimizations
        </span>
      </div>

      <div className="relative w-full h-[180px] flex items-center justify-center">
        {hasData ? (
          <svg className="w-full h-full" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
            {/* Grid horizontal grid lines */}
            {[0, 25, 50, 75, 100].map((level) => {
              const y = padding + chartHeight - (level / 100) * chartHeight;
              return (
                <g key={level}>
                  <line
                    x1={padding}
                    y1={y}
                    x2={width - padding}
                    y2={y}
                    className="stroke-slate-800/50"
                    strokeWidth="1"
                    strokeDasharray="4 4"
                  />
                  <text
                    x={padding - 10}
                    y={y + 3}
                    className="fill-slate-500 font-semibold text-[8px] text-right font-mono"
                    textAnchor="end"
                  >
                    {level}%
                  </text>
                </g>
              );
            })}

            {/* Main Trend Line */}
            {points.length > 0 && (
              <>
                {/* Under-shadow fill gradient */}
                <path
                  d={`${pathD} L ${points[points.length - 1].x} ${padding + chartHeight} L ${points[0].x} ${padding + chartHeight} Z`}
                  fill="url(#chartGlow)"
                  className="opacity-40"
                />
                {/* Main line */}
                <path
                  d={pathD}
                  fill="none"
                  className="stroke-indigo-500"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </>
            )}

            {/* Glowing nodes points */}
            {points.map((pt, idx) => (
              <g key={idx}>
                {/* Outer ring */}
                <circle
                  cx={pt.x}
                  cy={pt.y}
                  r="6"
                  className="fill-indigo-500/25 stroke-indigo-400"
                  strokeWidth="1.5"
                />
                {/* Inner dot */}
                <circle
                  cx={pt.x}
                  cy={pt.y}
                  r="3.5"
                  className="fill-indigo-400"
                />
              </g>
            ))}

            {/* Gradients definitions */}
            <defs>
              <linearGradient id="chartGlow" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#6366f1" stopOpacity="0.4" />
                <stop offset="100%" stopColor="#6366f1" stopOpacity="0" />
              </linearGradient>
            </defs>
          </svg>
        ) : (
          <div className="text-center p-6">
            <span className="text-xs text-slate-500 font-medium">
              No historical data available. Optimize a resume to begin tracking stats.
            </span>
          </div>
        )}
      </div>
    </Card>
  );
}
