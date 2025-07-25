import "./CreateGroupModal.css";

type Props = {
  onClose: () => void;
};

export default function FeedbackModal({ onClose }: Props) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2 className="modal-title">Want to support my project?</h2>
        <p style={{color:"white"}}>
          You can donate through this{" "}
          <a
            href="https://link.mercadopago.com.ar/splitred"
            target="_blank"
            rel="noopener noreferrer"
          >
            Mercado Pago
          </a>{" "}
          link.
        </p>
      </div>
    </div>
  );
}
