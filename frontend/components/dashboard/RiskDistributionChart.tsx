"use client";

import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from "chart.js";
import { DashboardStats } from "@/lib/types";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

interface Props {
  stats: DashboardStats | null;
}

export default function RiskDistributionChart({ stats }: Props) {
  if (!stats) {
    return <div className="card h-48 animate-pulse" />;
  }

  const data = {
    labels: ["Low", "Moderate", "High"],
    datasets: [
      {
        label: "Clause count",
        data: [
          stats.risk_distribution.Low,
          stats.risk_distribution.Moderate,
          stats.risk_distribution.High
        ],
        backgroundColor: ["#22c55e", "#eab308", "#ef4444"]
      }
    ]
  };

  return (
    <div className="card">
      <div className="mb-3 text-sm font-semibold">Risk Distribution</div>
      <Bar data={data} options={{ responsive: true, plugins: { legend: { display: false } } }} />
    </div>
  );
}

