import { useEffect, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../../shared/api/client";
import { useI18n } from "../../shared/i18n";
import { Button, ErrorText } from "../../shared/ui";
import { LiveRegion, usePageTitle } from "../../shared/a11y";

type Msg = { role: string; text: string };
const STAGES = ["INTAKE","MATCH","PLAN","COLLECT","FILL","REVIEW_CONFIRM","SUBMIT","TRACK"];

export default function Chat() {
  const { caseId } = useParams(); const { t } = useI18n(); usePageTitle(t("chat"));
  const [msgs, setMsgs] = useState<Msg[]>([]); const [text, setText] = useState(""); const [stage, setStage] = useState("INTAKE");
  const [err, setErr] = useState(""); const [announce, setAnnounce] = useState(""); const end = useRef<HTMLDivElement>(null);
  useEffect(() => { api(`/api/cases/${caseId}`).then(c => { setMsgs(c.conversation); setStage(c.stage); }); }, [caseId]);
  useEffect(() => end.current?.scrollIntoView({ block: "end", behavior: "smooth" }), [msgs]);
  async function send(v: string) {
    if (!v.trim()) return; setMsgs(m => [...m, { role: "user", text: v }]); setText(""); setErr("");
    try { const r = await api(`/api/cases/${caseId}/message`, { method: "POST", json: { text: v } }); setMsgs(m => [...m, { role: "agent", text: r.reply }]); setStage(r.stage); setAnnounce(r.reply); }
    catch (e: any) { setErr(e.message + " (Have you accepted the consent notice?)"); }
  }
  const current = Math.max(STAGES.indexOf(stage), 0);
  return (
    <div>
      <div className="page-head"><div><h1>Apply with help</h1><p>A guided conversation that keeps every important step visible.</p></div><div className="row"><Link className="btn plain" to={`/trace/${caseId}`}>Activity</Link><Link className="btn plain" to={`/documents/${caseId}`}>Documents</Link><Link className="btn plain" to={`/voice/${caseId}`}>Voice</Link></div></div>
      <div className="chat-layout">
        <div className="chat-panel">
          <div className="chat-panel-head"><div className="chat-agent"><div className="agent-avatar">S</div><div><strong>ScholarPath assistant</strong><div className="meta">Rule-led · human confirmation required</div></div></div><span className="tag green">{stage.replace("_"," ")}</span></div>
          <div className="chat-body" aria-label="Conversation">
            {msgs.length === 0 && <div className="empty-state">Tell me your class, family income, school type, category, or what scholarship you are looking for.</div>}
            {msgs.map((m,i)=><div key={i} className={`chat-bubble ${m.role === "agent" ? "agent" : "user"}`}><div className="meta" style={{marginBottom:4}}>{m.role === "agent" ? "ScholarPath" : "You"}</div><div style={{whiteSpace:"pre-wrap"}}>{m.text}</div></div>)}
            <div ref={end} />
          </div>
          <LiveRegion message={announce} />
          {stage === "REVIEW_CONFIRM" && <div style={{padding:"0 18px 12px"}}><Link className="btn success" to={`/review/${caseId}`}>Review and confirm application</Link></div>}
          <div className="chat-composer"><form onSubmit={e => { e.preventDefault(); send(text); }}><div className="composer-row"><textarea className="composer-input" value={text} onChange={e => setText(e.target.value)} placeholder={t("typeHere")} rows={2} aria-label={t("typeHere")} /><Button type="submit">Send</Button></div></form><div className="quick-prompts"><button type="button" onClick={() => send("Show scholarships for me")}>Find scholarships</button><button type="button" onClick={() => send("What documents do I need?")}>Documents</button><button type="button" onClick={() => send("What happens next?")}>What happens next?</button></div><ErrorText msg={err} /></div>
        </div>
        <aside className="chat-side">
          <div className="side-card"><h3>Journey</h3><div className="stage-list">{STAGES.map((s,i)=><div key={s} className={`stage ${i<current?"done":""} ${i===current?"current":""}`}><span className="stage-dot" /> <span>{s.replace("_"," ")}</span></div>)}</div></div>
          <div className="side-card"><h3>Safety checkpoint</h3><p className="meta">Eligibility comes from the rules engine. A submission cannot happen until you explicitly confirm the review summary.</p></div>
        </aside>
      </div>
    </div>
  );
}
