"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/apiClient";
import { DashboardStats } from "@/lib/types";

export default function AnalyticsPage() {
  const router = useRouter();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("crr_token") : null;
    if (!token) {
      router.replace("/login");
      return;
    }

    const load = async () => {
      try {
        const res = await api.get("/dashboard/stats");
        setStats(res.data);
      } catch (err: any) {
        if (err?.response?.status === 401) {
          router.replace("/login");
        }
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [router]);

  const riskDistribution = stats?.risk_distribution ?? { Low: 0, Moderate: 0, High: 0 };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Detailed Analysis</h1>
        <p className="mt-1 text-sm text-slate-500">Clause-level risk patterns and trends across all contracts</p>
      </div>

      {loading ? (
        <div className="rounded-lg border border-slate-200 bg-white p-8 text-sm text-slate-500 dark:border-slate-700 dark:bg-slate-800">
          Loading analytics...
        </div>
      ) : stats && stats.total_contracts > 0 ? (
        <div className="space-y-6">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-800">
              <div className="text-xs font-semibold uppercase text-slate-500">Total Clauses</div>
              <div className="mt-2 text-2xl font-bold">{stats.total_clauses}</div>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-800">
              <div className="text-xs font-semibold uppercase text-slate-500">High-Risk</div>
              <div className="mt-2 text-2xl font-bold text-red-600">{stats.high_risk_clauses}</div>
              <div className="mt-1 text-xs text-slate-500">
                {stats.total_clauses ? ((stats.high_risk_clauses / stats.total_clauses) * 100).toFixed(0) : 0}% of total
              </div>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-800">
              <div className="text-xs font-semibold uppercase text-slate-500">Avg Risk Score</div>
              <div className="mt-2 text-2xl font-bold">{stats.average_overall_risk.toFixed(0)}</div>
              <div className="mt-1 text-xs text-slate-500">out of 100</div>
            </div>
            <div className="rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-700 dark:bg-slate-800">
              <div className="text-xs font-semibold uppercase text-slate-500">Contracts Analyzed</div>
              <div className="mt-2 text-2xl font-bold">{stats.total_contracts}</div>
              <div className="mt-1 text-xs text-slate-500">total</div>
            </div>
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-800">
            <h2 className="mb-4 text-lg font-semibold">Risk Distribution</h2>
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600">{riskDistribution.Low}</div>
                <div className="mt-1 text-sm text-slate-500">Low Risk</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-amber-600">{riskDistribution.Moderate}</div>
                <div className="mt-1 text-sm text-slate-500">Moderate Risk</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-red-600">{riskDistribution.High}</div>
                <div className="mt-1 text-sm text-slate-500">High Risk</div>
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-6 dark:border-slate-700 dark:bg-slate-800">
            <h2 className="mb-4 text-lg font-semibold">Risk Categories</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Score 80-100 (Critical)</span>
                <span className="text-sm font-bold text-red-600">{stats.high_risk_clauses} clauses</span>
              </div>
              <div className="h-2 w-full rounded-full bg-slate-100 dark:bg-slate-700">
                <div
                  className="h-2 rounded-full bg-red-600"
                  style={{
                    width: stats.total_clauses ? `${(stats.high_risk_clauses / stats.total_clauses) * 100}%` : "0%",
                  }}
                />
              </div>

              <div className="mt-4 flex items-center justify-between">
                <span className="text-sm font-medium">Score 40-79 (Medium)</span>
                <span className="text-sm font-bold text-amber-600">{riskDistribution.Moderate} clauses</span>
              </div>
              <div className="h-2 w-full rounded-full bg-slate-100 dark:bg-slate-700">
                <div
                  className="h-2 rounded-full bg-amber-600"
                  style={{
                    width: stats.total_clauses ? `${(riskDistribution.Moderate / stats.total_clauses) * 100}%` : "0%",
                  }}
                />
              </div>

              <div className="mt-4 flex items-center justify-between">
                <span className="text-sm font-medium">Score 0-39 (Low)</span>
                <span className="text-sm font-bold text-green-600">{riskDistribution.Low} clauses</span>
              </div>
              <div className="h-2 w-full rounded-full bg-slate-100 dark:bg-slate-700">
                <div
                  className="h-2 rounded-full bg-green-600"
                  style={{
                    width: stats.total_clauses ? `${(riskDistribution.Low / stats.total_clauses) * 100}%` : "0%",
                  }}
                />
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-slate-200 bg-blue-50 p-6 dark:border-slate-700 dark:bg-slate-800">
            <h2 className="mb-3 text-lg font-semibold">Key Insights</h2>
            <ul className="space-y-2 text-sm text-slate-700 dark:text-slate-300">
              {stats.high_risk_clauses > 0 && (
                <li>You have <strong>{stats.high_risk_clauses}</strong> high-risk clauses that need immediate attention</li>
              )}
              {stats.average_overall_risk > 60 && (
                <li>Overall contract risk is <strong>elevated</strong> (score: {stats.average_overall_risk.toFixed(0)})</li>
              )}
              {stats.average_overall_risk <= 40 && (
                <li>Your contracts have <strong>low average risk</strong> (score: {stats.average_overall_risk.toFixed(0)})</li>
              )}
              <li>
                Review high-risk clauses in the{" "}
                <a href="/contracts" className="font-semibold underline">
                  Contracts
                </a>{" "}
                page for safer alternatives
              </li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="rounded-lg border border-slate-200 bg-slate-50 p-8 text-center dark:border-slate-700 dark:bg-slate-900">
          <p className="text-sm text-slate-500">
            No contracts uploaded yet. Upload contracts from the{" "}
            <a href="/contracts" className="font-semibold text-primary-600 hover:underline dark:text-primary-400">
              Contracts
            </a>{" "}
            page to see detailed risk analysis here.
          </p>
        </div>
      )}
    </div>
  );
}
