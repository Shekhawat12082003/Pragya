import React from 'react';

export default function Orb({ state }) {
  // state: 'idle' | 'listening' | 'thinking'
  return (
    <div className={`orb-wrapper orb-${state}`}>
      <div className="orb-core" />
      <div className="orb-ring ring1" />
      <div className="orb-ring ring2" />
      <div className="orb-ring ring3" />
      <style>{`
        .orb-wrapper {
          position: relative;
          width: 80px;
          height: 80px;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }
        .orb-core {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: radial-gradient(circle at 35% 35%, #a78bfa, #7c6af7, #4c1d95);
          box-shadow: 0 0 20px #7c6af788;
          z-index: 2;
          transition: transform 0.3s ease;
        }
        .orb-ring {
          position: absolute;
          border-radius: 50%;
          border: 1px solid #7c6af744;
          animation: none;
        }
        .ring1 { width: 52px; height: 52px; }
        .ring2 { width: 64px; height: 64px; border-color: #7c6af722; }
        .ring3 { width: 76px; height: 76px; border-color: #7c6af711; }

        .orb-listening .orb-core {
          animation: pulse-core 1s ease-in-out infinite;
          box-shadow: 0 0 30px #7c6af7cc;
        }
        .orb-listening .orb-ring {
          animation: pulse-ring 1.5s ease-out infinite;
        }
        .orb-listening .ring2 { animation-delay: 0.3s; }
        .orb-listening .ring3 { animation-delay: 0.6s; }

        .orb-thinking .orb-core {
          animation: spin-glow 1.5s linear infinite;
        }

        @keyframes pulse-core {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.15); }
        }
        @keyframes pulse-ring {
          0% { transform: scale(0.9); opacity: 0.8; }
          100% { transform: scale(1.3); opacity: 0; }
        }
        @keyframes spin-glow {
          0% { box-shadow: 0 0 20px #7c6af7aa; filter: hue-rotate(0deg); }
          100% { box-shadow: 0 0 30px #a78bfacc; filter: hue-rotate(60deg); }
        }
      `}</style>
    </div>
  );
}
