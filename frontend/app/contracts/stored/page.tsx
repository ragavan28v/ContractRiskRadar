"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/apiClient";
import ClauseExplorer from "@/components/analysis/ClauseExplorer";

export default function StoredContractsPage() {
  const router = useRouter();
  const [stored, setStored] = useState<Array<{ id: number; title: string; created_at: string }>>([]);
  const [storedLoading, setStoredLoading] = useState(false);
  const [unlockPasswords, setUnlockPasswords] = useState<Record<number, string>>({});
  const [storedError, setStoredError] = useState<string | null>(null);
  const [current, setCurrent] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("crr_token") : null;
    if (!token) {
      router.replace("/login");
      return;
    }

    const fetchStored = async () => {
      setStoredLoading(true);
      try {
        const res = await api.get("/contracts/stored");
        setStored(res.data);
      } catch (err: any) {
        console.error("fetch stored error", err);
      } finally {
        setStoredLoading(false);
      }
    };

    fetchStored();
  }, [router]);

  if (current) {
    return (
      <div className="max-w-4xl mx-auto py-8">
        <button
          className="mb-4 px-4 py-2 rounded bg-slate-200 hover:bg-slate-300 text-sm"
          onClick={() => setCurrent(null)}
        >
          Back to Stored List
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
      <button
        className="mb-4 px-4 py-2 rounded bg-slate-200 hover:bg-slate-300 text-sm"
        onClick={() => router.push("/contracts")}
      >
        Back to Upload
      </button>
      <div className="card">
        <div className="mb-2 text-sm font-semibold">Stored Documents</div>
        {storedLoading && <div className="text-sm text-slate-500">Loading...</div>}
        {!storedLoading && stored.length === 0 && (
          <div className="text-sm text-slate-500">No stored documents.</div>
        )}
        <div className="space-y-2">
          {stored.map((s) => (
            <div key={s.id} className="flex items-center gap-2">
              <div className="flex-1 text-sm">{s.title}</div>
              <input
                type="password"
                placeholder="Password"
                value={unlockPasswords[s.id] ?? ""}
                onChange={(e) => setUnlockPasswords((p) => ({ ...p, [s.id]: e.target.value }))}
                className="rounded border px-2 py-1 text-sm"
              />
              <button
                className="ml-2 rounded bg-primary-600 px-3 py-1 text-sm text-white"
                onClick={async () => {
                  const pwd = unlockPasswords[s.id] ?? "";
                  if (!pwd) {
                    setStoredError("Enter password");
                    return;
                  }
                  try {
                    setLoading(true);
                    const res = await api.post(`/contracts/${s.id}/unlock`, { password: pwd });
                    setCurrent(res.data);
                    setStoredError(null);
                  } catch (err: any) {
                    setStoredError(err?.response?.data?.detail || "Unlock failed");
                  } finally {
                    setLoading(false);
                  }
                }}
              >
                View
              </button>
            </div>
          ))}
        </div>
        {storedError && <div className="text-xs text-red-500 mt-2">{storedError}</div>}
      </div>
    </div>
  );
}
