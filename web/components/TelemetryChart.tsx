"use client";

import {
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

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

      <div className="mt-4 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="distance" 
              stroke="#9CA3AF"
              tick={{ fill: "#9CA3AF", fontSize: 12 }}
              label={{ value: "Distance (m)", position: "insideBottom", offset: -5, fill: "#9CA3AF" }}
            />
            <YAxis 
              yAxisId="speed"
              stroke="#EF4444"
              tick={{ fill: "#EF4444", fontSize: 12 }}
              label={{ value: "Speed (km/h)", angle: -90, position: "insideLeft", fill: "#EF4444" }}
            />
            <YAxis 
              yAxisId="rpm"
              orientation="right"
              stroke="#10B981"
              tick={{ fill: "#10B981", fontSize: 12 }}
              label={{ value: "RPM", angle: 90, position: "insideRight", fill: "#10B981" }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: "#1F2937", 
                border: "1px solid #374151",
                borderRadius: "8px"
              }}
              labelStyle={{ color: "#F3F4F6" }}
              itemStyle={{ color: "#F3F4F6" }}
              formatter={(value, name) => {
                if (name === "speed") return [`${value} km/h`, "Speed"];
                if (name === "gear") return [`G${value}`, "Gear"];
                if (name === "rpm") return [`${value}`, "RPM"];
                return [value, name];
              }}
              labelFormatter={(label) => `Distance: ${label}m`}
            />
            <Legend 
              wrapperStyle={{ color: "#F3F4F6" }}
              formatter={(value) => {
                if (value === "speed") return "Speed (km/h)";
                if (value === "gear") return "Gear";
                if (value === "rpm") return "RPM";
                return value;
              }}
            />
            <Line 
              yAxisId="speed"
              type="monotone" 
              dataKey="speed" 
              stroke="#EF4444" 
              strokeWidth={2}
              dot={false}
              name="speed"
            />
            <Line 
              yAxisId="speed"
              type="stepAfter" 
              dataKey="gear" 
              stroke="#3B82F6" 
              strokeWidth={2}
              dot={false}
              name="gear"
            />
            <Line 
              yAxisId="rpm"
              type="monotone" 
              dataKey="rpm" 
              stroke="#10B981" 
              strokeWidth={2}
              dot={false}
              name="rpm"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
