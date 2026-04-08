"use client";

import { useState } from "react";
import api from "@/lib/apiClient";

interface Props {
  onUploaded: (contractId: number) => void;
}

export default function UploadPanel({ onUploaded }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [consent, setConsent] = useState(false);
  const [accessPassword, setAccessPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [titleError, setTitleError] = useState<string | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);

  const isFormValid = file && title.trim().length > 0;

  const handleTitleChange = (value: string) => {
    setTitle(value);
    setTitleError(null);
  };

  const handleFileSelect = (selectedFile: File | null) => {
    setFile(selectedFile);
    setFileError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    let isValid = true;
    if (!file) {
      setFileError("Please select a file");
      isValid = false;
    }
    if (!title.trim()) {
      setTitleError("Please enter a contract title");
      isValid = false;
    }
    
    if (!isValid) return;

    setLoading(true);
    setError(null);
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("title", title.trim());
      form.append("consent_store", String(consent));
      if (consent && accessPassword) form.append("access_password", accessPassword);
      console.log("Uploading file:", file.name, "Title:", title);
      const res = await api.post("/contracts/upload", form, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      console.log("Upload successful:", res.data);
      setFile(null);
      setTitle("");
      setConsent(false);
      setAccessPassword("");
      setError(null);
      onUploaded(res.data.contract_id);
    } catch (err: any) {
      console.error("Upload error:", err);
      const errorMsg = err?.response?.data?.detail || err?.message || "Upload failed. Please try again.";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="mb-3 text-sm font-semibold">Upload Contract</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label className="block mb-1 text-xs font-medium text-slate-700">Contract Title *</label>
          <input
            type="text"
            placeholder="e.g. Master Service Agreement – ACME"
            value={title}
            onChange={(e) => handleTitleChange(e.target.value)}
            className={`w-full rounded-lg border px-3 py-2 text-sm outline-none transition-colors ${
              titleError
                ? "border-red-400 bg-red-50 focus:border-red-500 focus:ring-1 focus:ring-red-500"
                : "border-slate-200 bg-slate-50 focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
            } dark:border-slate-700 dark:bg-slate-900`}
          />
          {titleError && <p className="mt-1 text-xs text-red-500">{titleError}</p>}
        </div>

        <div>
          <label className="block mb-1 text-xs font-medium text-slate-700">Contract File *</label>
          <div
            className={`flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed px-4 py-8 text-center text-xs transition-colors ${
              fileError
                ? "border-red-300 bg-red-50 text-red-600"
                : "border-slate-300 bg-slate-50 text-slate-500 hover:border-primary-400"
            } dark:border-slate-700 dark:bg-slate-900`}
            onClick={() => {
              const input = document.getElementById("crr-file-input") as HTMLInputElement;
              input?.click();
            }}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              const droppedFile = e.dataTransfer.files?.[0];
              if (droppedFile) handleFileSelect(droppedFile);
            }}
          >
            <p className="font-medium">Drag & drop PDF / DOCX / TXT</p>
            <p className="mt-1 text-[11px]">or click to browse</p>
            {file && <p className="mt-2 text-xs font-medium">{file.name}</p>}
          </div>
          {fileError && <p className="mt-1 text-xs text-red-500">{fileError}</p>}
        </div>

        <input
          id="crr-file-input"
          type="file"
          accept=".pdf,.docx,.txt"
          className="hidden"
          onChange={(e) => handleFileSelect(e.target.files?.[0] ?? null)}
        />

        <label className="flex items-center gap-2 text-xs text-slate-600">
          <input
            type="checkbox"
            checked={consent}
            onChange={(e) => setConsent(e.target.checked)}
            className="h-3 w-3 rounded border-slate-300 text-primary-600 focus:ring-primary-500"
          />
          <span>
            I consent to securely store this contract for trend analytics. Otherwise, only transient
            processing is performed.
          </span>
        </label>

        {consent && (
          <div>
            <label className="block mb-1 text-xs font-medium text-slate-700">Access Password (required to view stored document)</label>
            <input
              type="password"
              placeholder="Set a password to protect stored contract"
              value={accessPassword}
              onChange={(e) => setAccessPassword(e.target.value)}
              className="w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 dark:border-slate-700 dark:bg-slate-900"
            />
          </div>
        )}

        {error && <p className="text-xs text-red-500 font-medium">{error}</p>}

        <button
          type="submit"
          disabled={loading || !isFormValid}
          className={`w-full rounded-lg px-3 py-2 text-sm font-semibold text-white shadow-sm transition-all ${
            loading || !isFormValid
              ? "bg-slate-400 cursor-not-allowed shadow-none"
              : "bg-primary-600 hover:bg-primary-500 active:bg-primary-700"
          }`}
        >
          {loading ? "Analyzing…" : "Upload & Analyze"}
        </button>
      </form>
    </div>
  );
}

