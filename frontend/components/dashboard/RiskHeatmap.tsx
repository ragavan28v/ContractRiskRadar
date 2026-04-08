import { ClauseAnalysis } from "@/lib/types";

interface Props {
  clauses: ClauseAnalysis[];
}

export default function RiskHeatmap({ clauses }: Props) {
  return (
    <div className="card">
      <div className="mb-2 text-sm font-semibold">Risk Heatmap</div>
      <div className="flex h-6 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
        {clauses.map((c) => {
          const bg =
            c.risk_level === "High"
              ? "bg-risk-high"
              : c.risk_level === "Moderate"
              ? "bg-risk-moderate"
              : "bg-risk-low";
          return (
            <div
              key={c.id}
              className={`h-full flex-1 ${bg}`}
              title={`${c.clause_id} – ${c.risk_level}`}
            />
          );
        })}
      </div>
      <div className="mt-2 flex justify-between text-[10px] text-slate-500">
        <span>Low</span>
        <span>Moderate</span>
        <span>High</span>
      </div>
    </div>
  );
}

