"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/apiClient";
import { DashboardStats, ClauseAnalysis } from "@/lib/types";
import OverviewCards from "@/components/dashboard/OverviewCards";
import RiskGauge from "@/components/dashboard/RiskGauge";
import RiskDistributionChart from "@/components/dashboard/RiskDistributionChart";
import RiskHeatmap from "@/components/dashboard/RiskHeatmap";

export default function DashboardPage() {
  const router = useRouter();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [heatmapClauses, setHeatmapClauses] = useState<ClauseAnalysis[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token =
      typeof window !== "undefined" ? localStorage.getItem("crr_token") : null;
    if (!token) {
      router.replace("/login");
      return;
    }

    const load = async () => {
      try {
        const statsRes = await api.get("/dashboard/stats");
        setStats(statsRes.data);
      } catch (err: any) {
        if (err?.response?.status === 401) {
          router.replace("/login");
          return;
        }
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [router]);

  const overall = stats?.average_overall_risk ?? 0;

  return (
    <div className="space-y-4">
      <OverviewCards stats={stats} loading={loading} />
      <div className="grid gap-4 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
        <RiskGauge value={overall} />
        <RiskDistributionChart stats={stats} />
      </div>
      {heatmapClauses.length > 0 && <RiskHeatmap clauses={heatmapClauses} />}
    </div>
  );
}

