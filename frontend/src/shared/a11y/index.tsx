import { useEffect } from "react";

/** Polite live region: agent messages are announced to screen readers. */
export function LiveRegion({ message }: { message: string }) {
  return <div className="sr-only" role="status" aria-live="polite" aria-atomic="true">{message}</div>;
}

export function SkipLink({ label }: { label: string }) {
  return <a className="skip" href="#main">{label}</a>;
}

export function usePageTitle(title: string) {
  useEffect(() => { document.title = `${title} - ScholarPath (demo)`; }, [title]);
}

/** Browser speech synthesis fallback for read-aloud. */
export function speak(text: string, lang: string) {
  if (!("speechSynthesis" in window)) return;
  const u = new SpeechSynthesisUtterance(text);
  u.lang = ({ en: "en-IN", hi: "hi-IN", te: "te-IN" } as Record<string, string>)[lang] || "en-IN";
  window.speechSynthesis.cancel(); window.speechSynthesis.speak(u);
}
