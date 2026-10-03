import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../shared/api/client";
import { usePageTitle } from "../../shared/a11y";

export default function Trace() {
  const { caseId } = useParams(); usePageTitle("Activity"); const [rows, setRows] = useState<any[]>([]);
  useEffect(() => { api(`/api/cases/${caseId}/trace`).then(setRows); }, [caseId]);
  return (
    <section>
      <h1>Agent activity</h1>
      <p>Every step the agent took. Personal details are masked.</p>
      <ol>{rows.map((r, i) => (
        <li key={i}><strong>{r.tool}</strong> {r.ok ? "" : "(blocked or failed)"} <span className="meta">{r.ts.slice(11, 19)}</span>
          <details><summary>Details</summary><pre>{JSON.stringify({ input: r.input, output: r.output }, null, 1)}</pre></details></li>))}</ol>
    </section>
  );
}
