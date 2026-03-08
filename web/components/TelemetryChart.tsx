"use client";

type TelemetryPoint = {
  distance: number;
  speed: number;
  gear: number;
  rpm: number;
};

type TelemetryChartProps = {
  title: string;
  data: TelemetryPoint[];
};

export function TelemetryChart({ title, data }: TelemetryChartProps) {
  return (
    <section className="rounded-2xl border border-zinc-800 bg-zinc-900/70 p-5">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-zinc-100">{title}</h2>
        <span className="text-xs uppercase tracking-widest text-zinc-400">
          Recharts placeholder
        </span>
      </div>

      <div className="grid gap-3 text-sm sm:grid-cols-3">
        <div className="rounded-lg bg-zinc-800/60 p-3">
          <p className="text-zinc-400">Latest Speed</p>
          <p className="text-xl font-semibold">{data.at(-1)?.speed ?? 0} km/h</p>
        </div>
        <div className="rounded-lg bg-zinc-800/60 p-3">
          <p className="text-zinc-400">Current Gear</p>
          <p className="text-xl font-semibold">G{data.at(-1)?.gear ?? 0}</p>
        </div>
        <div className="rounded-lg bg-zinc-800/60 p-3">
          <p className="text-zinc-400">Engine RPM</p>
          <p className="text-xl font-semibold">{data.at(-1)?.rpm ?? 0}</p>
        </div>
      </div>

      <div className="mt-4 rounded-lg border border-dashed border-zinc-700 p-6 text-center text-zinc-400">
        Chart canvas placeholder (Speed / Gear / RPM over distance)
      </div>
    </section>
  );
}
