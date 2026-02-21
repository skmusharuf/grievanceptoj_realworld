"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Mic, MicOff, Loader2 } from "lucide-react"

interface ComplaintFormProps {
  onSubmit: (data: { description: string }) => void
  loading: boolean
  message?: string
}

export function ComplaintForm({ onSubmit, loading, message }: ComplaintFormProps) {
  const [description, setDescription] = useState("")
  const [isListening, setIsListening] = useState(false)
  const [language, setLanguage] = useState<"en-IN" | "hi-IN" | "te-IN">("en-IN")
  const [voiceError, setVoiceError] = useState("")
  const [browserSupport, setBrowserSupport] = useState(true)
  const recognitionRef = useRef<any>(null)

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
      if (!SpeechRecognition) {
        setBrowserSupport(false)
        setVoiceError("Voice input not supported in this browser. Please use Chrome or Edge.")
        return
      }

      // Initialize speech recognition
      const recognition = new SpeechRecognition()
      recognition.continuous = true // Keep listening
      recognition.interimResults = true // Show results in real-time
      recognition.lang = language

      recognition.onresult = (event: any) => {
        let interimTranscript = ""
        let finalTranscript = ""

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript
          if (event.results[i].isFinal) {
            finalTranscript += transcript + " "
          } else {
            interimTranscript += transcript
          }
        }

        if (finalTranscript) {
          setDescription((prev) => prev + finalTranscript)
        }
      }

      recognition.onerror = (event: any) => {
        console.error("[v0] Speech recognition error:", event.error)
        if (event.error === "no-speech") {
          setVoiceError("No speech detected. Please try again.")
        } else if (event.error === "not-allowed") {
          setVoiceError("Microphone access denied. Please allow microphone permissions.")
        } else {
          setVoiceError("Voice input error. Please try again.")
        }
        setIsListening(false)
      }

      recognition.onend = () => {
        setIsListening(false)
      }

      recognitionRef.current = recognition
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [language])

  const startListening = () => {
    if (!recognitionRef.current) return

    try {
      setVoiceError("")
      recognitionRef.current.lang = language
      recognitionRef.current.start()
      setIsListening(true)
    } catch (error) {
      console.error("[v0] Error starting recognition:", error)
      setVoiceError("Could not start voice input. Please try again.")
    }
  }

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    }
  }

  const handleLanguageChange = (newLang: "en-IN" | "hi-IN" | "te-IN") => {
    if (isListening) {
      stopListening()
    }
    setLanguage(newLang)
  }

  const handleSubmit = () => {
    if (description.trim()) {
      onSubmit({ description: description.trim() })
    }
  }

  return (
    <Card className="bg-slate-800 border-slate-700">
      <CardHeader>
        <CardTitle className="text-white">Describe Your Complaint</CardTitle>
        <CardDescription>
          Type or speak your complaint in Telugu, Hindi, or English. Our AI will automatically classify it.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Language Selection */}
        <div>
          <label className="text-sm font-medium text-slate-300 block mb-2">Select Language for Voice Input</label>
          <div className="flex gap-2">
            <Button
              type="button"
              variant={language === "en-IN" ? "default" : "outline"}
              onClick={() => handleLanguageChange("en-IN")}
              disabled={isListening}
              className={
                language === "en-IN"
                  ? "bg-blue-600 hover:bg-blue-700"
                  : "border-slate-600 text-slate-300 hover:bg-slate-700"
              }
            >
              English
            </Button>
            <Button
              type="button"
              variant={language === "hi-IN" ? "default" : "outline"}
              onClick={() => handleLanguageChange("hi-IN")}
              disabled={isListening}
              className={
                language === "hi-IN"
                  ? "bg-blue-600 hover:bg-blue-700"
                  : "border-slate-600 text-slate-300 hover:bg-slate-700"
              }
            >
              हिंदी
            </Button>
            <Button
              type="button"
              variant={language === "te-IN" ? "default" : "outline"}
              onClick={() => handleLanguageChange("te-IN")}
              disabled={isListening}
              className={
                language === "te-IN"
                  ? "bg-blue-600 hover:bg-blue-700"
                  : "border-slate-600 text-slate-300 hover:bg-slate-700"
              }
            >
              తెలుగు
            </Button>
          </div>
        </div>

        {/* Description Input */}
        <div>
          <label className="text-sm font-medium text-slate-300 block mb-2">Complaint Description *</label>
          <Textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe your complaint in detail... (Type or use voice input)"
            className="bg-slate-700 border-slate-600 text-white min-h-[150px]"
            rows={6}
          />
          {isListening && (
            <p className="text-xs text-green-400 mt-1 flex items-center gap-2">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              Listening... Speak clearly in{" "}
              {language === "en-IN" ? "English" : language === "hi-IN" ? "Hindi" : "Telugu"}
            </p>
          )}
        </div>

        {/* Voice Input Button */}
        {browserSupport && (
          <div className="flex items-center gap-2">
            <Button
              type="button"
              onClick={isListening ? stopListening : startListening}
              disabled={loading}
              className={`flex items-center gap-2 ${
                isListening ? "bg-red-600 hover:bg-red-700" : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {isListening ? (
                <>
                  <MicOff className="w-4 h-4" />
                  Stop Voice Input
                </>
              ) : (
                <>
                  <Mic className="w-4 h-4" />
                  Start Voice Input
                </>
              )}
            </Button>
            {isListening && (
              <span className="text-green-400 text-sm flex items-center gap-2">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                Listening...
              </span>
            )}
          </div>
        )}

        {voiceError && (
          <Alert className="bg-red-900/20 border-red-700">
            <AlertDescription className="text-red-400">{voiceError}</AlertDescription>
          </Alert>
        )}

        {/* Info Alert */}
        <Alert className="bg-blue-900/20 border-blue-700">
          <AlertDescription className="text-blue-400">
            ℹ️ No need to select a category - our AI will automatically classify your complaint using Naive Bayes and
            assign criticality using Logistic Regression.
          </AlertDescription>
        </Alert>

        {message && (
          <Alert className="bg-red-900/20 border-red-700">
            <AlertDescription className="text-red-400">{message}</AlertDescription>
          </Alert>
        )}

        <Button
          onClick={handleSubmit}
          disabled={!description.trim() || loading}
          className="w-full bg-blue-600 hover:bg-blue-700"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Submitting...
            </>
          ) : (
            "Submit Complaint"
          )}
        </Button>
      </CardContent>
    </Card>
  )
}
