import { useEffect, useState } from "react";
import { api } from "../../shared/api/client";
import { Button } from "../../shared/ui";
import { usePageTitle } from "../../shared/a11y";

export default function Admin() {
  usePageTitle("Admin"); const [cases, setCases] = useState<any[]>([]); const [an, setAn] = useState<any>(null); const [schemes, setSchemes] = useState<any[]>([]);
  const [deadline, setDeadline] = useState<Record<string, string>>({});
  const load = () => { api("/api/admin/cases").then(setCases); api("/api/admin/analytics").then(setAn); api("/api/schemes").then(setSchemes); };
  useEffect(load, []);
  async function advance(id: number) { await api(`/api/admin/cases/${id}/advance`, { method: "POST", json: {} }); load(); }
  async function saveDeadline(id: string) { await api(`/api/admin/schemes/${id}`, { method: "PUT", json: { deadline_date: deadline[id] } }); }
  return (
    <section>
      <h1>Officer dashboard</h1>
      {an && <><p className="notice" role="note">{an.label}</p>
        <h2>Funnel</h2><table><thead><tr><th scope="col">Stage reached</th><th scope="col">Cases</th></tr></thead>
          <tbody>{Object.entries(an.funnel).map(([k, v]: any) => <tr key={k}><th scope="row">{k}</th><td>{v}</td></tr>)}</tbody></table>
        <p>Average rating: {an.avg_rating ?? "none yet"}. Blocked actions: {an.blocked_actions}.</p></>}
      <h2>Cases (metadata only)</h2>
      <table><thead><tr><th scope="col">Case</th><th scope="col">Stage</th><th scope="col">Status</th><th scope="col">Action</th></tr></thead>
        <tbody>{cases.map(c => <tr key={c.id}><td>{c.id}</td><td>{c.stage}</td><td>{c.status}</td><td>{c.application_id && <Button kind="plain" onClick={() => advance(c.id)}>Advance status</Button>}</td></tr>)}</tbody></table>
      <h2>Edit deadlines</h2>
      <ul className="plain">{schemes.map(s => <li key={s.scheme_id}><label htmlFor={`d-${s.scheme_id}`}>{s.name} deadline (YYYY-MM-DD)</label>{" "}
        <input id={`d-${s.scheme_id}`} onChange={e => setDeadline({ ...deadline, [s.scheme_id]: e.target.value })} /> <Button kind="plain" onClick={() => saveDeadline(s.scheme_id)}>Save</Button></li>)}</ul>
    </section>
  );
}
