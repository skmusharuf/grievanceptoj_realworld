"use client"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowRight, FileText, BarChart3, Shield, Zap } from "lucide-react"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Navigation */}
      <nav className="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Shield className="w-8 h-8 text-blue-500" />
            <span className="text-xl font-bold text-white">GrievanceHub</span>
          </div>
          <div className="flex gap-4">
            <Link href="/admin/login">
              <Button variant="ghost" className="text-slate-300 hover:text-white">
                Admin
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">Your Voice Matters</h1>
          <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
            Submit grievances easily, track progress in real-time, and get resolutions faster with our intelligent
            redressal system.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/submit-complaint">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white">
                Submit Complaint <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
            </Link>
            <Link href="/track">
              <Button
                size="lg"
                variant="outline"
                className="border-slate-600 text-white hover:bg-slate-800 bg-transparent"
              >
                Track Complaint
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-20">
          <Card className="bg-slate-800 border-slate-700 hover:border-blue-500 transition-colors">
            <CardHeader>
              <FileText className="w-8 h-8 text-blue-500 mb-2" />
              <CardTitle className="text-white">Easy Submission</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-slate-400">Submit complaints with text or voice in multiple languages</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800 border-slate-700 hover:border-blue-500 transition-colors">
            <CardHeader>
              <Zap className="w-8 h-8 text-blue-500 mb-2" />
              <CardTitle className="text-white">Smart Classification</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-slate-400">AI-powered categorization and priority detection</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800 border-slate-700 hover:border-blue-500 transition-colors">
            <CardHeader>
              <BarChart3 className="w-8 h-8 text-blue-500 mb-2" />
              <CardTitle className="text-white">Real-time Tracking</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-slate-400">Monitor your complaint status anytime, anywhere</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-800 border-slate-700 hover:border-blue-500 transition-colors">
            <CardHeader>
              <Shield className="w-8 h-8 text-blue-500 mb-2" />
              <CardTitle className="text-white">Secure & Private</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-slate-400">OTP verification and encrypted data storage</p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-slate-800/50 border-y border-slate-700 py-16 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-500 mb-2">10,000+</div>
              <p className="text-slate-400">Complaints Resolved</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-500 mb-2">98%</div>
              <p className="text-slate-400">Satisfaction Rate</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-500 mb-2">24/7</div>
              <p className="text-slate-400">Support Available</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-700 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-slate-400">
          <p>&copy; 2025 GrievanceHub. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}
