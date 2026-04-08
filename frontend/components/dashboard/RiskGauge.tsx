interface Props {
  value: number;
}

export default function RiskGauge({ value }: Props) {
  const clamped = Math.max(0, Math.min(100, value));
  const strokeDasharray = 283;
  const offset = strokeDasharray - (clamped / 100) * strokeDasharray;

  const color =
    clamped < 33 ? "text-risk-low" : clamped < 66 ? "text-risk-moderate" : "text-risk-high";

  return (
    <div className="card flex items-center justify-center">
      <div className="relative h-40 w-40">
        <svg className="h-full w-full -rotate-90" viewBox="0 0 100 100">
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="currentColor"
            strokeWidth="8"
            className="text-slate-200 dark:text-slate-800"
            fill="none"
          />
          <circle
            cx="50"
            cy="50"
            r="45"
            stroke="currentColor"
            strokeWidth="8"
            className={color}
            strokeDasharray={strokeDasharray}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="none"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-xs uppercase tracking-wide text-slate-500">Overall Risk</span>
          <span className="mt-1 text-2xl font-semibold">{clamped.toFixed(0)}</span>
          <span className="text-[10px] text-slate-400">out of 100</span>
        </div>
      </div>
    </div>
  );
}

