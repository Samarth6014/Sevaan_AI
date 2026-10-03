import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../shared/api/client";
import { Button } from "../../shared/ui";
import { usePageTitle } from "../../shared/a11y";

export default function Consent() {
  const { caseId } = useParams(); usePageTitle("Consent");
  const [n, setN] = useState<any>(null); const [ledger, setLedger] = useState<any[]>([]);
  const load = () => api(`/api/consent/${caseId}`).then(setLedger).catch(() => {});
  useEffect(() => { api("/api/consent/notice").then(setN); load(); }, [caseId]);
  async function grant() { await api("/api/consent", { method: "POST", json: { case_id: Number(caseId), purpose: "scholarship_application" } }); load(); }
  async function revoke(id: number) { await api(`/api/consent/${id}/revoke`, { method: "POST" }); load(); }
  if (!n) return null;
  return (
    <section>
      <h1>Consent notice</h1>
      <dl>
        <dt>Data collected</dt><dd>{n.data}</dd><dt>Why</dt><dd>{n.why}</dd><dt>How long</dt><dd>{n.how_long}</dd>
        <dt>Withdraw</dt><dd>{n.withdraw}</dd><dt>Complaints</dt><dd>{n.complain}</dd>
      </dl>
      <Button onClick={grant}>I agree for this purpose: scholarship application</Button>
      <h2>Your consent record</h2>
      <ul>{ledger.map(c => <li key={c.id}>{c.purpose}: {c.status} ({c.created_at.slice(0, 10)}) {c.status === "granted" && <Button kind="plain" onClick={() => revoke(c.id)}>Revoke</Button>}</li>)}</ul>
    </section>
  );
}
