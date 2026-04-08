"use client";

import { useState } from "react";
import { ClauseAnalysis } from "@/lib/types";
import ClauseList from "./ClauseList";
import ClauseDetail from "./ClauseDetail";

interface Props {
  contentText: string;
  clauses: ClauseAnalysis[];
}

export default function ClauseExplorer({ contentText, clauses }: Props) {
  const [selected, setSelected] = useState<ClauseAnalysis | null>(clauses[0] ?? null);

  return (
    <div className="grid gap-4 xl:grid-cols-[minmax(0,300px)_minmax(0,1fr)]">
      <div>
        <ClauseList clauses={clauses} selectedId={selected?.id ?? null} onSelect={setSelected} />
      </div>
      <div>
        {selected && <ClauseDetail clause={selected} />}
      </div>
    </div>
  );
}

