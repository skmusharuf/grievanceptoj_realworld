"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, LogOut, RefreshCw } from "lucide-react"

interface Complaint {
  id: string
  name: string
  email: string
  description: string
  category: string
  criticality: string
  status: string
  solution: string
  satisfaction_rate?: number
  created_at: string
}

interface Statistics {
  total: number
  pending: number
  resolved: number
  critical: number
  satisfaction_rate: number
  by_department: Record<string, number>
}

export default function AdminDashboard() {
  const router = useRouter()
  const [complaints, setComplaints] = useState<Complaint[]>([])
  const [statistics, setStatistics] = useState<Statistics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [selectedDept, setSelectedDept] = useState("all")
  const [sessionToken, setSessionToken] = useState<string | null>(null)
  const [selectedComplaint, setSelectedComplaint] = useState<Complaint | null>(null)

  useEffect(() => {
    // Check for session token on component mount
    const token = localStorage.getItem("adminSessionToken")

    if (!token) {
      setLoading(false)
      router.push("/admin/login")
      return
    }

    setSessionToken(token)
    // Fetch complaints after token is set
    fetchComplaints(token)
  }, [router])

  useEffect(() => {
    if (sessionToken) {
      fetchComplaints(sessionToken)
    }
  }, [selectedDept])

  const fetchComplaints = async (token: string) => {
    try {
      setLoading(true)
      const url = `http://localhost:5000/api/admin/complaints?session_token=${encodeURIComponent(token)}&department=${selectedDept}`

      const response = await fetch(url, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem("adminSessionToken")
          router.push("/admin/login")
          return
        }
        throw new Error(`Failed to fetch complaints: ${response.status}`)
      }

      const data = await response.json()
      setComplaints(data.complaints)
      setStatistics(data.statistics)
      setError("")
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : "Unknown error"
      setError(`Failed to load complaints: ${errorMsg}. Make sure backend is running on http://localhost:5000`)
    } finally {
      setLoading(false)
    }
  }

  const handleStatusUpdate = async (complaintId: string, newStatus: string, satisfactionRate: number | null) => {
    if (!sessionToken) return

    try {
      const response = await fetch(`http://localhost:5000/api/admin/complaints/${complaintId}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_token: sessionToken,
          status: newStatus,
          satisfaction_rate: satisfactionRate,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to update status")
      }

      // Refresh the complaints list
      if (sessionToken) {
        fetchComplaints(sessionToken)
      }
      setSelectedComplaint(null)
    } catch (err) {
      setError("Failed to update complaint status")
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("adminSessionToken")
    router.push("/admin/login")
  }

  const handleRefresh = () => {
    if (sessionToken) {
      fetchComplaints(sessionToken)
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-900 p-4 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-300">Loading dashboard...</p>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-slate-900 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-white">Admin Dashboard</h1>
          <Button onClick={handleLogout} variant="outline" className="bg-red-600 hover:bg-red-700 text-white border-0">
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-900/20 border border-red-700 rounded p-4 mb-6 flex gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
            <p className="text-red-300">{error}</p>
          </div>
        )}

        {/* Statistics Cards */}
        {statistics && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Total Complaints</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-white">{statistics.total}</p>
              </CardContent>
            </Card>
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Pending</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-yellow-500">{statistics.pending}</p>
              </CardContent>
            </Card>
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Resolved</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-green-500">{statistics.resolved}</p>
              </CardContent>
            </Card>
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Satisfaction Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold text-blue-500">{statistics.satisfaction_rate}%</p>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Filter and Refresh */}
        <div className="flex gap-4 mb-6">
          <select
            value={selectedDept}
            onChange={(e) => setSelectedDept(e.target.value)}
            className="bg-slate-700 border border-slate-600 text-white px-4 py-2 rounded"
          >
            <option value="all">All Departments</option>
            {statistics &&
              Object.keys(statistics.by_department).map((dept) => (
                <option key={dept} value={dept}>
                  {dept}
                </option>
              ))}
          </select>
          <Button onClick={handleRefresh} className="bg-blue-600 hover:bg-blue-700">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>

        {/* Complaints Table */}
        <Card className="bg-slate-800 border-slate-700 overflow-hidden">
          <CardHeader>
            <CardTitle className="text-white">Complaints</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left py-3 px-4 text-slate-300">ID</th>
                    <th className="text-left py-3 px-4 text-slate-300">Name</th>
                    <th className="text-left py-3 px-4 text-slate-300">Category</th>
                    <th className="text-left py-3 px-4 text-slate-300">Criticality</th>
                    <th className="text-left py-3 px-4 text-slate-300">Status</th>
                    <th className="text-left py-3 px-4 text-slate-300">Solution</th>
                    <th className="text-left py-3 px-4 text-slate-300">Satisfaction</th>
                  </tr>
                </thead>
                <tbody>
                  {complaints.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="text-center py-8 text-slate-400">
                        No complaints found
                      </td>
                    </tr>
                  ) : (
                    complaints.map((complaint) => (
                      <tr
                        key={complaint.id}
                        className="border-b border-slate-700 hover:bg-slate-700/50 cursor-pointer"
                        onClick={() => setSelectedComplaint(complaint)}
                      >
                        <td className="py-3 px-4 text-white">{complaint.id}</td>
                        <td className="py-3 px-4 text-white">{complaint.name}</td>
                        <td className="py-3 px-4 text-slate-300">{complaint.category}</td>
                        <td className="py-3 px-4">
                          <span className={complaint.criticality === "Critical" ? "text-red-400" : "text-green-400"}>
                            {complaint.criticality}
                          </span>
                        </td>
                        <td className="py-3 px-4">
                          <span
                            className={
                              complaint.status === "Resolved"
                                ? "text-green-400"
                                : complaint.status === "In Progress"
                                  ? "text-yellow-400"
                                  : "text-gray-400"
                            }
                          >
                            {complaint.status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-blue-300 truncate max-w-xs">{complaint.solution}</td>
                        <td className="py-3 px-4 text-slate-300">{complaint.satisfaction_rate || "-"}%</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Detail Modal */}
        {selectedComplaint && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <Card className="bg-slate-800 border-slate-700 w-full max-w-2xl max-h-96 overflow-y-auto">
              <CardHeader>
                <CardTitle className="text-white">Complaint Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-slate-400 text-sm">ID</p>
                  <p className="text-white">{selectedComplaint.id}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Description</p>
                  <p className="text-white">{selectedComplaint.description}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">AI Solution</p>
                  <p className="text-blue-300">{selectedComplaint.solution}</p>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Update Status</p>
                  <select
                    value={selectedComplaint.status}
                    onChange={(e) =>
                      handleStatusUpdate(
                        selectedComplaint.id,
                        e.target.value,
                        selectedComplaint.satisfaction_rate || null,
                      )
                    }
                    className="bg-slate-700 border border-slate-600 text-white px-3 py-2 rounded w-full"
                  >
                    <option value="Pending">Pending</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Resolved">Resolved</option>
                  </select>
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Satisfaction Rate (%)</p>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={selectedComplaint.satisfaction_rate || ""}
                    onChange={(e) =>
                      handleStatusUpdate(
                        selectedComplaint.id,
                        selectedComplaint.status,
                        e.target.value ? Number.parseInt(e.target.value) : null,
                      )
                    }
                    className="bg-slate-700 border border-slate-600 text-white px-3 py-2 rounded w-full"
                    placeholder="Enter satisfaction rate"
                  />
                </div>
                <Button onClick={() => setSelectedComplaint(null)} className="bg-slate-700 hover:bg-slate-600">
                  Close
                </Button>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </main>
  )
}
