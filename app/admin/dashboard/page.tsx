"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Search, AlertCircle, LogOut, MapPin, User, Mail, Phone, Clock, Shield, Building } from "lucide-react"
import Link from "next/link"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from "recharts"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface Complaint {
  id: string
  db_id: number
  name: string
  email: string
  phone: string
  description: string
  full_address: string
  locality_name: string
  zone_id: number
  zone_name: string
  zone_number: number
  circle_name: string
  category: string
  criticality: string
  status: string
  assigned_admin_name: string
  created_at: string
  updated_at: string
  resolved_at: string | null
}

interface AdminInfo {
  id: number
  admin_id: string
  email: string
  name: string
  role: string
  department: string | null
  zone_id: number | null
  zone_name: string | null
  circle_id: number | null
  circle_name: string | null
}

interface Zone {
  id: number
  zone_number: number
  zone_name: string
}

export default function AdminDashboard() {
  const router = useRouter()
  const [department, setDepartment] = useState("all")
  const [departments, setDepartments] = useState<string[]>(["all"])
  const [complaints, setComplaints] = useState<Complaint[]>([])
  const [filteredComplaints, setFilteredComplaints] = useState<Complaint[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [zoneFilter, setZoneFilter] = useState("all")
  const [zones, setZones] = useState<Zone[]>([])
  const [sessionToken, setSessionToken] = useState<string | null>(null)
  const [adminInfo, setAdminInfo] = useState<AdminInfo | null>(null)
  const [categoryData, setCategoryData] = useState<any[]>([])
  const [statusData, setStatusData] = useState<any[]>([])
  const [selectedComplaint, setSelectedComplaint] = useState<Complaint | null>(null)
  const [showDetailsDialog, setShowDetailsDialog] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem("adminSessionToken")
    const storedAdmin = localStorage.getItem("adminInfo")

    if (!token) {
      router.push("/admin/login")
      return
    }

    setSessionToken(token)
    if (storedAdmin) {
      setAdminInfo(JSON.parse(storedAdmin))
    }
    
    fetchCategories()
    fetchZones()
  }, [router])

  useEffect(() => {
    if (sessionToken) {
      fetchComplaints()
    }
  }, [department, statusFilter, zoneFilter, sessionToken])

  useEffect(() => {
    filterComplaints()
    updateCharts()
  }, [searchTerm, complaints, department])

  const updateCharts = () => {
    // Category chart
    const categoryCount: { [key: string]: number } = {}
    complaints.forEach((complaint) => {
      const category = complaint.category || "Uncategorized"
      categoryCount[category] = (categoryCount[category] || 0) + 1
    })
    const categoryChartData = Object.entries(categoryCount).map(([name, value]) => ({
      name,
      value,
    }))
    setCategoryData(categoryChartData)

    // Status chart
    const filteredForStatus = department === "all" ? complaints : complaints.filter((c) => c.category === department)
    const statusCount: { [key: string]: number } = {}
    filteredForStatus.forEach((complaint) => {
      const status = complaint.status || "Unknown"
      statusCount[status] = (statusCount[status] || 0) + 1
    })
    const statusChartData = Object.entries(statusCount).map(([name, value]) => ({
      name,
      value,
    }))
    setStatusData(statusChartData)
  }

  const fetchZones = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      const response = await fetch(`${apiUrl}/api/zones`)
      const data = await response.json()
      if (data.success) {
        setZones(data.zones)
      }
    } catch (error) {
      console.error("[v0] Error fetching zones:", error)
    }
  }

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
    if (!sessionToken) return

    setLoading(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      let url = `${apiUrl}/api/admin/complaints?status=${statusFilter}`
      
      if (department !== "all") {
        url += `&department=${department}`
      }
      if (zoneFilter !== "all" && adminInfo?.role === "super_admin") {
        url += `&zone=${zoneFilter}`
      }

      const response = await fetch(url, {
        headers: {
          "X-Session-Token": sessionToken,
        },
      })

      if (response.status === 401) {
        localStorage.removeItem("adminSessionToken")
        localStorage.removeItem("adminInfo")
        router.push("/admin/login")
        return
      }

      const data = await response.json()

      if (data.success) {
        setComplaints(Array.isArray(data.complaints) ? data.complaints : [])
        if (data.admin_info) {
          setAdminInfo(prev => prev ? { ...prev, ...data.admin_info } : null)
        }
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
          c.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.locality_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          c.full_address?.toLowerCase().includes(searchTerm.toLowerCase()),
      )
    }
    setFilteredComplaints(filtered)
  }

  const handleStatusChange = async (complaintId: string, newStatus: string) => {
    if (!sessionToken) return

    // Find the complaint to check if it's resolved
    const complaint = complaints.find(c => c.id === complaintId)
    if (complaint?.status === "Resolved") {
      alert("Cannot modify resolved complaints")
      return
    }

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      const response = await fetch(`${apiUrl}/api/admin/complaints/${complaintId}/status`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-Session-Token": sessionToken,
        },
        body: JSON.stringify({ status: newStatus }),
      })

      const data = await response.json()

      if (response.ok) {
        fetchComplaints()
      } else {
        alert(data.error || "Error updating status")
      }
    } catch (error) {
      console.error("[v0] Error updating status:", error)
    }
  }

  const handleLogout = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      await fetch(`${apiUrl}/api/admin/logout`, {
        method: "POST",
        headers: {
          "X-Session-Token": sessionToken || "",
        },
      })
    } catch (error) {
      console.error("[v0] Logout error:", error)
    }
    
    localStorage.removeItem("adminSessionToken")
    localStorage.removeItem("adminInfo")
    router.push("/admin/login")
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

  const getRoleBadgeClass = (role: string) => {
    switch (role) {
      case "super_admin":
        return "bg-purple-900/20 text-purple-400 border-purple-700"
      case "sub_admin":
        return "bg-blue-900/20 text-blue-400 border-blue-700"
      case "department_admin":
        return "bg-green-900/20 text-green-400 border-green-700"
      default:
        return "bg-slate-900/20 text-slate-400 border-slate-700"
    }
  }

  const formatRoleName = (role: string) => {
    switch (role) {
      case "super_admin":
        return "Super Admin"
      case "sub_admin":
        return "Zone Admin"
      case "department_admin":
        return "Department Admin"
      default:
        return role
    }
  }

  const CHART_COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4", "#14b8a6"]

  const openComplaintDetails = (complaint: Complaint) => {
    setSelectedComplaint(complaint)
    setShowDetailsDialog(true)
  }

  if (loading && !complaints.length) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-300">Loading dashboard...</p>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header with Admin Info */}
        <div className="mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-white mb-1">Admin Dashboard</h1>
              <p className="text-slate-400">Manage complaints and track department performance</p>
            </div>
            <div className="flex gap-3">
              <Link href="/">
                <Button variant="outline" className="border-slate-600 text-white hover:bg-slate-700 bg-transparent">
                  Back to Home
                </Button>
              </Link>
              <Button onClick={handleLogout} className="bg-red-600 hover:bg-red-700 text-white">
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
          
          {/* Admin Info Card */}
          {adminInfo && (
            <Card className="bg-slate-800/50 border-slate-700 mt-4">
              <CardContent className="py-4">
                <div className="flex flex-wrap items-center gap-4">
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-slate-400" />
                    <span className="text-white font-medium">{adminInfo.name}</span>
                  </div>
                  <Badge className={`${getRoleBadgeClass(adminInfo.role)} border`}>
                    <Shield className="w-3 h-3 mr-1" />
                    {formatRoleName(adminInfo.role)}
                  </Badge>
                  {adminInfo.zone_name && (
                    <div className="flex items-center gap-1 text-slate-300">
                      <MapPin className="w-4 h-4 text-blue-400" />
                      <span>{adminInfo.zone_name}</span>
                    </div>
                  )}
                  {adminInfo.circle_name && (
                    <div className="flex items-center gap-1 text-slate-300">
                      <Building className="w-4 h-4 text-green-400" />
                      <span>{adminInfo.circle_name}</span>
                    </div>
                  )}
                  {adminInfo.department && (
                    <Badge className="bg-slate-700 text-slate-300 border-slate-600">
                      {adminInfo.department}
                    </Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Filters */}
        <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-4">
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
          
          {adminInfo?.role === "super_admin" && (
            <div>
              <label className="text-sm font-medium text-slate-300 block mb-2">Zone</label>
              <Select value={zoneFilter} onValueChange={setZoneFilter}>
                <SelectTrigger className="bg-slate-800 border-slate-700 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="all" className="text-white">All Zones</SelectItem>
                  {zones.map((zone) => (
                    <SelectItem key={zone.id} value={zone.id.toString()} className="text-white">
                      Zone {zone.zone_number}: {zone.zone_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
          
          <div>
            <label className="text-sm font-medium text-slate-300 block mb-2">Status</label>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="bg-slate-800 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="all" className="text-white">All Status</SelectItem>
                <SelectItem value="Pending" className="text-white">Pending</SelectItem>
                <SelectItem value="In Progress" className="text-white">In Progress</SelectItem>
                <SelectItem value="Resolved" className="text-white">Resolved</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div>
            <label className="text-sm font-medium text-slate-300 block mb-2">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
              <Input
                placeholder="Search by ID, name, email, location..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-slate-800 border-slate-700 text-white"
              />
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="mb-6 grid md:grid-cols-2 gap-6">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Complaints by Category</CardTitle>
              <CardDescription>Total complaints across all categories</CardDescription>
            </CardHeader>
            <CardContent className="flex justify-center">
              {categoryData.length > 0 ? (
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {categoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [`${value} complaints`, "Count"]} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-slate-400 py-8">No data available</p>
              )}
            </CardContent>
          </Card>

          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Complaints by Status</CardTitle>
              <CardDescription>{department === "all" ? "All departments" : `${department} department`}</CardDescription>
            </CardHeader>
            <CardContent className="flex justify-center">
              {statusData.length > 0 ? (
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={statusData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {statusData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [`${value} complaints`, "Count"]} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <p className="text-slate-400 py-8">No data available</p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Complaints Table */}
        <Card className="bg-slate-800 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white">Complaints Management</CardTitle>
            <CardDescription>
              {department === "all" ? "All departments" : department} - {filteredComplaints.length} complaint(s)
              {adminInfo?.role !== "super_admin" && adminInfo?.zone_name && ` in ${adminInfo.zone_name}`}
              {adminInfo?.role === "department_admin" && adminInfo?.circle_name && ` (${adminInfo.circle_name})`}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left py-3 px-2 text-slate-400">ID</th>
                    <th className="text-left py-3 px-2 text-slate-400">User Details</th>
                    <th className="text-left py-3 px-2 text-slate-400">Location</th>
                    <th className="text-left py-3 px-2 text-slate-400">Category</th>
                    <th className="text-left py-3 px-2 text-slate-400">Priority</th>
                    <th className="text-left py-3 px-2 text-slate-400">Status</th>
                    <th className="text-left py-3 px-2 text-slate-400">Date</th>
                    <th className="text-left py-3 px-2 text-slate-400">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={8} className="py-8 px-4 text-center text-slate-400">
                        Loading complaints...
                      </td>
                    </tr>
                  ) : filteredComplaints.length > 0 ? (
                    filteredComplaints.map((complaint) => (
                      <tr key={complaint.id} className="border-b border-slate-700 hover:bg-slate-700/50">
                        <td className="py-3 px-2">
                          <span className="text-white font-mono text-xs">{complaint.id}</span>
                        </td>
                        <td className="py-3 px-2">
                          <div className="space-y-1">
                            <p className="text-white font-medium">{complaint.name}</p>
                            <p className="text-xs text-slate-400 flex items-center gap-1">
                              <Mail className="w-3 h-3" /> {complaint.email}
                            </p>
                            <p className="text-xs text-slate-400 flex items-center gap-1">
                              <Phone className="w-3 h-3" /> {complaint.phone || "N/A"}
                            </p>
                          </div>
                        </td>
                        <td className="py-3 px-2">
                          <div className="space-y-1">
                            <p className="text-white text-xs flex items-center gap-1">
                              <MapPin className="w-3 h-3 text-blue-400" />
                              {complaint.locality_name || "N/A"}
                            </p>
                            <p className="text-xs text-slate-400">
                              Zone: {complaint.zone_name || "N/A"}
                            </p>
                            {complaint.full_address && (
                              <p className="text-xs text-slate-500 max-w-[150px] truncate" title={complaint.full_address}>
                                {complaint.full_address}
                              </p>
                            )}
                          </div>
                        </td>
                        <td className="py-3 px-2">
                          <span className="text-slate-300 text-xs">{complaint.category}</span>
                        </td>
                        <td className="py-3 px-2">
                          {complaint.criticality === "Critical" && (
                            <Badge className={`${getPriorityBadgeClass("Critical")} border flex items-center gap-1 w-fit`}>
                              <AlertCircle className="w-3 h-3" />
                              CRITICAL
                            </Badge>
                          )}
                        </td>
                        <td className="py-3 px-2">
                          <Select
                            value={complaint.status}
                            onValueChange={(value) => handleStatusChange(complaint.id, value)}
                            disabled={complaint.status === "Resolved"}
                          >
                            <SelectTrigger
                              className={`w-28 h-7 text-xs ${getStatusBadgeClass(complaint.status)} border ${complaint.status === "Resolved" ? "opacity-60 cursor-not-allowed" : ""}`}
                            >
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent className="bg-slate-800 border-slate-700">
                              <SelectItem value="Pending" className="text-white text-xs">Pending</SelectItem>
                              <SelectItem value="In Progress" className="text-white text-xs">In Progress</SelectItem>
                              <SelectItem value="Resolved" className="text-white text-xs">Resolved</SelectItem>
                            </SelectContent>
                          </Select>
                          {complaint.status === "Resolved" && (
                            <p className="text-xs text-slate-500 mt-1">Locked</p>
                          )}
                        </td>
                        <td className="py-3 px-2">
                          <div className="flex items-center gap-1 text-slate-400 text-xs">
                            <Clock className="w-3 h-3" />
                            {new Date(complaint.created_at).toLocaleDateString()}
                          </div>
                        </td>
                        <td className="py-3 px-2">
                          <Button
                            size="sm"
                            variant="outline"
                            className="border-slate-600 text-slate-300 hover:bg-slate-700 text-xs h-7 bg-transparent"
                            onClick={() => openComplaintDetails(complaint)}
                          >
                            View
                          </Button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={8} className="py-8 px-4 text-center text-slate-400">
                        No complaints found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Complaint Details Dialog */}
        <Dialog open={showDetailsDialog} onOpenChange={setShowDetailsDialog}>
          <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                Complaint Details
                {selectedComplaint?.criticality === "Critical" && (
                  <Badge className="bg-red-900/20 text-red-400 border-red-700 border">
                    <AlertCircle className="w-3 h-3 mr-1" />
                    CRITICAL
                  </Badge>
                )}
              </DialogTitle>
              <DialogDescription>
                Full details for complaint {selectedComplaint?.id}
              </DialogDescription>
            </DialogHeader>
            
            {selectedComplaint && (
              <div className="space-y-4 mt-4">
                {/* Complainant Info */}
                <div className="bg-slate-700/50 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-slate-400 mb-3">Complainant Information</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs text-slate-500">Name</p>
                      <p className="text-white font-medium">{selectedComplaint.name}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Email</p>
                      <p className="text-white">{selectedComplaint.email}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Phone</p>
                      <p className="text-white">{selectedComplaint.phone || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Complaint ID</p>
                      <p className="text-blue-400 font-mono">{selectedComplaint.id}</p>
                    </div>
                  </div>
                </div>

                {/* Location Info */}
                <div className="bg-slate-700/50 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-slate-400 mb-3">Location Details</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs text-slate-500">Zone</p>
                      <p className="text-white">
                        {selectedComplaint.zone_name ? `${selectedComplaint.zone_name} (Zone ${selectedComplaint.zone_number})` : "N/A"}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Circle</p>
                      <p className="text-white">{selectedComplaint.circle_name || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Locality</p>
                      <p className="text-white">{selectedComplaint.locality_name || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Assigned Admin</p>
                      <p className="text-white">{selectedComplaint.assigned_admin_name || "Not Assigned"}</p>
                    </div>
                  </div>
                  {selectedComplaint.full_address && (
                    <div className="mt-3">
                      <p className="text-xs text-slate-500">Complete Address</p>
                      <p className="text-white mt-1">{selectedComplaint.full_address}</p>
                    </div>
                  )}
                </div>

                {/* Complaint Info */}
                <div className="bg-slate-700/50 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-slate-400 mb-3">Complaint Details</h3>
                  <div className="grid grid-cols-2 gap-4 mb-3">
                    <div>
                      <p className="text-xs text-slate-500">Category</p>
                      <p className="text-white">{selectedComplaint.category}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Status</p>
                      <Badge className={`${getStatusBadgeClass(selectedComplaint.status)} border`}>
                        {selectedComplaint.status}
                      </Badge>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Created At</p>
                      <p className="text-white">{new Date(selectedComplaint.created_at).toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Last Updated</p>
                      <p className="text-white">{new Date(selectedComplaint.updated_at).toLocaleString()}</p>
                    </div>
                    {selectedComplaint.resolved_at && (
                      <div>
                        <p className="text-xs text-slate-500">Resolved At</p>
                        <p className="text-green-400">{new Date(selectedComplaint.resolved_at).toLocaleString()}</p>
                      </div>
                    )}
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 mb-1">Description</p>
                    <p className="text-white bg-slate-800 rounded p-3">{selectedComplaint.description}</p>
                  </div>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </main>
  )
}
