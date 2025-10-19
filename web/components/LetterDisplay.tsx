interface LetterDisplayProps {
  letter: string
  confidence: number
  holdProgress: number
}

export default function LetterDisplay({ letter, confidence, holdProgress }: LetterDisplayProps) {
  return (
    <div className="bg-dark/50 border border-primary/30 rounded-xl p-6">
      <h3 className="text-sm font-semibold text-gray-400 mb-3">Detected Letter</h3>
      
      {letter ? (
        <div className="text-center">
          <div className="text-8xl font-bold mb-4 animate-pulse-slow">
            {letter}
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-400">Confidence</span>
              <span className="text-primary font-bold">{(confidence * 100).toFixed(0)}%</span>
            </div>
            <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-300"
                style={{ width: `${confidence * 100}%` }}
              />
            </div>
          </div>
          
          {holdProgress > 0 && (
            <div className="mt-4 text-sm text-gray-300">
              Hold to add... ({(holdProgress * 100).toFixed(0)}%)
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">
          <div className="text-6xl mb-4">👋</div>
          <p>Show a letter to the camera</p>
        </div>
      )}
    </div>
  )
}
