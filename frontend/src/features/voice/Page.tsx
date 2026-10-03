import { useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../shared/api/client";
import { useI18n } from "../../shared/i18n";
import { Button, ErrorText, Notice } from "../../shared/ui";
import { speak, LiveRegion, usePageTitle } from "../../shared/a11y";

export default function Voice() {
  const { caseId } = useParams(); const { t, lang } = useI18n(); usePageTitle(t("listen"));
  const rec = useRef<MediaRecorder | null>(null); const chunks = useRef<Blob[]>([]);
  const [recording, setRecording] = useState(false); const [reply, setReply] = useState(""); const [err, setErr] = useState("");
  async function start() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mr = new MediaRecorder(stream); chunks.current = [];
      mr.ondataavailable = e => chunks.current.push(e.data);
      mr.onstop = async () => {
        const blob = new Blob(chunks.current); const buf = new Uint8Array(await blob.arrayBuffer());
        let bin = ""; buf.forEach(b => (bin += String.fromCharCode(b)));
        try { const r = await api(`/api/cases/${caseId}/message`, { method: "POST", json: { audio_b64: btoa(bin) } }); setReply(r.reply); speak(r.reply, lang); }
        catch (e: any) { setErr(e.message); }
      };
      mr.start(); rec.current = mr; setRecording(true);
    } catch { setErr("Microphone not available. Use the typed chat instead."); }
  }
  function stop() { rec.current?.stop(); rec.current?.stream.getTracks().forEach(t => t.stop()); setRecording(false); }
  return (
    <section>
      <h1>{t("listen")}</h1>
      <Notice>Keep clips under 30 seconds. If speech is not set up, the typed chat always works.</Notice>
      <Button onClick={recording ? stop : start} aria-pressed={recording}>{recording ? "Stop" : t("listen")}</Button>
      <LiveRegion message={reply} /><p>{reply}</p><ErrorText msg={err} />
    </section>
  );
}
