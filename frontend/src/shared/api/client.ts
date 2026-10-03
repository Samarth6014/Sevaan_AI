let token = localStorage.getItem("sp_token") || "";
export const session = {
  get token() { return token; },
  set(t: string, role: string) { token = t; localStorage.setItem("sp_token", t); localStorage.setItem("sp_role", role); },
  get role() { return localStorage.getItem("sp_role") || ""; },
  clear() { token = ""; localStorage.removeItem("sp_token"); localStorage.removeItem("sp_role"); },
};

export async function api<T = any>(path: string, opts: RequestInit & { json?: unknown } = {}): Promise<T> {
  const headers: Record<string, string> = { ...(opts.headers as Record<string, string>) };
  if (token) headers.Authorization = `Bearer ${token}`;
  let body = opts.body;
  if (opts.json !== undefined) { headers["Content-Type"] = "application/json"; body = JSON.stringify(opts.json); }
  const res = await fetch(path, { ...opts, headers, body });
  if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || res.statusText);
  return res.json();
}
