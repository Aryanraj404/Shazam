function Waveform() {

  const bars = Array.from(
    { length: 20 },
    (_, i) => i
  )

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: "4px",
        marginTop: "20px"
      }}
    >
      {bars.map((bar) => (
        <div
          key={bar}
          style={{
            width: "6px",
            height: `${20 + Math.random() * 50}px`,
            backgroundColor: "#3b82f6",
            borderRadius: "10px",
            animation: `wave 0.8s infinite alternate`,
            animationDelay: `${bar * 0.05}s`
          }}
        />
      ))}

      <style>
        {`
          @keyframes wave {
            from {
              transform: scaleY(0.5);
            }
            to {
              transform: scaleY(1.5);
            }
          }
        `}
      </style>
    </div>
  )
}

export default Waveform