export type RiskLevel = "Low" | "Moderate" | "High";

export interface ClauseAnalysis {
  id: number;
  clause_id: string;
  clause_type: string | null;
  text: string;
  risk_detected: boolean;
  risk_level: RiskLevel;
  risk_category: string | null;
  risk_score: number;
  why_risky: string | null;
  trigger_phrases: string[];
  financial_exposure: string | null;
  power_imbalance: string | null;
  safer_alternative: string | null;
  negotiation_tip: string | null;
  confidence_score: number;
}

export interface ContractDetail {
  id: number;
  title: string;
  overall_risk_score: number;
  total_clauses: number;
  high_risk_clauses: number;
  content_text: string;
  clauses: ClauseAnalysis[];
}

export interface DashboardStats {
  total_contracts: number;
  average_overall_risk: number;
  total_clauses: number;
  high_risk_clauses: number;
  risk_distribution: {
    Low: number;
    Moderate: number;
    High: number;
  };
}

