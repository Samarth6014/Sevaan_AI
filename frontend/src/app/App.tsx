import { Link, Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { allRoutes } from "./router";
import { session } from "../shared/api/client";
import { useI18n } from "../shared/i18n";
import { useDisplay } from "../shared/display";
import { SkipLink } from "../shared/a11y";

const PUBLIC = ["/", "/schemes", "/login"];

function SparkleMark() {
  return <span className="brand-mark" aria-hidden="true"><span className="brand-orb" /><span className="brand-spark" /></span>;
}

function Icon({ name }: { name: string }) {
  const common = { width: 18, height: 18, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.9, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  if (name === "home") return <svg {...common}><path d="m3 11 9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/></svg>;
  if (name === "cases") return <svg {...common}><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 5V3h8v2"/><path d="M3 11h18"/><path d="M10 15h4"/></svg>;
  if (name === "bell") return <svg {...common}><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/></svg>;
  if (name === "grid") return <svg {...common}><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>;
  if (name === "logout") return <svg {...common}><path d="M10 17l5-5-5-5"/><path d="M15 12H3"/><path d="M21 3v18"/></svg>;
  return <svg {...common}><circle cx="12" cy="12" r="8"/></svg>;
}

export default function App() {
  const { t, lang, setLang } = useI18n();
  const d = useDisplay();
  const nav = useNavigate();
  const location = useLocation();
  const role = session.role;

  const isHome = location.pathname === "/";
  const isAuth = location.pathname === "/login";

  return (
    <>
      <SkipLink label={t("skip")} />
      <div className="demo-ribbon"><span className="status-dot" /> {t("demo")}</div>

      <header className="shell-topbar">
        <div className="topbar-inner">
          <Link to="/" className="brand-link" aria-label="ScholarPath home">
            <SparkleMark />
            <span><strong>Scholar</strong>Path</span>
          </Link>

          <nav className="primary-nav" aria-label="Main navigation">
            <Link className={isHome ? "active" : ""} to="/"><Icon name="home" />Home</Link>
            <Link className={location.pathname.startsWith("/schemes") ? "active" : ""} to="/schemes"><Icon name="grid" />Explore</Link>
            {role === "citizen" && <Link className={location.pathname.startsWith("/cases") ? "active" : ""} to="/cases"><Icon name="cases" />My applications</Link>}
          </nav>

          <div className="topbar-actions">
            {role === "citizen" && <Link className="icon-button" aria-label="Notifications" to="/notifications"><Icon name="bell" /></Link>}
            {role === "admin" && <Link className="tiny-role" to="/admin">Officer view</Link>}
            <label className="lang-select" aria-label={t("language")}>
              <span className="sr-only">{t("language")}</span>
              <select value={lang} onChange={e => setLang(e.target.value)}>
                <option value="en">EN</option><option value="hi">हिं</option><option value="te">తె</option>
              </select>
            </label>
            {session.token ? (
              <button className="avatar-button" onClick={() => { session.clear(); nav("/"); }} aria-label="Log out">
                <span className="avatar">{role === "admin" ? "A" : role === "helper" ? "H" : "S"}</span><Icon name="logout" />
              </button>
            ) : !isAuth && <Link className="top-cta" to="/login">Get started</Link>}
          </div>
        </div>
      </header>

      {!isHome && !isAuth && (
        <div className="utility-bar">
          <div className="utility-inner">
            <div className="utility-title">{location.pathname.startsWith("/schemes") ? "Scholarship explorer" : location.pathname.startsWith("/cases") ? "Your applications" : "ScholarPath workspace"}</div>
            <div className="display-tools">
              <label><input type="checkbox" checked={d.large} onChange={() => d.toggle("large")} /> Large text</label>
              <label><input type="checkbox" checked={d.contrast} onChange={() => d.toggle("contrast")} /> High contrast</label>
              <label><input type="checkbox" checked={d.lite} onChange={() => d.toggle("lite")} /> Lite</label>
            </div>
          </div>
        </div>
      )}

      {isHome && <div className="utility-tools-home"><label><input type="checkbox" checked={d.large} onChange={() => d.toggle("large")} /> Large text</label><label><input type="checkbox" checked={d.contrast} onChange={() => d.toggle("contrast")} /> High contrast</label><label><input type="checkbox" checked={d.lite} onChange={() => d.toggle("lite")} /> Lite mode</label></div>}

      <main id="main" className="app-main" tabIndex={-1}>
        <Routes>
          {allRoutes.map(r => <Route key={r.path} path={r.path} element={PUBLIC.includes(r.path) || r.path.startsWith("/schemes/") || session.token ? r.element : <Navigate to="/login" />} />)}
        </Routes>
      </main>

      <footer className="site-footer">
        <div><span className="footer-dot" /> ScholarPath <span className="meta">· accessible scholarship application assistant · demo only</span></div>
        <div className="footer-links"><Link to="/schemes">Explore schemes</Link>{role === "citizen" && <Link to="/cases">My applications</Link>}</div>
      </footer>
    </>
  );
}
