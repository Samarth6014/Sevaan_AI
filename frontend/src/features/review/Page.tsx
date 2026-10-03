import { useEffect, useMemo, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { api } from "../../shared/api/client";
import { useI18n } from "../../shared/i18n";
import { Button } from "../../shared/ui";
import { speak, usePageTitle } from "../../shared/a11y";

export default function Review() {
  const { caseId } = useParams(); const { t, lang } = useI18n(); const nav = useNavigate(); usePageTitle("Review");
  const [form, setForm] = useState<Record<string, any>>({}); const [out, setOut] = useState(""); const [busy, setBusy] = useState(false);
  useEffect(() => { api(`/api/cases/${caseId}`).then(c => setForm(c.form || {})); }, [caseId]);
  const entries = useMemo(() => Object.entries(form), [form]);
  const lines = entries.map(([k, v]: any) => `${k}: ${v?.value ?? ""}`);
  async function decide(decision: boolean) { setBusy(true); try { const r = await api(`/api/cases/${caseId}/confirm`, { method:"POST", json:{decision} }); setOut(r.reply); if (decision) setTimeout(() => nav(`/cases`), 2500); } finally { setBusy(false); } }
  return (
    <div>
      <div className="page-head"><div><h1>Review before submission</h1><p>Read every important field. Nothing is sent until you explicitly confirm.</p></div><Link className="btn plain" to={`/chat/${caseId}`}>Back to chat</Link></div>
      <div className="review-shell">
        <section className="review-card">
          {entries.length === 0 ? <div className="empty-state">The review is not ready yet. Continue the chat until the assistant reaches the review stage.</div> : <>{entries.map(([k,v]: any) => <div className="review-row" key={k}><strong>{k.replaceAll("_"," ")}</strong><div className="review-value">{String(v?.value ?? "—")}</div><span className="source-tag">{v?.source || "unknown source"}</span></div>)}</>}
        </section>
        <aside className="confirm-card">
          <h3>Your confirmation</h3><p>This is the human gate. The simulated portal can only receive the form after a valid confirmation token is created.</p>
          <div className="check-list"><div className="check-line">Every important field is visible.</div><div className="check-line">Sources are shown beside the values.</div><div className="check-line">Changing facts invalidates the confirmation.</div></div>
          <div className="row"><Button kind="plain" onClick={() => speak(lines.join(". "), lang)}>{t("readAloud")}</Button><Button className="success" onClick={() => decide(true)} disabled={busy || entries.length === 0}>{busy ? "Processing…" : t("yes")}</Button></div>
          <Button kind="plain" onClick={() => decide(false)} disabled={busy} style={{marginTop:8,width:"100%"}}>{t("no")}</Button>
          {out && <p className="notice" style={{marginTop:12}} role="status" aria-live="polite">{out}</p>}
        </aside>
      </div>
    </div>
  );
}
