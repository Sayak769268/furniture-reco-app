import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function PriceBucketsChart({ data }) {
  const arr = Object.entries(data).map(([bucket, count]) => ({
    bucket,
    count
  }));

  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="font-semibold mb-2">Price distribution</h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={arr}>
          <XAxis dataKey="bucket" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#f59e0b" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
