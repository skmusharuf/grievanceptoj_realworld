"use client"
import { useState } from "react"
import type React from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Shield, AlertCircle } from "lucide-react"
import Link from "next/link"

export default function AdminLogin() {
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"
      const response = await fetch(`${apiUrl}/api/admin/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        setError(data.error || "Login failed")
        setLoading(false)
        return
      }

      // Store session token and admin info
      localStorage.setItem("adminSessionToken", data.session_token)
      if (data.admin) {
        localStorage.setItem("adminInfo", JSON.stringify(data.admin))
      }

      // Redirect to admin dashboard
      router.push("/admin/dashboard")
    } catch (err) {
      setError("Connection error. Make sure the backend is running.")
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <Card className="w-full max-w-md bg-slate-800 border-slate-700">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <Shield className="w-8 h-8 text-blue-500" />
          </div>
          <CardTitle className="text-white text-2xl">Admin Portal</CardTitle>
          <CardDescription className="text-slate-400">
            Multi-level admin access for Hyderabad Grievance System
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            {error && (
              <div className="bg-red-900/20 border border-red-700 rounded p-3 flex gap-2 items-start">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Email</label>
              <Input
                type="email"
                placeholder="admin@grievancehub.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-500"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Password</label>
              <Input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-500"
                required
              />
            </div>

            <Button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white">
              {loading ? "Logging in..." : "Login"}
            </Button>

            <div className="text-center text-sm">
              <p className="text-slate-400">
                Not an admin?{" "}
                <Link href="/" className="text-blue-400 hover:text-blue-300">
                  Back to home
                </Link>
              </p>
            </div>
          </form>

          <div className="mt-6 space-y-3">
            <div className="p-3 bg-purple-900/20 border border-purple-700 rounded text-xs text-purple-300">
              <p className="font-semibold mb-1">Super Admin (All Zones):</p>
              <p>Email: superadmin@grievancehub.com</p>
              <p>Password: superadmin@123</p>
            </div>
            
            <div className="p-3 bg-blue-900/20 border border-blue-700 rounded text-xs text-blue-300">
              <p className="font-semibold mb-1">Zone Admin (Zone 1 - Malkajgiri):</p>
              <p>Email: zone1admin@grievancehub.com</p>
              <p>Password: zone1admin@123</p>
            </div>
            
            <div className="p-3 bg-green-900/20 border border-green-700 rounded text-xs text-green-300">
              <p className="font-semibold mb-1">Department Admin (Circle 1):</p>
              <p>Email: dept1@grievancehub.com</p>
              <p>Password: dept1admin@123</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </main>
  )
}
