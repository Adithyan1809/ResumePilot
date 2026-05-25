"use client";

import React, { useState, useRef } from "react";
import Button from "../ui/Button";

/**
 * Modern Drag-and-Drop Resume File Upload Zone.
 */
export default function FileUpload({
  onFileSelect,
  isUploading = false,
  error = "",
}) {
  const [isDragActive, setIsDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      _processFile(file);
    }
  };

  const handleInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      _processFile(file);
    }
  };

  const _processFile = (file) => {
    // Validate file type
    const validTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    const extension = file.name.split(".").pop().toLowerCase();
    
    if (!validTypes.includes(file.type) && !["pdf", "docx"].includes(extension)) {
      alert("Unsupported file type. Please upload a PDF or DOCX resume.");
      return;
    }

    // Validate size (10 MB maximum)
    if (file.size > 10 * 1024 * 1024) {
      alert("File too large. Maximum size is 10 MB.");
      return;
    }

    setSelectedFile(file);
    onFileSelect(file);
  };

  const triggerInputClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="flex flex-col gap-4 w-full">
      <div
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={triggerInputClick}
        className={`relative flex flex-col items-center justify-center border-2 border-dashed rounded-3xl p-8 md:p-12 text-center cursor-pointer transition-all duration-300 backdrop-blur-sm ${
          isDragActive
            ? "border-indigo-500 bg-indigo-500/5 scale-102"
            : "border-slate-800 hover:border-slate-700 bg-slate-900/30 hover:bg-slate-900/50"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx"
          className="hidden"
          onChange={handleInputChange}
          disabled={isUploading}
        />

        {/* Icon */}
        <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-4 transition-transform duration-300 ${
          isDragActive ? "bg-indigo-500/20 text-indigo-400 scale-110" : "bg-slate-950/60 text-slate-400"
        }`}>
          {isUploading ? (
            <svg className="w-8 h-8 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          ) : (
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          )}
        </div>

        {/* Labels */}
        {selectedFile ? (
          <div className="flex flex-col items-center">
            <span className="text-sm font-bold text-slate-200 truncate max-w-xs md:max-w-md">
              {selectedFile.name}
            </span>
            <span className="text-xs font-semibold text-slate-500 mt-1 uppercase">
              {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
            </span>
          </div>
        ) : (
          <div className="flex flex-col gap-2">
            <h4 className="text-lg font-bold text-slate-200">
              Drag & Drop your resume here
            </h4>
            <p className="text-sm text-slate-500 max-w-sm">
              Supports standard <span className="text-slate-400 font-semibold">PDF</span> or <span className="text-slate-400 font-semibold">DOCX</span> files up to 10 MB.
            </p>
          </div>
        )}

        {/* Indicator button inside */}
        {!selectedFile && !isUploading && (
          <Button variant="secondary" size="sm" className="mt-6 pointer-events-none">
            Browse Files
          </Button>
        )}
      </div>

      {error && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-2xl text-sm font-medium">
          {error}
        </div>
      )}
    </div>
  );
}
