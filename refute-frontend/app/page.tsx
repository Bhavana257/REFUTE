"use client";

import { useEffect, useRef, useState } from "react";

import Image from "next/image";

const API_URL = "https://refute.onrender.com/challenge";

export default function HomePage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [claim, setClaim] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);


  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const context = canvas.getContext("2d");
    if (!context) return;
    const ctx = context;

    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);

    const nodes = Array.from({ length: 90 }).map(() => ({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
    }));

    const animate = () => {
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
    };

    animate();

    const resize = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    };

    window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, []);

  const handleRefute = async () => {
    if (!claim.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ claim }),
      });

      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Backend error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="relative min-h-screen overflow-hidden bg-black text-white flex items-center justify-center">
      <canvas ref={canvasRef} className="absolute inset-0 z-0" />

      <div className="relative z-10 w-full max-w-3xl px-6">
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
          Challenge claims through structured reasoning and intelligent rebuttal.
        </p>

        <div className="bg-neutral-900/80 rounded-3xl p-8 border border-white/10">
          <textarea
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            placeholder="Enter a claim you want to challenge…"
            className="w-full h-32 bg-black/60 rounded-xl p-4"
          />

          <button
            onClick={handleRefute}
            disabled={loading}
            className="mt-6 w-full py-4 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500"
          >
            {loading ? "Refuting..." : "Refute Claim"}
          </button>

          {result && (
            <div className="mt-8 space-y-4">
              <p><b>Verdict:</b> {result.verdict}</p>
              <p><b>Argument:</b> {result.argument}</p>
              <p><b>Counter-Argument:</b> {result.counter_argument}</p>
              <p><b>Reasoning:</b> {result.reasoning}</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
