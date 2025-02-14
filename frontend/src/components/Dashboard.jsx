import React, { useEffect, useState } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const API_URL = "https://real-time-sentiment-analysis-for-social.onrender.com";

const Dashboard = () => {
  const [tweets, setTweets] = useState([]);
  const [stats, setStats] = useState([]);

  useEffect(() => {
    fetchTweets();
    fetchStats();
  }, []);

  const fetchTweets = async () => {
    try {
      const response = await axios.get(`${API_URL}/tweets`);
      console.log("res:", response)
      setTweets(response.data.tweets);
    } catch (error) {
      console.error("Error fetching tweets:", error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/stats`);
      console.log("stats:", response)
      setStats(response.data.stats);
    } catch (error) {
      console.error("Error fetching sentiment stats:", error);
    }
  };

  const COLORS = ["#0088FE", "#00C49F", "#FF8042"];

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-center mb-6">Sentiment Dashboard</h1>

      {/* Sentiment Statistics Chart */}
      <div className="flex justify-center mb-8">
        <PieChart width={400} height={300}>
          <Pie
            data={stats}
            dataKey="count"
            nameKey="sentiment_label"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#8884d8"
            label
          >
            {stats.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>

      {/* Recent Tweets Section */}
      <h2 className="text-xl font-semibold mb-4">Recent Tweets</h2>
      <div className="space-y-4">
        {tweets.map((tweet) => (
          <div key={tweet.id} className="border p-4 rounded-md shadow-md">
            <p className="text-gray-800">{tweet.tweet}</p>
            <span
              className={`px-2 py-1 rounded-md text-white ${
                tweet.sentiment_label === "Positive"
                  ? "bg-green-500"
                  : tweet.sentiment_label === "Negative"
                  ? "bg-red-500"
                  : "bg-gray-500"
              }`}
            >
              {tweet.sentiment_label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
