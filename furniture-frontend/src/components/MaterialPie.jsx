import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts";

const COLORS = ["#7c3aed", "#10b981", "#f59e0b", "#ef4444", "#3b82f6", "#6366f1", "#14b8a6"];

export function MaterialPie({ data }) {
  const clean = data.map(d => ({
    name: d.material,
    value: d.count
  }));

  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="font-semibold mb-2">Material distribution</h3>
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={clean}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={80}
          >
            {clean.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
