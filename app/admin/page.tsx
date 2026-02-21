"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Search, AlertCircle } from "lucide-react"
import { AdminAnalytics } from "@/components/admin-analytics"
import Link from "next/link"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function AdminDashboard() {
  const [department, setDepartment] = useState("all")
  const [departments, setDepartments] = useState<string[]>(["all"])
  const [complaints, setComplaints] = useState<any[]>([])
  const [filteredComplaints, setFilteredComplaints] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  useEffect(() => {
    fetchCategories()
  }, [])

  useEffect(() => {
    fetchComplaints()
  }, [department, statusFilter])

  useEffect(() => {
    filterComplaints()
  }, [searchTerm, complaints])

  const fetchCategories = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      const response = await fetch(`${apiUrl}/api/categories`)
      const data = await response.json()

      if (data.success && data.categories) {
        setDepartments(["all", ...data.categories])
      }
    } catch (error) {
      console.error("[v0] Error fetching categories:", error)
    }
  }

  const fetchComplaints = async () => {
    setLoading(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      const url =
        department === "all"
          ? `${apiUrl}/api/admin/complaints?status=${statusFilter}`
          : `${apiUrl}/api/admin/complaints?department=${department}&status=${statusFilter}`

      const response = await fetch(url)
      const data = await response.json()

      if (data.success) {
        setComplaints(Array.isArray(data.complaints) ? data.complaints : [])
      }
    } catch (error) {
      console.error("[v0] Error fetching complaints:", error)
      setComplaints([])
    }
    setLoading(false)
  }

  const filterComplaints = () => {
    let filtered = complaints
    if (searchTerm) {
      filtered = filtered.filter(
        (c) =>
          c.id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.email?.toLowerCase().includes(searchTerm.toLowerCase()),
      )
    }
    setFilteredComplaints(filtered)
  }

  const handleStatusChange = async (complaintId: string, newStatus: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      const response = await fetch(`${apiUrl}/api/admin/complaints/${complaintId}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      })

      if (response.ok) {
        fetchComplaints()
      }
    } catch (error) {
      console.error("[v0] Error updating status:", error)
    }
  }

  const getStatusBadgeClass = (status: string) => {
    switch (status?.toLowerCase()) {
      case "resolved":
        return "bg-green-900/20 text-green-400 border-green-700"
      case "in progress":
      case "in_progress":
        return "bg-blue-900/20 text-blue-400 border-blue-700"
      case "pending":
        return "bg-yellow-900/20 text-yellow-400 border-yellow-700"
      default:
        return "bg-slate-900/20 text-slate-400 border-slate-700"
    }
  }

  const getPriorityBadgeClass = (criticality: string) => {
    return criticality === "Critical"
      ? "bg-red-900/20 text-red-400 border-red-700"
      : "bg-slate-900/20 text-slate-400 border-slate-700"
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 py-12">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Admin Dashboard</h1>
            <p className="text-slate-400">Manage complaints and track department performance</p>
          </div>
          <Link href="/">
            <Button variant="outline" className="border-slate-600 text-white hover:bg-slate-700 bg-transparent">
              Back to Home
            </Button>
          </Link>
        </div>

        {/* Filters */}
        <div className="mb-8 grid md:grid-cols-3 gap-4">
          <div>
            <label className="text-sm font-medium text-slate-300 block mb-2">Department</label>
            <Select value={department} onValueChange={setDepartment}>
              <SelectTrigger className="bg-slate-800 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                {departments.map((dept) => (
                  <SelectItem key={dept} value={dept} className="text-white">
                    {dept === "all" ? "All Departments" : dept}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-sm font-medium text-slate-300 block mb-2">Status Filter</label>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="bg-slate-800 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="all" className="text-white">
                  All Status
                </SelectItem>
                <SelectItem value="Pending" className="text-white">
                  Pending
                </SelectItem>
                <SelectItem value="In Progress" className="text-white">
                  In Progress
                </SelectItem>
                <SelectItem value="Resolved" className="text-white">
                  Resolved
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-sm font-medium text-slate-300 block mb-2">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
              <Input
                placeholder="Search by ID, name, email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-slate-800 border-slate-700 text-white"
              />
            </div>
          </div>
        </div>

        {/* Analytics Section */}
        <AdminAnalytics department={department} />

        {/* Complaints Table */}
        <Card className="bg-slate-800 border-slate-700 mt-8">
          <CardHeader>
            <CardTitle className="text-white">Complaints Management</CardTitle>
            <CardDescription>
              {department === "all" ? "All departments" : department} - {filteredComplaints.length} complaint(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left py-3 px-4 text-slate-400">ID</th>
                    <th className="text-left py-3 px-4 text-slate-400">User</th>
                    <th className="text-left py-3 px-4 text-slate-400">Email</th>
                    <th className="text-left py-3 px-4 text-slate-400">Description</th>
                    <th className="text-left py-3 px-4 text-slate-400">Category</th>
                    <th className="text-left py-3 px-4 text-slate-400">Priority</th>
                    <th className="text-left py-3 px-4 text-slate-400">Status</th>
                    <th className="text-left py-3 px-4 text-slate-400">Date</th>
                    <th className="text-left py-3 px-4 text-slate-400">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={9} className="py-8 px-4 text-center text-slate-400">
                        Loading complaints...
                      </td>
                    </tr>
                  ) : filteredComplaints.length > 0 ? (
                    filteredComplaints.map((complaint: any) => (
                      <tr key={complaint.id} className="border-b border-slate-700 hover:bg-slate-700/50">
                        <td className="py-3 px-4 text-white font-mono text-xs">{complaint.id}</td>
                        <td className="py-3 px-4 text-slate-300">{complaint.name}</td>
                        <td className="py-3 px-4 text-slate-300 text-xs">{complaint.email}</td>
                        <td className="py-3 px-4 text-slate-300 max-w-xs truncate">{complaint.description}</td>
                        <td className="py-3 px-4 text-slate-300 text-xs">{complaint.category}</td>
                        <td className="py-3 px-4">
                          {complaint.criticality === "Critical" && (
                            <Badge
                              className={`${getPriorityBadgeClass("Critical")} border flex items-center gap-1 w-fit`}
                            >
                              <AlertCircle className="w-3 h-3" />
                              CRITICAL
                            </Badge>
                          )}
                        </td>
                        <td className="py-3 px-4">
                          <Select
                            value={complaint.status}
                            onValueChange={(value) => handleStatusChange(complaint.id, value)}
                          >
                            <SelectTrigger
                              className={`w-32 h-7 text-xs ${getStatusBadgeClass(complaint.status)} border`}
                            >
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent className="bg-slate-800 border-slate-700">
                              <SelectItem value="Pending" className="text-white text-xs">
                                Pending
                              </SelectItem>
                              <SelectItem value="In Progress" className="text-white text-xs">
                                In Progress
                              </SelectItem>
                              <SelectItem value="Resolved" className="text-white text-xs">
                                Resolved
                              </SelectItem>
                            </SelectContent>
                          </Select>
                        </td>
                        <td className="py-3 px-4 text-slate-400 text-xs">
                          {new Date(complaint.created_at).toLocaleDateString()}
                        </td>
                        <td className="py-3 px-4">
                          <Button
                            size="sm"
                            variant="outline"
                            className="border-slate-600 text-slate-300 hover:bg-slate-700 text-xs h-7 bg-transparent"
                            onClick={() => {
                              alert(
                                `Full Details:\n\nID: ${complaint.id}\nUser: ${complaint.name}\nEmail: ${complaint.email}\nPhone: ${complaint.phone || "N/A"}\nDescription: ${complaint.description}\nCategory: ${complaint.category}\nStatus: ${complaint.status}\nCritical: ${complaint.criticality}`,
                              )
                            }}
                          >
                            View
                          </Button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={9} className="py-8 px-4 text-center text-slate-400">
                        No complaints found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
