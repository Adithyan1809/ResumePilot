"use client";

import React from "react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";

/**
 * Preview parsed resume segments.
 */
export default function ResumePreview({ parsedSections }) {
  if (!parsedSections) return null;

  const {
    contact_info = {},
    summary = "",
    experience = [],
    education = [],
    skills = [],
    certifications = [],
  } = parsedSections;

  return (
    <div className="flex flex-col gap-8 w-full max-h-[70vh] overflow-y-auto pr-2 custom-scrollbar">
      {/* Contact card */}
      <Card variant="outline" className="p-6 border-slate-800 bg-slate-950/20">
        <h4 className="text-xl font-bold text-slate-100">{contact_info.name || "Candidate Name"}</h4>
        <div className="flex flex-wrap gap-x-4 gap-y-2 text-sm text-slate-400 mt-2">
          {contact_info.email && <span>{contact_info.email}</span>}
          {contact_info.phone && <span>{contact_info.phone}</span>}
          {contact_info.location && <span>{contact_info.location}</span>}
        </div>
      </Card>

      {/* Summary */}
      {summary && (
        <div className="flex flex-col gap-2">
          <h5 className="text-xs font-bold text-slate-500 uppercase tracking-widest">
            Professional Summary
          </h5>
          <p className="text-sm text-slate-300 leading-relaxed bg-slate-950/25 p-4 rounded-xl border border-slate-800/40">
            {summary}
          </p>
        </div>
      )}

      {/* Experience */}
      {experience && experience.length > 0 && (
        <div className="flex flex-col gap-4">
          <h5 className="text-xs font-bold text-slate-500 uppercase tracking-widest">
            Work Experience
          </h5>
          <div className="flex flex-col gap-4">
            {experience.map((job, idx) => (
              <div key={idx} className="bg-slate-950/15 border border-slate-850 p-5 rounded-2xl flex flex-col gap-3">
                <div className="flex flex-col md:flex-row justify-between md:items-center gap-1">
                  <div>
                    <h6 className="font-bold text-slate-200 text-sm">{job.role}</h6>
                    <span className="text-xs text-indigo-400 font-medium">{job.company}</span>
                  </div>
                  <span className="text-xs text-slate-500 font-semibold">{job.dates}</span>
                </div>
                <ul className="list-disc pl-5 flex flex-col gap-1.5 text-xs text-slate-400 leading-relaxed">
                  {job.bullets?.map((b, bIdx) => (
                    <li key={bIdx}>{b}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Skills */}
      {skills && skills.length > 0 && (
        <div className="flex flex-col gap-2">
          <h5 className="text-xs font-bold text-slate-500 uppercase tracking-widest">
            Technical Skills
          </h5>
          <div className="flex flex-wrap gap-2 bg-slate-950/15 p-4 border border-slate-850 rounded-2xl">
            {skills.map((skill, idx) => (
              <Badge key={idx} variant="slate">
                {skill}
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* Education */}
      {education && education.length > 0 && (
        <div className="flex flex-col gap-3">
          <h5 className="text-xs font-bold text-slate-500 uppercase tracking-widest">
            Education
          </h5>
          <div className="flex flex-col gap-3">
            {education.map((edu, idx) => (
              <div key={idx} className="bg-slate-950/15 border border-slate-850 p-4 rounded-xl flex justify-between items-center text-xs">
                <div>
                  <h6 className="font-bold text-slate-300">{edu.degree}</h6>
                  <span className="text-slate-500 font-medium">{edu.school}</span>
                </div>
                <span className="text-slate-500 font-semibold">{edu.dates}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Certifications */}
      {certifications && certifications.length > 0 && (
        <div className="flex flex-col gap-2">
          <h5 className="text-xs font-bold text-slate-500 uppercase tracking-widest">
            Certifications
          </h5>
          <div className="flex flex-wrap gap-2">
            {certifications.map((cert, idx) => (
              <Badge key={idx} variant="indigo">
                {cert}
              </Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
