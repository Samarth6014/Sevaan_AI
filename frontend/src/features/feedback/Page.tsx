import { useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../shared/api/client";
import { Button, Field } from "../../shared/ui";
import { usePageTitle } from "../../shared/a11y";

export default function Feedback() {
  const { caseId } = useParams(); usePageTitle("Feedback");
  const [rating, setRating] = useState(5); const [comment, setComment] = useState(""); const [done, setDone] = useState(false);
  async function send() { await api(`/api/cases/${caseId}/feedback`, { method: "POST", json: { rating, comment } }); setDone(true); }
  return (
    <section>
      <h1>Feedback</h1>
      <Field id="rating" label="Rating (1 to 5)"><select id="rating" value={rating} onChange={e => setRating(Number(e.target.value))}>{[1, 2, 3, 4, 5].map(n => <option key={n}>{n}</option>)}</select></Field>
      <Field id="comment" label="Comment"><textarea id="comment" value={comment} onChange={e => setComment(e.target.value)} /></Field>
      <Button onClick={send}>Send feedback</Button>
      <p role="status" aria-live="polite">{done ? "Thank you." : ""}</p>
    </section>
  );
}
