import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// Replace this with data from your backend later
const dummyData = [
  { month: "Jan", avgPrice: 28 },
  { month: "Feb", avgPrice: 30 },
  { month: "Mar", avgPrice: 32 },
  { month: "Apr", avgPrice: 27 },
  { month: "May", avgPrice: 35 },
  { month: "Jun", avgPrice: 33 },
];

export default function TrendChart() {
  return (
    <div className="w-full h-96">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={dummyData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="avgPrice"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
