import { createContext, useContext, useEffect, useState, ReactNode } from "react";

type D = { large: boolean; contrast: boolean; lite: boolean; toggle: (k: "large" | "contrast" | "lite") => void };
const Ctx = createContext<D>({ large: false, contrast: false, lite: false, toggle: () => {} });

export function DisplayProvider({ children }: { children: ReactNode }) {
  const [s, setS] = useState({ large: false, contrast: false, lite: false });
  useEffect(() => {
    const r = document.documentElement;
    r.classList.toggle("large", s.large); r.classList.toggle("contrast", s.contrast); r.classList.toggle("lite", s.lite);
  }, [s]);
  return <Ctx.Provider value={{ ...s, toggle: k => setS(p => ({ ...p, [k]: !p[k] })) }}>{children}</Ctx.Provider>;
}
export const useDisplay = () => useContext(Ctx);
