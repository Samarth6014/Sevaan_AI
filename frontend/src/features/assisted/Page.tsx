import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../shared/api/client";
import { usePageTitle } from "../../shared/a11y";

export default function Assisted() {
  usePageTitle("Helper cases"); const [cases, setCases] = useState<any[]>([]);
  useEffect(() => { api("/api/cases").then(setCases); }, []);
  return (
    <section>
      <h1>Helper cases</h1>
      <p>You only see cases whose owner has granted you access, and each case has its own consent.</p>
      {cases.length === 0 && <p>No granted cases yet.</p>}
      <ul>{cases.map(c => <li key={c.id}>Case {c.id}: stage {c.stage}, status {c.status}. <Link to={`/chat/${c.id}`}>Open</Link></li>)}</ul>
    </section>
  );
}
