"use client";

import { ClauseAnalysis } from "@/lib/types";
import clsx from "clsx";

interface Props {
  clauses: ClauseAnalysis[];
  selectedId: number | null;
  onSelect: (clause: ClauseAnalysis) => void;
}

export default function ClauseList({ clauses, selectedId, onSelect }: Props) {
  return (
    <div className="card flex flex-col">
      <div className="mb-2 text-sm font-semibold">Clauses</div>
      <div className="scrollbar-thin flex-1 space-y-1 overflow-y-auto pr-2 text-xs">
        {clauses.map((c) => {
          const riskColor =
            c.risk_level === "High"
              ? "bg-risk-high/10 text-risk-high"
              : c.risk_level === "Moderate"
              ? "bg-risk-moderate/10 text-risk-moderate"
              : "bg-risk-low/10 text-risk-low";
          return (
            <button
              key={c.id}
              onClick={() => onSelect(c)}
              className={clsx(
                "w-full rounded-lg border px-2 py-2 text-left transition",
                selectedId === c.id
                  ? "border-primary-400 bg-primary-50 dark:border-primary-500/80 dark:bg-primary-500/5"
                  : "border-slate-200 hover:bg-slate-50 dark:border-slate-700 dark:hover:bg-slate-900"
              )}
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-medium text-slate-500">
                  Clause {c.clause_id || c.id}
                </span>
                <span
                  className={`rounded-full px-2 py-[1px] text-[10px] font-semibold ${riskColor}`}
                >
                  {c.risk_level}
                </span>
              </div>
              <div className="mt-1 line-clamp-2 text-[11px] text-slate-600 dark:text-slate-300">
                {c.text}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

