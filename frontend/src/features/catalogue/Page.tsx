import { useEffect, useMemo, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { api, session } from "../../shared/api/client";
import { useI18n } from "../../shared/i18n";
import { Button, Field } from "../../shared/ui";
import { usePageTitle } from "../../shared/a11y";

function Icon({ children }: { children: string }) { return <span aria-hidden="true">{children}</span>; }

export default function Catalogue() {
  const { t } = useI18n();
  const location = useLocation();
  const nav = useNavigate();
  const home = location.pathname === "/";
  usePageTitle(home ? "Home" : t("schemes"));
  const [q, setQ] = useState("");
  const [items, setItems] = useState<any[]>([]);
  const [filter, setFilter] = useState("All");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (home) return;
    setLoading(true);
    api(`/api/schemes?q=${encodeURIComponent(q)}`)
      .then(setItems)
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [q, home]);

  const filtered = useMemo(() => {
    if (filter === "All") return items;
    if (filter === "Verified") return items.filter(x => x.verified);
    if (filter === "Central") return items.filter(x => String(x.level).toLowerCase() === "central");
    return items.filter(x => (x.categories || []).some((c: string) => c.toLowerCase().includes(filter.toLowerCase())));
  }, [items, filter]);

  if (home) {
    return (
      <div className="home-page">
        <section className="hero">
          <div className="hero-copy">
            <span className="eyebrow"><span className="status-dot" /> Human-confirmed scholarship help</span>
            <h1>Scholarships, <span className="gradient-text">without the maze.</span></h1>
            <p>ScholarPath helps you discover relevant schemes, understand what is missing, prepare documents, and review every important field before a simulated submission.</p>
            <div className="hero-actions">
              <Button onClick={() => nav(session.token ? "/cases" : "/login")}>Start an application <span aria-hidden="true">↗</span></Button>
              <Link className="btn plain" to="/schemes">Explore schemes</Link>
            </div>
            <div className="hero-note"><span aria-hidden="true">✦</span><div><strong>Built around trust.</strong> Eligibility comes from deterministic rules; submission requires explicit confirmation.</div></div>
          </div>

          <div className="hero-panel">
            <div className="panel-inner">
              <div>
                <div className="panel-kicker"><span>LIVE DEMO · SCHOLARPATH</span><span>SIMULATED PORTAL</span></div>
                <div className="match-card">
                  <div className="match-card-head"><div><div className="meta" style={{color:"#b9cce4"}}>Potential match</div><h3>National Means-Cum-Merit Scholarship Scheme</h3></div><span className="match-chip">MATCHED</span></div>
                  <div className="match-bar"><span /></div>
                  <div className="panel-kicker"><span>Eligibility confidence</span><strong>84%</strong></div>
                </div>
              </div>
              <div className="hero-metrics">
                <div className="hero-metric"><strong>10+</strong><span>scheme records</span></div>
                <div className="hero-metric"><strong>3</strong><span>languages</span></div>
                <div className="hero-metric"><strong>1</strong><span>human gate</span></div>
              </div>
            </div>
          </div>
        </section>

        <section>
          <div className="section-title"><div><h2>Choose your next move</h2><p>A calm starting point, whether you are applying for the first time or checking an existing case.</p></div></div>
          <div className="action-grid">
            <Link className="action-card" to={session.token ? "/cases" : "/login"}><div className="action-icon"><Icon>➜</Icon></div><h3>Start application</h3><p>Open a guided case and let the assistant collect only what it needs.</p></Link>
            <Link className="action-card" to="/schemes"><div className="action-icon"><Icon>⌕</Icon></div><h3>Explore schemes</h3><p>Search the scholarship catalogue and open the source-backed scheme page.</p></Link>
            <Link className="action-card" to={session.token ? "/cases" : "/login"}><div className="action-icon"><Icon>◷</Icon></div><h3>Track a case</h3><p>Continue where you left off and see the current stage at a glance.</p></Link>
            <Link className="action-card" to={session.token ? "/notifications" : "/login"}><div className="action-icon"><Icon>✦</Icon></div><h3>Check updates</h3><p>View in-app reminders and status updates from your demo cases.</p></Link>
          </div>
        </section>

        <section>
          <div className="section-title"><div><h2>Why ScholarPath feels different</h2><p>Every part of the experience is designed around explainability and agency.</p></div></div>
          <div className="feature-grid">
            <div className="feature-card">
              <h3>One guided journey</h3>
              <div className="feature-list">
                {[["Discover","Find candidate schemes using structured profile facts."],["Prepare","Identify documents and surface missing information."],["Review","Show field sources and let the citizen confirm."],["Submit","Call the simulated portal only after a valid confirmation token."]].map(([a,b]) => <div className="feature-item" key={a}><div className="feature-check">✓</div><div><strong>{a}</strong><span>{b}</span></div></div>)}
              </div>
            </div>
            <div className="feature-card security-card">
              <h3>Trust is visible</h3>
              <div className="feature-list">
                <div className="feature-item"><div className="feature-check">01</div><div><strong>Deterministic eligibility</strong><span>The agent explains rule-engine output; it does not decide eligibility itself.</span></div></div>
                <div className="feature-item"><div className="feature-check">02</div><div><strong>Explicit confirmation</strong><span>A human reviews the important fields before the demo submits.</span></div></div>
                <div className="feature-item"><div className="feature-check">03</div><div><strong>Accessible by design</strong><span>Keyboard support, readable layouts, high contrast and lite mode.</span></div></div>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }

  return (
    <div>
      <div className="page-head"><div><h1>{t("schemes")}</h1><p>Search source-backed scholarship records and open a scheme before you start.</p></div><span className="tag blue">AY 2026–27 demo</span></div>
      <div className="search-panel">
        <div className="search-row"><Field id="q" label="Search schemes"><input className="search-input" id="q" type="search" placeholder="Try: disability, engineering, school…" value={q} onChange={e => setQ(e.target.value)} /></Field><div style={{alignSelf:"end"}}><Button kind="plain" onClick={() => setQ("")}>Clear</Button></div></div>
        <div className="filter-pills" role="group" aria-label="Scheme filters">
          {["All","Central","Verified"].map(f => <button key={f} className={`filter-pill ${filter===f?"active":""}`} onClick={() => setFilter(f)}>{f}</button>)}
        </div>
      </div>
      <p className="meta" aria-live="polite">{loading ? "Loading…" : `${filtered.length} scheme records shown`}</p>
      {filtered.length === 0 && !loading ? <div className="empty-state">No scheme matched that search. Try a shorter phrase or clear the filters.</div> : <div className="scheme-grid">{filtered.map(s => <article className="scheme-card" key={s.scheme_id}><div className="scheme-top"><span className="tag blue">{s.level || "central"}</span><span className={`tag ${s.verified?"green":"gold"}`}>{s.verified ? "Verified" : "Draft"}</span></div><h3>{s.name}</h3><p>{s.ministry}</p><Link className="card-link" to={`/schemes/${s.scheme_id}`}>Open scheme <span aria-hidden="true">→</span></Link></article>)}</div>}
    </div>
  );
}
