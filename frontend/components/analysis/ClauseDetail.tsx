"use client";

import { ClauseAnalysis } from "@/lib/types";
import api from "@/lib/apiClient";
import { useState } from "react";

interface Props {
  clause: ClauseAnalysis;
}

export default function ClauseDetail({ clause }: Props) {
  const [rewrite, setRewrite] = useState<string | null>(clause.safer_alternative);
  const [tip, setTip] = useState<string | null>(clause.negotiation_tip);
  const [loading, setLoading] = useState(false);

  const handleRewrite = async () => {
    setLoading(true);
    try {
      const res = await api.post("/rewrite", { clause_text: clause.text });
      setRewrite(res.data.safer_alternative);
      setTip(res.data.negotiation_tip);
    } finally {
      setLoading(false);
    }
  };

  const riskColor =
    clause.risk_level === "High"
      ? "bg-risk-high/10 text-risk-high border-risk-high/30"
      : clause.risk_level === "Moderate"
      ? "bg-risk-moderate/10 text-risk-moderate border-risk-moderate/30"
      : "bg-risk-low/10 text-risk-low border-risk-low/30";

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-500 mb-1">Clause {clause.clause_id || clause.id}</div>
            <div className={`inline-block rounded-lg border px-3 py-2 ${riskColor}`}>
              <div className="font-bold text-base">{clause.risk_level} Risk</div>
              <div className="text-sm font-semibold">{clause.risk_score.toFixed(0)} / 100</div>
            </div>
          </div>
          <button
            disabled={loading}
            onClick={handleRewrite}
            className="rounded-lg border-2 border-primary-500 px-4 py-2 text-sm font-semibold text-primary-600 hover:bg-primary-50 disabled:opacity-60 dark:text-primary-200 dark:hover:bg-primary-500/10 transition"
          >
            {loading ? "Generating..." : "🔄 Safer Rewrite"}
          </button>
        </div>
      </div>

      {/* Original Clause */}
      <div className="card">
        <div className="mb-3 text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Original Clause</div>
        <div className="rounded-lg bg-slate-50 p-4 text-sm leading-relaxed text-slate-700 border border-slate-200 dark:bg-slate-900 dark:text-slate-200 dark:border-slate-700">
          {clause.text}
        </div>
      </div>

      {/* Risk Analysis */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Why Risky */}
        <div className="card">
          <div className="mb-3 text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Why This Is Risky</div>
          <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300 mb-4">
            {clause.why_risky || "No explanation provided."}
          </p>
          
          {clause.trigger_phrases?.length > 0 && (
            <div>
              <div className="mb-2 text-xs font-semibold text-slate-600 dark:text-slate-400">🚩 Risk Triggers</div>
              <div className="flex flex-wrap gap-2">
                {clause.trigger_phrases.map((t) => (
                  <span
                    key={t}
                    className="rounded-full bg-yellow-100 px-3 py-1 text-sm font-medium text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-200"
                  >
                    {t}
                  </span>
                ))}
              </div>
            </div>
          )}

          {clause.financial_exposure && (
            <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
              <div className="text-xs font-semibold text-red-600 dark:text-red-400 mb-1">💰 Financial Exposure</div>
              <p className="text-sm text-slate-700 dark:text-slate-300">{clause.financial_exposure}</p>
            </div>
          )}
          
          {clause.power_imbalance && (
            <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
              <div className="text-xs font-semibold text-orange-600 dark:text-orange-400 mb-1">⚖️ Power Imbalance</div>
              <p className="text-sm text-slate-700 dark:text-slate-300">{clause.power_imbalance}</p>
            </div>
          )}
        </div>

        {/* Safer Rewrite & Tips */}
        <div className="card">
          <div className="mb-3 text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Safer Alternative</div>
          <textarea
            className="w-full rounded-lg border-2 border-green-200 bg-green-50 p-3 text-sm leading-relaxed text-slate-700 outline-none focus:border-green-500 focus:ring-2 focus:ring-green-400/30 dark:border-green-900 dark:bg-green-900/10 dark:text-slate-200 dark:focus:ring-green-500/30 mb-3"
            value={rewrite ?? ""}
            onChange={(e) => setRewrite(e.target.value)}
            rows={7}
          />
          <div className="flex gap-2 text-xs text-slate-600 dark:text-slate-400">
            <button
              type="button"
              className="font-semibold text-green-600 hover:underline dark:text-green-400"
              onClick={() => {
                if (rewrite && typeof navigator !== "undefined") {
                  navigator.clipboard.writeText(rewrite);
                }
              }}
            >
              📋 Copy
            </button>
            <span className="ml-auto">Confidence: {(clause.confidence_score * 100).toFixed(0)}%</span>
          </div>
          
          {tip && (
            <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700">
              <div className="text-xs font-semibold text-blue-600 dark:text-blue-400 mb-2">💡 Negotiation Suggestion</div>
              <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">{tip}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

