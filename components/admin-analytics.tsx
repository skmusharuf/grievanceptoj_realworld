"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts"
import { BarChart3, CheckCircle, Clock, AlertCircle } from "lucide-react"

interface AdminAnalyticsProps {
  department: string
}

export function AdminAnalytics({ department }: AdminAnalyticsProps) {
  const [stats, setStats] = useState({
    total_complaints: 0,
    resolved: 0,
    pending: 0,
    in_progress: 0,
    critical: 0,
    resolution_rate: 0,
  })

  useEffect(() => {
    fetchStats()
  }, [department])

  const fetchStats = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      const url =
        department === "all"
          ? `${apiUrl}/api/admin/complaints`
          : `${apiUrl}/api/admin/complaints?department=${department}`

      const response = await fetch(url)
      const data = await response.json()

      if (data.success && data.statistics) {
        setStats({
          total_complaints: data.statistics.total,
          resolved: data.statistics.resolved,
          pending: data.statistics.pending,
          in_progress: data.statistics.in_progress,
          critical: data.statistics.critical,
          resolution_rate: data.statistics.total > 0 ? (data.statistics.resolved / data.statistics.total) * 100 : 0,
        })
      }
    } catch (error) {
      console.error("[v0] Error fetching stats:", error)
    }
  }

  const pieData = [
    { name: "Resolved", value: stats.resolved, color: "#22c55e" },
    { name: "In Progress", value: stats.in_progress, color: "#3b82f6" },
    { name: "Pending", value: stats.pending, color: "#eab308" },
  ]

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {/* Total Complaints */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-slate-300">Total Complaints</CardTitle>
          <BarChart3 className="w-4 h-4 text-blue-500" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold text-white">{stats.total_complaints}</div>
          <p className="text-xs text-slate-400 mt-1">All time</p>
        </CardContent>
      </Card>

      {/* Resolved */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-slate-300">Resolved</CardTitle>
          <CheckCircle className="w-4 h-4 text-green-500" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold text-green-400">{stats.resolved}</div>
          <p className="text-xs text-slate-400 mt-1">{stats.resolution_rate.toFixed(1)}% resolution rate</p>
        </CardContent>
      </Card>

      {/* Pending */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-slate-300">Pending</CardTitle>
          <Clock className="w-4 h-4 text-yellow-500" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold text-yellow-400">{stats.pending}</div>
          <p className="text-xs text-slate-400 mt-1">Awaiting action</p>
        </CardContent>
      </Card>

      {/* Critical */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-slate-300">Critical</CardTitle>
          <AlertCircle className="w-4 h-4 text-red-500" />
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold text-red-400">{stats.critical}</div>
          <p className="text-xs text-slate-400 mt-1">High priority</p>
        </CardContent>
      </Card>

      {/* Pie Chart */}
      <Card className="bg-slate-800 border-slate-700 md:col-span-2 lg:col-span-4">
        <CardHeader>
          <CardTitle className="text-white">Complaint Status Distribution</CardTitle>
          <CardDescription>Visual breakdown of complaint statuses</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1e293b",
                  border: "1px solid #334155",
                  borderRadius: "8px",
                  color: "#fff",
                }}
              />
              <Legend
                wrapperStyle={{
                  color: "#fff",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
