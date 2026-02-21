"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Search, Clock, CheckCircle, AlertCircle } from "lucide-react"
import Link from "next/link"

export default function TrackComplaint() {
  const [complaintId, setComplaintId] = useState("")
  const [email, setEmail] = useState("")
  const [otp, setOtp] = useState("") // Added OTP state for tracking verification
  const [complaint, setComplaint] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleTrack = async () => {
    if (!complaintId.trim() || !email.trim() || !otp.trim()) {
      // Updated validation to include OTP
      setError("Please enter complaint ID, email, and OTP")
      return
    }

    setLoading(true)
    setError("")
    setComplaint(null)

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/complaints/track`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            complaint_id: complaintId,
            email: email,
            otp: otp, // Added OTP to request body
          }),
        },
      )
      const data = await response.json()

      if (response.ok && data.success) {
        setComplaint(data.complaint)
      } else {
        setError(data.error || "Invalid OTP or complaint not found")
      }
    } catch (err) {
      setError("Error tracking complaint. Please try again.")
    }

    setLoading(false)
  }

  const getStatusIcon = (status: string) => {
    switch (status?.toLowerCase()) {
      case "resolved":
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case "in_progress":
      case "in-progress":
        return <Clock className="w-5 h-5 text-blue-500" />
      case "pending":
        return <AlertCircle className="w-5 h-5 text-yellow-500" />
      default:
        return <Clock className="w-5 h-5 text-slate-500" />
    }
  }

  const getStatusBadgeClass = (status: string) => {
    switch (status?.toLowerCase()) {
      case "resolved":
        return "bg-green-900/20 text-green-400 border-green-700"
      case "in_progress":
      case "in-progress":
        return "bg-blue-900/20 text-blue-400 border-blue-700"
      case "pending":
        return "bg-yellow-900/20 text-yellow-400 border-yellow-700"
      default:
        return "bg-slate-900/20 text-slate-400 border-slate-700"
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 py-12">
      <div className="max-w-3xl mx-auto px-4">
        <div className="mb-8">
          <Link href="/">
            <Button variant="ghost" className="text-slate-300 hover:text-white mb-4">
              ← Back to Home
            </Button>
          </Link>
          <h1 className="text-4xl font-bold text-white mb-2">Track Your Complaint</h1>
          <p className="text-slate-400">Enter your complaint ID, email, and OTP to check the status</p>{" "}
          {/* Updated description to mention OTP */}
        </div>

        <Card className="bg-slate-800 border-slate-700 mb-6">
          <CardHeader>
            <CardTitle className="text-white">Search Complaint</CardTitle>
            <CardDescription>Enter your complaint details to track status</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <Input
                value={complaintId}
                onChange={(e) => setComplaintId(e.target.value)}
                placeholder="Complaint ID (e.g., CMP00818268)"
                className="bg-slate-700 border-slate-600 text-white"
              />
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email Address"
                className="bg-slate-700 border-slate-600 text-white"
              />
              <Input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="OTP (sent to your email)"
                className="bg-slate-700 border-slate-600 text-white"
                onKeyPress={(e) => e.key === "Enter" && handleTrack()}
              />{" "}
              {/* Added OTP input field */}
            </div>

            <Button onClick={handleTrack} disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700">
              <Search className="w-4 h-4 mr-2" />
              {loading ? "Searching..." : "Track Complaint"}
            </Button>

            {error && (
              <Alert className="bg-red-900/20 border-red-700">
                <AlertDescription className="text-red-400">{error}</AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {complaint && (
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-white">Complaint Details</CardTitle>
                <Badge className={`${getStatusBadgeClass(complaint.status)} border`}>
                  {complaint.status?.replace("_", " ").toUpperCase()}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-slate-400">Complaint ID</p>
                  <p className="text-white font-mono">{complaint.id}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Category</p>
                  <p className="text-white">{complaint.category}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Criticality</p>
                  <Badge
                    className={
                      complaint.criticality === "Critical"
                        ? "bg-red-900/20 text-red-400"
                        : "bg-green-900/20 text-green-400"
                    }
                  >
                    {complaint.criticality}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Status</p>
                  <p className="text-white">{complaint.status}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Submitted On</p>
                  <p className="text-white">{new Date(complaint.created_at).toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400">Last Updated</p>
                  <p className="text-white">{new Date(complaint.updated_at).toLocaleString()}</p>
                </div>
              </div>

              <div>
                <p className="text-sm text-slate-400 mb-2">Description</p>
                <p className="text-white bg-slate-700 p-4 rounded-lg">{complaint.description}</p>
              </div>

              {complaint.criticality === "Critical" && (
                <Alert className="bg-red-900/20 border-red-700">
                  <AlertDescription className="text-red-400 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4" />
                    This complaint has been marked as CRITICAL and will be prioritized.
                  </AlertDescription>
                </Alert>
              )}

              {/* Status Timeline */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-white">Status Timeline</h3>
                <div className="space-y-3">
                  <div className="flex items-start gap-3">
                    {getStatusIcon("pending")}
                    <div>
                      <p className="text-white font-medium">Complaint Submitted</p>
                      <p className="text-sm text-slate-400">{new Date(complaint.created_at).toLocaleString()}</p>
                    </div>
                  </div>

                  {(complaint.status === "In Progress" || complaint.status === "Resolved") && (
                    <div className="flex items-start gap-3">
                      {getStatusIcon("in_progress")}
                      <div>
                        <p className="text-white font-medium">Under Review</p>
                        <p className="text-sm text-slate-400">Department is working on your complaint</p>
                      </div>
                    </div>
                  )}

                  {complaint.status === "Resolved" && (
                    <div className="flex items-start gap-3">
                      {getStatusIcon("resolved")}
                      <div>
                        <p className="text-white font-medium">Resolved</p>
                        <p className="text-sm text-slate-400">{new Date(complaint.updated_at).toLocaleString()}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  )
}
