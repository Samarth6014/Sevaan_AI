import { createContext, useContext, useState, ReactNode } from "react";
import en from "./locales/en.json";
import hi from "./locales/hi.json";
import te from "./locales/te.json";

const packs: Record<string, Record<string, string>> = { en, hi, te };
type Ctx = { lang: string; setLang: (l: string) => void; t: (k: string) => string };
const I18n = createContext<Ctx>({ lang: "en", setLang: () => {}, t: k => k });

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState(localStorage.getItem("sp_lang") || "en");
  const setLang = (l: string) => { localStorage.setItem("sp_lang", l); document.documentElement.lang = l; setLangState(l); };
  const t = (k: string) => packs[lang]?.[k] ?? packs.en[k] ?? k;
  return <I18n.Provider value={{ lang, setLang, t }}>{children}</I18n.Provider>;
}
export const useI18n = () => useContext(I18n);
