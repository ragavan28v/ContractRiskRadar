import { DashboardStats } from "@/lib/types";

interface Props {
  stats: DashboardStats | null;
  loading: boolean;
}

export default function OverviewCards({ stats, loading }: Props) {
  const skeleton = <div className="h-12 w-24 animate-pulse rounded bg-slate-200 dark:bg-slate-800" />;

  return (
    <div className="grid gap-4 md:grid-cols-4">
      <div className="card">
        <div className="text-xs font-medium text-slate-500">Overall Risk</div>
        <div className="mt-2 flex items-baseline gap-1">
          {loading || !stats ? (
            skeleton
          ) : (
            <>
              <span className="text-2xl font-semibold">{stats.average_overall_risk.toFixed(0)}</span>
              <span className="text-xs text-slate-500">/ 100</span>
            </>
          )}
        </div>
      </div>
      <div className="card">
        <div className="text-xs font-medium text-slate-500">Total Contracts</div>
        <div className="mt-2 text-2xl font-semibold">{loading || !stats ? "..." : stats.total_contracts}</div>
      </div>
      <div className="card">
        <div className="text-xs font-medium text-slate-500">Total Clauses</div>
        <div className="mt-2 text-2xl font-semibold">{loading || !stats ? "..." : stats.total_clauses}</div>
      </div>
      <div className="card">
        <div className="text-xs font-medium text-slate-500">High Risk Clauses</div>
        <div className="mt-2 text-2xl font-semibold text-risk-high">{loading || !stats ? "..." : stats.high_risk_clauses}</div>
      </div>
    </div>
  );
}
