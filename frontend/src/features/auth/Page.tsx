import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, session } from "../../shared/api/client";
import { useI18n } from "../../shared/i18n";
import { Button, Field, Notice, ErrorText } from "../../shared/ui";
import { usePageTitle } from "../../shared/a11y";

export default function Login() {
  const { t } = useI18n(); usePageTitle(t("login")); const nav = useNavigate();
  const [phone, setPhone] = useState(""); const [otp, setOtp] = useState(""); const [role, setRole] = useState("citizen"); const [sent, setSent] = useState(false); const [err, setErr] = useState("");
  async function send() { try { await api("/api/auth/otp", { method:"POST", json:{phone} }); setSent(true); setErr(""); } catch(e:any) { setErr(e.message); } }
  async function verify() { try { const r = await api("/api/auth/verify", { method:"POST", json:{phone, otp, role} }); session.set(r.token,r.role); nav(r.role === "admin" ? "/admin" : r.role === "helper" ? "/assisted" : "/cases"); } catch(e:any) { setErr(e.message); } }
  return (
    <div className="auth-wrap"><div className="auth-card">
      <div className="eyebrow">ScholarPath · Demo access</div><h1>Welcome back.</h1><p className="auth-sub">Use the demo OTP to step into a simulated scholarship journey.</p>
      <Notice>{t("demo")} The login is intentionally simulated; no SMS is sent.</Notice>
      <Field id="phone" label={t("phone")}><input id="phone" inputMode="numeric" autoComplete="tel" value={phone} onChange={e => setPhone(e.target.value)} placeholder="10-digit demo number" /></Field>
      <Field id="role" label="Role"><select id="role" value={role} onChange={e => setRole(e.target.value)}><option value="citizen">Citizen</option><option value="helper">Volunteer helper</option><option value="admin">Officer (admin)</option></select></Field>
      {!sent ? <Button onClick={send} disabled={phone.length < 10}>Send demo OTP</Button> : <><Field id="otp" label={t("otp")}><input id="otp" inputMode="numeric" value={otp} onChange={e => setOtp(e.target.value)} placeholder="6-digit code" /></Field><Button onClick={verify}>Enter ScholarPath</Button></>}
      {sent && <div className="demo-otp"><span>Demo OTP</span><span className="otp-code">123456</span></div>}
      <ErrorText msg={err} />
    </div></div>
  );
}
