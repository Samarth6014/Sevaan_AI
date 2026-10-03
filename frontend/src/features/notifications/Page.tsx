import { useEffect, useState } from "react";
import { api } from "../../shared/api/client";
import { useI18n } from "../../shared/i18n";
import { usePageTitle } from "../../shared/a11y";

export default function Notifications() {
  const { t } = useI18n(); usePageTitle(t("notifications")); const [items, setItems] = useState<any[]>([]);
  useEffect(() => { api("/api/notifications").then(setItems); }, []);
  return <section><h1>{t("notifications")}</h1>{items.length === 0 ? <p>Nothing yet.</p> : <ul>{items.map(n => <li key={n.id}>{n.message}{n.due_date ? ` (by ${n.due_date})` : ""}</li>)}</ul>}</section>;
}
