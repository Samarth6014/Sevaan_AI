import { ReactNode, ButtonHTMLAttributes } from "react";

export function Button(p: ButtonHTMLAttributes<HTMLButtonElement> & { kind?: "primary" | "plain" }) {
  const { kind = "primary", className = "", ...rest } = p;
  return <button {...rest} className={`btn ${kind} ${className}`} />;
}
export function Field({ id, label, children }: { id: string; label: string; children: ReactNode }) {
  return <div className="field"><label htmlFor={id}>{label}</label>{children}</div>;
}
export function Notice({ children }: { children: ReactNode }) { return <p className="notice" role="note">{children}</p>; }
export function ErrorText({ msg }: { msg: string }) { return msg ? <p className="error" role="alert">{msg}</p> : null; }
