import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";

const data = [
  { month: "Jan", price: 25 },
  { month: "Feb", price: 30 },
  { month: "Mar", price: 28 },
];

export default function TrendChart() {
  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid stroke="#ccc" />
      <XAxis dataKey="month" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="price" stroke="#8884d8" />
    </LineChart>
  );
}
