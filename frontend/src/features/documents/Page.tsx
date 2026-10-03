import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../../shared/api/client";
import { Button, Field, ErrorText } from "../../shared/ui";
import { usePageTitle } from "../../shared/a11y";

const TYPES = ["income_certificate", "caste_certificate", "mark_sheet", "bank_passbook", "bonafide_certificate"];

export default function Documents() {
  const { caseId } = useParams(); usePageTitle("My documents");
  const [docs, setDocs] = useState<any[]>([]); const [type, setType] = useState(TYPES[0]); const [file, setFile] = useState<File | null>(null);
  const [msg, setMsg] = useState(""); const [err, setErr] = useState(""); const [drag, setDrag] = useState(false);
  const load = () => api(`/api/cases/${caseId}/documents`).then(setDocs).catch(() => setDocs([]));
  useEffect(() => { load(); }, [caseId]);
  async function upload() { if (!file) return; setErr(""); setMsg(""); const fd = new FormData(); fd.append("doc_type", type); fd.append("file", file); try { const r = await api(`/api/cases/${caseId}/documents`, { method:"POST", body:fd }); if (!r.ok) setErr(r.error); else setMsg(r.reply || "Document added."); load(); } catch (e:any) { setErr(e.message); } }
  async function del(id: number) { await api(`/api/cases/${caseId}/documents/${id}`, { method:"DELETE" }); load(); }
  function choose(f: File | null) { if (f) setFile(f); }
  return (
    <div>
      <div className="page-head"><div><h1>My documents</h1><p>Upload the evidence needed for your current case. The demo limit is 200 KB per file.</p></div><Link className="btn plain" to={`/chat/${caseId}`}>Back to chat</Link></div>
      <div className="doc-grid">
        <div className="feature-card">
          <div className={`dropzone ${drag ? "dragging" : ""}`} onDragOver={e => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)} onDrop={e => { e.preventDefault(); setDrag(false); choose(e.dataTransfer.files?.[0] || null); }}>
            <div className="drop-icon">↑</div><h3>Drop a document here</h3><p className="meta">PDF, JPG, PNG, or TXT for the demo. Your file stays inside the simulated portal.</p>
            <input id="file" type="file" onChange={e => choose(e.target.files?.[0] || null)} style={{display:"none"}} />
            <label className="btn plain" htmlFor="file">Choose file</label>
            {file && <p className="meta" style={{marginTop:12}}><strong>Selected:</strong> {file.name}</p>}
          </div>
          <Field id="type" label="What is this document?"><select id="type" value={type} onChange={e => setType(e.target.value)}>{TYPES.map(x => <option key={x}>{x}</option>)}</select></Field>
          <div className="row"><Button onClick={upload} disabled={!file}>Upload document</Button><Link className="btn plain" to={`/chat/${caseId}`}>Continue</Link></div>
          <ErrorText msg={err} /><p className="notice" role="status" aria-live="polite">{msg}</p>
        </div>
        <div className="feature-card"><h3>Your uploaded documents</h3><div className="file-list">{docs.length === 0 ? <div className="empty-state">No documents yet. Add the first document from the left.</div> : docs.map(d => <div className="file-row" key={d.id}><div className="file-main"><div className="file-icon">▣</div><div className="file-name"><strong>{d.filename}</strong><span>{d.doc_type} · {d.status}{d.confidence != null ? ` · ${Math.round(d.confidence*100)}% confidence` : ""}</span></div></div><Button kind="plain" onClick={() => del(d.id)}>Remove</Button></div>)}</div></div>
      </div>
    </div>
  );
}
