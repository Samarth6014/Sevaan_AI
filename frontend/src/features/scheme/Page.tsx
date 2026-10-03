import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../../shared/api/client";
import { usePageTitle } from "../../shared/a11y";

export default function Scheme() {
  const { id } = useParams(); const [s, setS] = useState<any>(null); usePageTitle(s?.name || "Scheme");
  useEffect(() => { api(`/api/schemes/${id}`).then(setS); }, [id]);
  if (!s) return <p>Loading...</p>;
  return (
    <article>
      <h1>{s.name}</h1>
      <p>{s.ministry}</p>
      {!s.verified && <p className="notice" role="note">These details are not verified against the official page yet. Check {s.source_official_url} before relying on them.</p>}
      <h2>Deadline</h2><p>{s.deadline.date || s.deadline.note}</p>
      <h2>Documents and where to get them</h2>
      {s.documents.length === 0 ? <p>Not drafted yet.</p> : <ul>{s.documents.map((d: any) => <li key={d.id}>{d.label}: {d.where_to_get.office === "verify" ? "verify on the official portal" : d.where_to_get.office}</li>)}</ul>}
      <h2>FAQs</h2>
      {s.faqs.length === 0 ? <p>No verified FAQs yet.</p> : s.faqs.map((f: any, i: number) => <details key={i}><summary>{f.q}</summary><p>{f.a}</p></details>)}
      <p><Link to="/cases">Start an application</Link></p>
    </article>
  );
}
