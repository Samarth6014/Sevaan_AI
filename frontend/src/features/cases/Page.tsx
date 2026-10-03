import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../../shared/api/client";
import { useI18n } from "../../shared/i18n";
import { Button } from "../../shared/ui";
import { usePageTitle } from "../../shared/a11y";

const STAGES = ["INTAKE","MATCH","PLAN","COLLECT","FILL","REVIEW_CONFIRM","SUBMIT","TRACK"];

function stageIndex(stage: string) { const i = STAGES.indexOf(stage); return i < 0 ? 0 : i; }

export default function Cases() {
  const { t, lang } = useI18n();
  usePageTitle(t("cases"));
  const nav = useNavigate();
  const [cases, setCases] = useState<any[]>([]);
  const [busy, setBusy] = useState(false);
  const load = () => api("/api/cases").then(setCases).catch(() => setCases([]));
  useEffect(() => { load(); }, []);
  const active = useMemo(() => cases.filter(c => c.status !== "completed"), [cases]);
  async function create() { setBusy(true); try { const c = await api("/api/cases", { method: "POST", json: { language: lang } }); nav(`/consent/${c.id}`); } finally { setBusy(false); } }
  async function del(id: number) { if (window.confirm("Delete this case and its data?")) { await api(`/api/cases/${id}`, { method: "DELETE" }); load(); } }
  return (
    <div>
      <div className="page-head"><div><h1>{t("cases")}</h1><p>{active.length ? `${active.length} active case${active.length === 1 ? "" : "s"} in progress.` : "No active applications yet."}</p></div><Button onClick={create} disabled={busy}>{busy ? "Creating…" : "+ New application"}</Button></div>
      {cases.length === 0 ? <div className="empty-state"><div style={{fontSize:"2rem",marginBottom:8}}>✦</div><strong>Your first application can start here.</strong><p>Create a case, accept the consent notice, and the assistant will guide the next steps.</p><Button onClick={create}>Start application</Button></div> : <div className="case-grid">{cases.map(c => { const idx = stageIndex(c.stage); const scheme = c.chosen_scheme_id || "No scheme chosen yet"; return <article className="case-card" key={c.id}><div className="case-card-top"><span className="case-id">Case #{c.id}</span><span className={`status-pill ${c.application_id?"done":c.stage==="INTAKE"?"neutral":"active"}`}>{c.application_id ? "Submitted" : c.stage.replace("_"," ")}</span></div><h3>{scheme}</h3><p>Started {new Date(c.created_at).toLocaleDateString()} · {c.language?.toUpperCase() || "EN"}</p><div className="progress-track" aria-label={`Progress: ${Math.min(idx+1, STAGES.length)} of ${STAGES.length}`}>
{STAGES.slice(0,5).map((s,i)=><span key={s} className={i<=Math.min(idx,4)?"on":""} />)}</div><div className="case-actions"><Link className="btn primary" to={`/chat/${c.id}`}>Continue</Link><Link className="btn plain" to={`/trace/${c.id}`}>Activity</Link>{c.stage === "COLLECT" && <Link className="btn plain" to={`/documents/${c.id}`}>Documents</Link>}{c.stage === "REVIEW_CONFIRM" && <Link className="btn success" to={`/review/${c.id}`}>Review</Link>}<Button kind="plain" onClick={() => del(c.id)}>Delete</Button></div></article>})}</div>}
    </div>
  );
}
