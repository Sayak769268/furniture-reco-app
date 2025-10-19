import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function AvgPriceByCategoryChart({ data }) {
  const formatted = data.map(d => ({
    ...d,
    avg_price_inr: d.avg_price // assume
  }));

  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="font-semibold mb-2">Average price by category</h3>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={formatted} layout="vertical">
          <XAxis type="number" />
          <YAxis type="category" dataKey="category" width={120} />
          <Tooltip />
          <Bar dataKey="avg_price_inr" fill="#10b981" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
