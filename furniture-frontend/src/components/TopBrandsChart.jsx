import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function TopBrandsChart({ data }) {
  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="font-semibold mb-2">Top brands</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <XAxis dataKey="brand" hide />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#7c3aed" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
