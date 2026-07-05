import { useState } from "react"
import Waveform from "./waveform"

const API_URL = "http://localhost:8000"
function App() {

  const [song, setSong] = useState("")
  const [loading, setLoading] = useState(false)
  const [score, setScore] = useState(0)
  const [error, setError] = useState("") 
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadMessage, setUploadMessage] = useState("")
  const [uploading, setUploading] = useState(false)

    async function identifySong() {

    setLoading(true)
    setSong("")
    setScore(0)
    setError("")

    // 1. Ask browser for mic permission
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

    // 2. Record for 8 seconds
    const recorder = new MediaRecorder(stream)
    const chunks = []

    recorder.ondataavailable = (e) => chunks.push(e.data)

    recorder.onstop = async () => {
      // 3. Stop all mic tracks
      stream.getTracks().forEach(t => t.stop())

      // 4. Build a .wav blob and send it to /identify
      const blob = new Blob(chunks, { type: "audio/wav" })
      const formData = new FormData()
      formData.append("audio", blob, "query.wav")

      try {
        const response = await fetch(`${API_URL}/identify`, {
          method: "POST",
          body: formData
        })

        const data = await response.json()
        console.log(data)

        if (data.detected_song === "No match found") {
          setError("❌ No match found. Try again!")
        } else {
          setSong(data.detected_song)
          setScore(data.match_score)
        }
      } catch (err) {
        setError("❌ Server error. Is the backend running?")
      }

      setLoading(false)
    }

    // 5. Start recording, stop after 8 seconds
    recorder.start()
    setTimeout(() => recorder.stop(), 10000)
    }


  async function addSong() {

    if (!selectedFile) {
      alert("Please select a file")
      return
    }

    setUploading(true)
    setUploadMessage("⏳ Adding Song...")

    const formData = new FormData()

    formData.append(
      "song",
      selectedFile
    )

    const response = await fetch(`${API_URL}/add-song`,
      {
        method: "POST",
        body: formData
      }
    )

    const data = await response.json()

    console.log(data)

    setUploadMessage(
      data.message
    )

    setSelectedFile(null)
    setUploading(false)
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        background:
          "linear-gradient(135deg, #111827, #1e3a8a)",
        color: "white",
        fontFamily: "Arial",
      }}
    >

      <h1
        style={{
          fontSize: "4rem",
          marginBottom: "2rem",
          textShadow:
            "0 0 20px rgba(255,255,255,0.3)",
        }}
      >
        🎵 SonicHash
      </h1>

     <div
  style={{
    position: "absolute",
    top: "20px",
    right: "20px",
    width: "300px",
    backgroundColor: "#1f2937",
    padding: "1rem",
    borderRadius: "16px",
    boxShadow: "0 8px 25px rgba(0,0,0,0.3)"
  }}
>
  <h3
    style={{
      marginTop: 0,
      marginBottom: "1rem",
      textAlign: "center"
    }}
  >
    📁 Add Song
  </h3>

  <input
    type="file"
    accept=".wav, .mp3"
    onChange={(event) =>
      setSelectedFile(
        event.target.files[0]
      )
    }
    style={{
      width: "100%"
    }}
  />

  {
    selectedFile &&
    <p
      style={{
        color: "#9ca3af",
        fontSize: "0.85rem",
        marginTop: "0.5rem",
        wordBreak: "break-word"
      }}
    >
      Selected: {selectedFile.name}
    </p>
  }

  <button
    onClick={addSong}
    disabled={uploading}
    style={{
      width: "100%",
      marginTop: "1rem",
      padding: "0.8rem",
      borderRadius: "10px",
      border: "none",
      backgroundColor: "#10b981",
      color: "white",
      fontWeight: "bold",
      cursor: "pointer"
    }}
  >
    {
      uploading
        ? "⏳ Adding..."
        : "➕ Add Song"
    }
  </button>

  {
    uploadMessage &&
    <div
      style={{
        marginTop: "1rem",
        padding: "0.7rem",
        borderRadius: "8px",
        textAlign: "center",
        backgroundColor:
          uploadMessage.includes("Already")
            ? "#78350f"
            : "#064e3b"
      }}
    >
      {uploadMessage}
    </div>
  }
</div>
      <button
        onClick={identifySong}
        disabled={loading}
        style={{
          padding: "1rem 2rem",
          fontSize: "1.2rem",
          borderRadius: "12px",
          border: "none",
          cursor:
            loading
              ? "not-allowed"
              : "pointer",
          backgroundColor: "#3b82f6",
          color: "white",
          fontWeight: "bold",
          boxShadow:
            "0 4px 15px rgba(59,130,246,0.4)",
        }}
      >
        {
          loading
            ? "🎤 Listening..."
            : "🎵 Identify Song"
        }
      </button>

      {
        loading &&
        <Waveform />
      }
       {/* ← add this */}
      {error &&
        <div style={{
          marginTop: "1rem",
          padding: "1rem",
          backgroundColor: "#7f1d1d",
          borderRadius: "12px",
          color: "white"
        }}>
          {error}
        </div>
      }

      {
        song &&
        <div
          style={{
            marginTop: "2rem",
            padding: "1.5rem 2rem",
            backgroundColor: "#1f2937",
            borderRadius: "16px",
            minWidth: "300px",
            textAlign: "center",
            boxShadow:
              "0 8px 25px rgba(0,0,0,0.3)",
          }}
        >
          <h2
            style={{
              marginBottom: "0.5rem",
            }}
          >
            🎶 {
              song
                .replace(".wav", "")
                .replaceAll("_", " ")
                .split(" ")
                .map(
                  word =>
                    word.charAt(0).toUpperCase() +
                    word.slice(1)
                )
                .join(" ")
            }
          </h2>

          <p
            style={{
              color: "#9ca3af",
            }}
          >
            Match Score: {score}
          </p>
        </div>
      }

    </div>
  )
}

export default App