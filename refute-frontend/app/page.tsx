"use client";

import { useEffect, useRef, useState } from "react";

import Image from "next/image";

export default function HomePage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [claim, setClaim] = useState("");

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const context = canvas.getContext("2d");
    if (!context) return;

    const ctx = context; // ✅ non-null forever

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

  return (
    <main className="relative min-h-screen overflow-hidden bg-black text-white flex items-center justify-center">
      {/* Animated Network Background */}
      <canvas ref={canvasRef} className="absolute inset-0 z-0" />

      {/* Radial Glow */}
      <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_center,rgba(59,130,246,0.15),transparent_70%)]" />

      {/* Main Content */}
      <div className="relative z-10 w-full max-w-3xl px-6">
        {/* Logo */}
        <div className="flex justify-center mb-6">
          <div className="relative w-20 h-20">
            <Image
              src="/refute-logo.svg"
              alt="Refute Logo"
              fill
              priority
              className="object-contain drop-shadow-[0_0_20px_rgba(59,130,246,0.6)]"
            />
          </div>
        </div>

        {/* Title */}
        <h1 className="text-5xl font-bold text-center tracking-tight">
          Refute
        </h1>
        <p className="text-center text-blue-200/70 mt-3 mb-10">
          Challenge claims through structured reasoning and intelligent rebuttal.
        </p>

        {/* Card */}
        <div className="relative bg-neutral-900/80 backdrop-blur-2xl rounded-3xl p-8 shadow-[0_0_80px_rgba(59,130,246,0.25)] border border-white/10">
          <textarea
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            placeholder="Enter a claim you want to challenge…"
            className="w-full h-36 resize-none bg-black/60 rounded-2xl border border-white/10 p-5 text-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />

          <button
            className="mt-6 w-full py-4 rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 font-semibold text-lg hover:scale-[1.02] hover:shadow-xl hover:shadow-blue-500/40 transition-all"
            onClick={() => {
              if (!claim.trim()) return;
              alert("Frontend is wired. Backend call will be enabled next.");
            }}
          >
            Refute Claim
          </button>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-white/30 mt-6">
          Powered by Gemini 3 • Built for critical thinking
        </p>
      </div>
    </main>
  );
}
