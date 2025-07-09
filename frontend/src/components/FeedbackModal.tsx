import { useState } from "react";
import "./FeedbackModal.css";

type Props = {
  onClose: () => void;
};

export default function FeedbackModal({ onClose }: Props) {
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "sent" | "error">("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (message.trim().length < 3) return;

    try {
      // TODO: Reemplazar por tu backend real
      // Por ahora simula un envío:
      await new Promise((res) => setTimeout(res, 1000));
      setStatus("sent");
      setTimeout(onClose, 1500);
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2 className="modal-title">Send Feedback</h2>

        <form onSubmit={handleSubmit} className="modal-form">
          <textarea
            placeholder="Write your thoughts here..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="feedback-textarea"
            rows={5}
            autoFocus
          />

          <button type="submit" className="modal-button">
            Send
          </button>

          {status === "sent" && <p className="feedback-status">✅ Thanks for your feedback!</p>}
          {status === "error" && <p className="feedback-status error">❌ Something went wrong</p>}
        </form>
      </div>
    </div>
  );
}
