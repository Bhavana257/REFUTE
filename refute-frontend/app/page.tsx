"use client";

import { useEffect, useRef, useState } from "react";

import Image from "next/image";

type RefuteResponse = {
  argument: string;
  counter_argument: string;
  reasoning: string;
  verdict: string;
};

export default function HomePage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [claim, setClaim] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RefuteResponse | null>(null);
  const [error, setError] = useState("");

  /* ================== BACKGROUND ANIMATION ================== */
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);

    const nodes = Array.from({ length: 90 }).map(() => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
    }));

    function animate() {
      ctx.clearRect(0, 0, w, h);
      nodes.forEach((n, i) => {
        n.x += n.vx;
        n.y += n.vy;
        if (n.x < 0 || n.x > w) n.vx *= -1;
        if (n.y < 0 || n.y > h) n.vy *= -1;

        ctx.beginPath();
        ctx.arc(n.x, n.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = "#93c5fd";
        ctx.fill();

        for (let j = i + 1; j < nodes.length; j++) {
          const m = nodes[j];
          const d = Math.hypot(n.x - m.x, n.y - m.y);
          if (d < 160) {
            ctx.strokeStyle = `rgba(147,197,253,${1 - d / 160})`;
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(n.x, n.y);
            ctx.lineTo(m.x, m.y);
            ctx.stroke();
          }
        }
      });
      requestAnimationFrame(animate);
    }

    animate();
    window.addEventListener("resize", () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    });
  }, []);

  /* ================== API CALL ================== */
  const handleRefute = async () => {
    if (!claim.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/challenge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ claim }),
      });

      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Failed to fetch response from backend");
    } finally {
      setLoading(false);
    }
  };

  /* ================== UI ================== */
  return (
    <main className="relative min-h-screen bg-black text-white flex items-center justify-center overflow-hidden">
      <canvas ref={canvasRef} className="absolute inset-0 z-0" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.15),transparent_70%)] z-0" />

      <div className="relative z-10 max-w-3xl w-full px-6">
        {/* Logo */}
        <div className="flex justify-center mb-6">
          <div className="relative w-20 h-20">
            <Image
              src="/refute-logo.svg"
              alt="Refute Logo"
              fill
              className="object-contain"
              priority
            />
          </div>
        </div>

        <h1 className="text-5xl font-bold text-center">Refute</h1>
        <p className="text-center text-blue-200/70 mt-3 mb-10">
          Challenge claims through structured reasoning
        </p>

        <div className="bg-neutral-900/80 backdrop-blur-xl rounded-3xl p-8 border border-white/10 shadow-2xl">
          <textarea
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            placeholder="Enter a claim to challenge..."
            className="w-full h-32 resize-none rounded-xl bg-black/60 border border-white/10 p-4 text-lg focus:outline-none"
          />

          <button
            onClick={handleRefute}
            disabled={loading}
            className="mt-6 w-full py-4 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 font-semibold hover:scale-[1.02] transition"
          >
            {loading ? "Refuting..." : "Refute Claim"}
          </button>
        </div>

        {/* RESULTS */}
        {error && (
          <p className="text-red-400 text-center mt-6">{error}</p>
        )}

        {result && (
          <div className="mt-10 space-y-4 bg-black/60 rounded-2xl p-6 border border-white/10">
            <Section title="Argument" text={result.argument} />
            <Section title="Counter-Argument" text={result.counter_argument} />
            <Section title="Reasoning" text={result.reasoning} />
            <Section title="Verdict" text={result.verdict} />
          </div>
        )}
      </div>
    </main>
  );
}

function Section({ title, text }: { title: string; text: string }) {
  return (
    <div>
      <h3 className="text-blue-400 font-semibold mb-1">{title}</h3>
      <p className="text-white/80 leading-relaxed">{text}</p>
    </div>
  );
}
