import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  TimeScale,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  TimeScale
);

export default function CoinChart({ prices }) {
  if (!prices || prices.length === 0) {
    return <p>No price data available.</p>;
  }

  const labels = prices.map((p) =>
    new Date(p.timestamp).toLocaleDateString()
  );
  const values = prices.map((p) => p.price);

  const chartData = {
    labels,
    datasets: [
      {
        label: "Price (USD)",
        data: values,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        fill: true,
        tension: 0.2,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true, position: "top" },
    },
    scales: {
      x: { display: true, title: { display: true, text: "Date" } },
      y: { display: true, title: { display: true, text: "Price (USD)" } },
    },
  };

  return (
    <div className="chart-wrapper">
      <Line data={chartData} options={options} />
    </div>
  );
}
