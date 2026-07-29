"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import UploadPanel from "@/components/contracts/UploadPanel";
import { ContractDetail } from "@/lib/types";
import api from "@/lib/apiClient";
import ClauseExplorer from "@/components/analysis/ClauseExplorer";

export default function ContractsPage() {
  const router = useRouter();
  const [current, setCurrent] = useState<ContractDetail | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUploaded = async (contractId: number) => {
    setLoading(true);
    try {
      const res = await api.get(`/contracts/${contractId}`);
      setCurrent(res.data);
    } catch (err: any) {
      if (err?.response?.status === 401) router.replace("/login");
    } finally {
      setLoading(false);
    }
  };

  if (current) {
    return (
      <div className="max-w-4xl mx-auto py-8">
        <button
          className="mb-4 px-4 py-2 rounded bg-slate-200 hover:bg-slate-300 text-sm"
          onClick={() => setCurrent(null)}
        >
          Back to Upload
        </button>
        <div className="card mb-4">
          <div className="mb-1 text-xs font-semibold text-slate-500">Overview</div>
          <div className="text-sm font-semibold">{current.title}</div>
          <div className="mt-1 text-xs text-slate-500">
            Overall Risk: {current.overall_risk_score.toFixed(0)} / 100. High-risk clauses: {current.high_risk_clauses} / {current.total_clauses}
          </div>
        </div>
        <div className="card">
          <div className="mb-2 text-sm font-semibold">Clause Analysis</div>
          <ClauseExplorer contentText={current.content_text} clauses={current.clauses} />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto py-8 space-y-8">
      <UploadPanel onUploaded={handleUploaded} />
      <button
        className="w-full px-4 py-2 rounded bg-primary-600 text-white hover:bg-primary-700 text-sm"
        onClick={() => router.push("/contracts/stored")}
      >
        View Stored Documents
      </button>
    </div>
  );
}
