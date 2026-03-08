import { Gauge, Radio, Timer } from "lucide-react";

import { TelemetryChart } from "@/components/TelemetryChart";

export default function Home() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,#1f2538_0%,#0c0f18_35%,#07090f_100%)] px-6 py-8 text-zinc-100 sm:px-10">
      <main className="mx-auto flex w-full max-w-6xl flex-col gap-6">
        <header className="rounded-2xl border border-zinc-700/50 bg-zinc-900/60 p-6 backdrop-blur">
          <p className="mb-2 text-xs font-semibold uppercase tracking-[0.22em] text-red-400">
            Race Control
          </p>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
            F1 Telemetry Dashboard
          </h1>
          <p className="mt-2 text-sm text-zinc-400">
            Real-time monitoring for speed, throttle, brake and gear traces per driver.
          </p>
        </header>

        <section className="grid gap-4 sm:grid-cols-3">
          <article className="rounded-xl border border-zinc-800 bg-zinc-900/70 p-4">
            <div className="mb-2 flex items-center gap-2 text-zinc-400">
              <Gauge size={16} />
              <span className="text-xs uppercase tracking-widest">Top Speed</span>
            </div>
            <p className="text-2xl font-semibold">342 km/h</p>
          </article>
          <article className="rounded-xl border border-zinc-800 bg-zinc-900/70 p-4">
            <div className="mb-2 flex items-center gap-2 text-zinc-400">
              <Timer size={16} />
              <span className="text-xs uppercase tracking-widest">Best Lap</span>
            </div>
            <p className="text-2xl font-semibold">1:27.183</p>
          </article>
          <article className="rounded-xl border border-zinc-800 bg-zinc-900/70 p-4">
            <div className="mb-2 flex items-center gap-2 text-zinc-400">
              <Radio size={16} />
              <span className="text-xs uppercase tracking-widest">Live Status</span>
            </div>
            <p className="text-2xl font-semibold text-emerald-400">Connected</p>
          </article>
        </section>

        <TelemetryChart
          title="Telemetry Trace (Stub)"
          data={[
            { distance: 0, speed: 120, gear: 3, rpm: 8000 },
            { distance: 100, speed: 188, gear: 5, rpm: 10200 },
            { distance: 200, speed: 244, gear: 6, rpm: 11100 },
            { distance: 300, speed: 302, gear: 7, rpm: 11800 },
            { distance: 400, speed: 278, gear: 6, rpm: 10900 },
          ]}
        />
      </main>
    </div>
  );
}
