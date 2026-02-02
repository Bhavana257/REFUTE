"use client";

import { useState } from "react";

type RefuteResponse = {
  verdict: string;
  argument: string;
  counter_argument: string;
  reasoning: string[];
};

export default function Home() {
  const [claim, setClaim] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RefuteResponse | null>(null);

  const handleSubmit = async () => {
    if (!claim.trim()) return;
    setLoading(true);
    setResult(null);

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/refute`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ claim }),
      }
    );

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <main className="relative min-h-screen flex justify-center px-6 py-20 text-neutral-200">
      {/* Background */}
      <div className="ai-bg" />

      <div className="w-full max-w-4xl space-y-14">
        {/* Header */}
        <header className="text-center space-y-5">
          <div className="flex justify-center">
            <div className="text-6xl font-extrabold tracking-tight text-white drop-shadow-[0_0_20px_rgba(255,255,255,0.2)]">
              R
            </div>
          </div>

          <h1 className="text-4xl font-bold text-white">Refute</h1>
          <p className="text-neutral-400">
            Challenge a claim. Reveal structured reasoning.
          </p>
        </header>

        {/* Input */}
        <section className="glass rounded-2xl p-6 space-y-5 glow-blue">
          <textarea
            className="w-full bg-transparent text-white placeholder-neutral-500 resize-none focus:outline-none text-lg"
            rows={4}
            placeholder="Enter a claim to challenge..."
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full py-4 rounded-xl bg-white text-black font-semibold text-lg hover:bg-neutral-200 transition"
          >
            {loading ? "Analyzing…" : "Refute Claim"}
          </button>
        </section>

        {/* Results */}
        {result && (
          <section className="space-y-8 animate-fade-in">
            <div className="glass glow-red rounded-xl p-6 border border-red-700">
              <h2 className="text-sm uppercase text-red-400">Verdict</h2>
              <p className="text-3xl font-bold">{result.verdict}</p>
            </div>

            <div className="glass glow-blue rounded-xl p-6 border border-blue-700">
              <h2 className="text-blue-400 font-semibold mb-2">
                Argument (User Claim)
              </h2>
              <p>{result.argument}</p>
            </div>

            <div className="glass glow-red rounded-xl p-6 border border-red-700">
              <h2 className="text-red-400 font-semibold mb-2">
                Counter-Argument (AI Challenge)
              </h2>
              <p>{result.counter_argument}</p>
            </div>

            <div className="glass glow-yellow rounded-xl p-6 border border-yellow-600">
              <h2 className="text-yellow-400 font-semibold mb-3">
                Reasoning
              </h2>
              <ol className="list-decimal ml-6 space-y-2">
                {result.reasoning.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ol>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
