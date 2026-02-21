"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { CheckCircle, Search, MapPin, Loader2 } from "lucide-react"
import Link from "next/link"
import { ComplaintForm } from "@/components/complaint-form"

interface Area {
  id: number
  area_name: string
  ward_number: number
  zone_id: number
  zone_name: string
  zone_number: number
  circle_name: string
  display_name: string
}

export default function SubmitComplaint() {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    email: "",
    aadhar: "",
    full_address: "",
    area_id: null as number | null,
  })
  const [otp, setOtp] = useState("")
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")
  const [complaintId, setComplaintId] = useState("")
  const [complaintDetails, setComplaintDetails] = useState<{
    zone?: string
    locality?: string
    category?: string
    criticality?: string
  }>({})
  
  // Area search state
  const [areaSearch, setAreaSearch] = useState("")
  const [areas, setAreas] = useState<Area[]>([])
  const [selectedArea, setSelectedArea] = useState<Area | null>(null)
  const [showAreaDropdown, setShowAreaDropdown] = useState(false)
  const [loadingAreas, setLoadingAreas] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowAreaDropdown(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  // Search areas when typing
  useEffect(() => {
    const searchAreas = async () => {
      if (areaSearch.length < 2) {
        setAreas([])
        return
      }
      
      setLoadingAreas(true)
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/areas?search=${encodeURIComponent(areaSearch)}`
        )
        const data = await response.json()
        if (data.success) {
          setAreas(data.areas)
          setShowAreaDropdown(true)
        }
      } catch (error) {
        console.error("[v0] Error searching areas:", error)
      }
      setLoadingAreas(false)
    }

    const debounce = setTimeout(searchAreas, 300)
    return () => clearTimeout(debounce)
  }, [areaSearch])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleAreaSelect = (area: Area) => {
    setSelectedArea(area)
    setFormData((prev) => ({ ...prev, area_id: area.id }))
    setAreaSearch(area.area_name)
    setShowAreaDropdown(false)
  }

  const handleSendOTP = async () => {
    setLoading(true)
    setMessage("")
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/auth/send-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: formData.email }),
      })

      if (response.ok) {
        setMessage("OTP sent to your email")
        setStep(2)
      } else {
        setMessage("Error sending OTP")
      }
    } catch (error) {
      setMessage("Error: Failed to fetch")
    }
    setLoading(false)
  }

  const handleVerifyOTP = async () => {
    setLoading(true)
    setMessage("")
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/auth/verify-otp`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: formData.email, otp }),
        },
      )

      if (response.ok) {
        setMessage("OTP verified successfully")
        setStep(3)
      } else {
        setMessage("Invalid OTP")
      }
    } catch (error) {
      setMessage("Error: Failed to fetch")
    }
    setLoading(false)
  }

  const handleSubmitComplaint = async (complaintData: { description: string }) => {
    setLoading(true)
    setMessage("")

    console.log("[v0] Submitting complaint with data:", {
      ...formData,
      ...complaintData,
    })

    try {
      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}/api/complaints/submit`
      console.log("[v0] API URL:", apiUrl)

      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          ...complaintData,
        }),
      })

      console.log("[v0] Response status:", response.status)

      const data = await response.json()
      console.log("[v0] Response data:", data)

      if (response.ok) {
        setComplaintId(data.complaint_id)
        setComplaintDetails({
          zone: data.zone,
          locality: data.locality,
          category: data.category,
          criticality: data.criticality,
        })
        setMessage("Complaint submitted successfully!")
        setStep(4)
      } else {
        setMessage(data.error || "Error submitting complaint")
      }
    } catch (error) {
      console.error("[v0] Error submitting complaint:", error)
      setMessage("Error: Failed to fetch")
    }
    setLoading(false)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 py-12">
      <div className="max-w-2xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <Link href="/">
            <Button variant="ghost" className="text-slate-300 hover:text-white mb-4">
              ← Back to Home
            </Button>
          </Link>
          <h1 className="text-4xl font-bold text-white mb-2">Submit Your Grievance</h1>
          <p className="text-slate-400">Step {step} of 4</p>
        </div>

        {/* Progress Bar */}
        <div className="flex gap-2 mb-8">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className={`h-2 flex-1 rounded-full transition-colors ${i <= step ? "bg-blue-500" : "bg-slate-700"}`}
            />
          ))}
        </div>

        {/* Step 1: Personal Information with Address */}
        {step === 1 && (
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Personal Information & Location</CardTitle>
              <CardDescription>Please provide your details and address</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-slate-300">Full Name *</label>
                  <Input
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="Enter your full name"
                    className="bg-slate-700 border-slate-600 text-white mt-1"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-300">Phone Number *</label>
                  <Input
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    placeholder="Enter your phone number"
                    className="bg-slate-700 border-slate-600 text-white mt-1"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-slate-300">Email *</label>
                  <Input
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="Enter your email"
                    className="bg-slate-700 border-slate-600 text-white mt-1"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-300">Aadhar Number *</label>
                  <Input
                    name="aadhar"
                    value={formData.aadhar}
                    onChange={handleInputChange}
                    placeholder="Enter your 12-digit Aadhar"
                    maxLength={12}
                    className="bg-slate-700 border-slate-600 text-white mt-1"
                  />
                </div>
              </div>

              {/* Area/Locality Search */}
              <div className="relative" ref={dropdownRef}>
                <label className="text-sm font-medium text-slate-300 block mb-1">
                  Select Your Area/Locality in Hyderabad *
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                  <Input
                    value={areaSearch}
                    onChange={(e) => {
                      setAreaSearch(e.target.value)
                      if (selectedArea && e.target.value !== selectedArea.area_name) {
                        setSelectedArea(null)
                        setFormData((prev) => ({ ...prev, area_id: null }))
                      }
                    }}
                    onFocus={() => areaSearch.length >= 2 && setShowAreaDropdown(true)}
                    placeholder="Type to search (e.g., Miyapur, Kukatpally, Secunderabad...)"
                    className="pl-10 bg-slate-700 border-slate-600 text-white"
                  />
                  {loadingAreas && (
                    <Loader2 className="absolute right-3 top-3 h-4 w-4 text-slate-400 animate-spin" />
                  )}
                </div>
                
                {/* Area Dropdown */}
                {showAreaDropdown && areas.length > 0 && (
                  <div className="absolute z-50 w-full mt-1 bg-slate-700 border border-slate-600 rounded-md shadow-lg max-h-60 overflow-y-auto">
                    {areas.map((area) => (
                      <button
                        key={area.id}
                        type="button"
                        onClick={() => handleAreaSelect(area)}
                        className="w-full px-4 py-3 text-left hover:bg-slate-600 transition-colors border-b border-slate-600 last:border-0"
                      >
                        <div className="flex items-start gap-2">
                          <MapPin className="h-4 w-4 text-blue-400 mt-0.5 flex-shrink-0" />
                          <div>
                            <p className="text-white font-medium">{area.area_name}</p>
                            <p className="text-xs text-slate-400">
                              Zone {area.zone_number}: {area.zone_name} | Circle: {area.circle_name}
                            </p>
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
                
                {areaSearch.length >= 2 && areas.length === 0 && !loadingAreas && (
                  <div className="absolute z-50 w-full mt-1 bg-slate-700 border border-slate-600 rounded-md shadow-lg p-4 text-center">
                    <p className="text-slate-400">No areas found. Try a different search term.</p>
                  </div>
                )}
              </div>

              {/* Selected Area Display */}
              {selectedArea && (
                <div className="bg-slate-700/50 border border-blue-500/30 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <MapPin className="h-5 w-5 text-blue-400" />
                    <span className="text-white font-medium">Selected Location</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>
                      <span className="text-slate-400">Area:</span>
                      <span className="text-white ml-2">{selectedArea.area_name}</span>
                    </div>
                    <div>
                      <span className="text-slate-400">Ward:</span>
                      <span className="text-white ml-2">{selectedArea.ward_number}</span>
                    </div>
                    <div>
                      <span className="text-slate-400">Zone:</span>
                      <span className="text-white ml-2">{selectedArea.zone_name}</span>
                    </div>
                    <div>
                      <span className="text-slate-400">Circle:</span>
                      <span className="text-white ml-2">{selectedArea.circle_name}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Full Address */}
              <div>
                <label className="text-sm font-medium text-slate-300 block mb-1">
                  Complete Address *
                </label>
                <Textarea
                  name="full_address"
                  value={formData.full_address}
                  onChange={handleInputChange}
                  placeholder="Enter your complete address (House No., Street, Landmark, etc.)"
                  className="bg-slate-700 border-slate-600 text-white min-h-[100px]"
                  rows={3}
                />
              </div>

              {message && (
                <Alert className="bg-red-900/20 border-red-700">
                  <AlertDescription className="text-red-400">{message}</AlertDescription>
                </Alert>
              )}
              
              <Button
                onClick={handleSendOTP}
                disabled={
                  !formData.name || 
                  !formData.phone || 
                  !formData.email || 
                  !formData.aadhar || 
                  !formData.area_id ||
                  !formData.full_address ||
                  loading
                }
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                {loading ? "Sending OTP..." : "Send OTP"}
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Step 2: OTP Verification */}
        {step === 2 && (
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Verify OTP</CardTitle>
              <CardDescription>Enter the OTP sent to {formData.email}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-slate-300">OTP *</label>
                <Input
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  placeholder="Enter 6-digit OTP"
                  className="bg-slate-700 border-slate-600 text-white mt-1"
                  maxLength={6}
                />
              </div>
              {message && (
                <Alert
                  className={
                    message.includes("successfully")
                      ? "bg-green-900/20 border-green-700"
                      : "bg-red-900/20 border-red-700"
                  }
                >
                  <AlertDescription className={message.includes("successfully") ? "text-green-400" : "text-red-400"}>
                    {message}
                  </AlertDescription>
                </Alert>
              )}
              <Button
                onClick={handleVerifyOTP}
                disabled={otp.length !== 6 || loading}
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                {loading ? "Verifying..." : "Verify OTP"}
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Complaint Description with Voice Input */}
        {step === 3 && <ComplaintForm onSubmit={handleSubmitComplaint} loading={loading} message={message} />}

        {/* Step 4: Success */}
        {step === 4 && (
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <CheckCircle className="w-6 h-6 text-green-500" />
                Complaint Submitted Successfully
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-slate-700 rounded-lg p-4 space-y-3">
                <div>
                  <p className="text-sm text-slate-400">Your Complaint ID</p>
                  <p className="text-2xl font-bold text-blue-400">{complaintId}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-600">
                  <div>
                    <p className="text-xs text-slate-400">Category</p>
                    <p className="text-white">{complaintDetails.category || 'Processing...'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-400">Criticality</p>
                    <p className={complaintDetails.criticality === 'Critical' ? 'text-red-400' : 'text-green-400'}>
                      {complaintDetails.criticality || 'Processing...'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-400">Zone</p>
                    <p className="text-white">{complaintDetails.zone || selectedArea?.zone_name || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-400">Locality</p>
                    <p className="text-white">{complaintDetails.locality || selectedArea?.area_name || 'N/A'}</p>
                  </div>
                </div>
              </div>
              
              <Alert className="bg-blue-900/20 border-blue-700">
                <AlertDescription className="text-blue-400">
                  Your grievance has been automatically classified and assigned to the appropriate zone admin. 
                  You will receive email updates when the status changes.
                </AlertDescription>
              </Alert>
              
              <p className="text-slate-300">
                Your complaint has been assigned to <strong className="text-white">{complaintDetails.zone || selectedArea?.zone_name}</strong> zone 
                and will be handled by the concerned department.
              </p>
              
              <div className="flex gap-3">
                <Link href="/track" className="flex-1">
                  <Button className="w-full bg-blue-600 hover:bg-blue-700">Track Complaint</Button>
                </Link>
                <Link href="/" className="flex-1">
                  <Button
                    variant="outline"
                    className="w-full border-slate-600 text-white hover:bg-slate-700 bg-transparent"
                  >
                    Back to Home
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  )
}
