"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import UploadPanel from "@/components/contracts/UploadPanel";
import { ContractDetail } from "@/lib/types";
import api from "@/lib/apiClient";
import ClauseExplorer from "@/components/analysis/ClauseExplorer";

export default function ContractsPage() {
  const router = useRouter();
  const [current, setCurrent] = useState<ContractDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [stored, setStored] = useState<Array<{id:number,title:string,created_at:string}>>([]);
  const [storedLoading, setStoredLoading] = useState(false);
  const [unlockPasswords, setUnlockPasswords] = useState<Record<number,string>>({});
  const [storedError, setStoredError] = useState<string | null>(null);

  useEffect(() => {
    const token =
      typeof window !== "undefined" ? localStorage.getItem("crr_token") : null;
    if (!token) {
      router.replace("/login");
    }
    // fetch stored contracts
    const fetchStored = async () => {
      setStoredLoading(true);
      try {
        const res = await api.get('/contracts/stored');
        setStored(res.data);
      } catch (err:any) {
        console.error('fetch stored error', err);
      } finally {
        setStoredLoading(false);
      }
    }
    fetchStored();
  }, [router]);

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

  return (
    <div className="grid gap-4 grid-cols-1 items-start lg:grid-cols-[minmax(0,320px)_minmax(0,1fr)]">
      <div className="space-y-4">
        <UploadPanel onUploaded={handleUploaded} />
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
                onChange={(e) => setUnlockPasswords((p)=>({...p,[s.id]:e.target.value}))}
                className="rounded border px-2 py-1 text-sm"
              />
              <button
                className="ml-2 rounded bg-primary-600 px-3 py-1 text-sm text-white"
                onClick={async ()=>{
                  const pwd = unlockPasswords[s.id] ?? "";
                  if(!pwd) { setStoredError('Enter password'); return }
                  try{
                    setLoading(true);
                    const res = await api.post(`/contracts/${s.id}/unlock`, { password: pwd });
                    setCurrent(res.data);
                    setStoredError(null);
                  }catch(err:any){
                    setStoredError(err?.response?.data?.detail || 'Unlock failed');
                  }finally{setLoading(false)}
                }}
              >View</button>
            </div>
          ))}
        </div>
        {storedError && <div className="text-xs text-red-500 mt-2">{storedError}</div>}
      </div>
    </div>
    <div className="space-y-4">
        {loading && <div className="card h-64 animate-pulse" />}
        {!loading && current && (
          <>
            <div className="card">
              <div className="mb-1 text-xs font-semibold text-slate-500">Overview</div>
              <div className="text-sm font-semibold">{current.title}</div>
              <div className="mt-1 text-xs text-slate-500">
                Overall Risk: {current.overall_risk_score.toFixed(0)} / 100 · High-risk clauses:{" "}
                {current.high_risk_clauses} / {current.total_clauses}
              </div>
            </div>
            <ClauseExplorer contentText={current.content_text} clauses={current.clauses} />
          </>
        )}
        {!loading && !current && (
          <div className="card text-sm text-slate-500">
            Upload a contract to see clause-by-clause risk analysis.
          </div>
        )}
      </div>
    </div>
  );
}

