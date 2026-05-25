"use client";

import React, { useEffect, useState } from "react";

/**
 * Animated Circular SVG Score Gauge.
 */
export default function ScoreGauge({ score = 0, size = 180, title = "ATS Match Score" }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  // Animate numbers counting up on load
  useEffect(() => {
    const duration = 1000; // 1s
    const steps = 60;
    const stepTime = duration / steps;
    let currentStep = 0;

    const timer = setInterval(() => {
      currentStep++;
      const nextScore = Math.min(score, Math.round((score / steps) * currentStep));
      setAnimatedScore(nextScore);

      if (currentStep >= steps) {
        clearInterval(timer);
        setAnimatedScore(score); // snap to final in case of float rounding
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [score]);

  // SVG properties
  const strokeWidth = 14;
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  // Determine colors based on score value
  let colorClass = "stroke-rose-500 text-rose-500 drop-shadow-[0_0_8px_rgba(244,63,94,0.15)]";
  let bgGradient = "from-rose-500/10 to-rose-500/0";
  if (score >= 70) {
    colorClass = "stroke-emerald-500 text-emerald-400 drop-shadow-[0_0_8px_rgba(16,185,129,0.15)]";
    bgGradient = "from-emerald-500/10 to-emerald-500/0";
  } else if (score >= 40) {
    colorClass = "stroke-amber-500 text-amber-400 drop-shadow-[0_0_8px_rgba(245,158,11,0.15)]";
    bgGradient = "from-amber-500/10 to-amber-500/0";
  }

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative" style={{ width: size, height: size }}>
        {/* Glow center */}
        <div className={`absolute inset-4 rounded-full bg-gradient-to-b ${bgGradient} blur-xl opacity-50`} />
        
        <svg className="w-full h-full transform -rotate-90" viewBox={`0 0 ${size} ${size}`}>
          {/* Background circle */}
          <circle
            className="stroke-slate-800"
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Active progress circle */}
          <circle
            className={`transition-all duration-300 ease-out ${colorClass}`}
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>
        {/* Central numbers indicator */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-extrabold tracking-tighter text-slate-100">
            {animatedScore}
            <span className="text-lg font-semibold text-slate-400">%</span>
          </span>
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">
            Match
          </span>
        </div>
      </div>
      {title && (
        <h6 className="text-sm font-semibold text-slate-300 mt-4 tracking-wide uppercase">
          {title}
        </h6>
      )}
    </div>
  );
}
