interface HelpGuideProps {
  onClose: () => void
}

export default function HelpGuide({ onClose }: HelpGuideProps) {
  const letters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'
  ]

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-dark-light border border-primary/30 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-dark-light border-b border-primary/30 p-6 flex justify-between items-center">
          <h2 className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            ASL Letter Guide
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white text-2xl transition-colors"
          >
            ✕
          </button>
        </div>
        
        <div className="p-6 space-y-6">
          {/* Important Notes */}
          <div className="bg-primary/10 border border-primary/30 rounded-xl p-4">
            <h3 className="font-bold text-primary mb-2">📌 Important Tips:</h3>
            <ul className="text-sm text-gray-300 space-y-1">
              <li>• Show the <strong>BACK of your hand</strong> to the camera</li>
              <li>• Hold each gesture steady for <strong>1 second</strong></li>
              <li>• Wait for <strong>1.5 second cooldown</strong> between letters</li>
              <li>• Make sure your hand is well-lit and clearly visible</li>
              <li>• Letters J and Z require motion and are not supported</li>
            </ul>
          </div>
          
          {/* Supported Letters Grid */}
          <div>
            <h3 className="font-bold text-lg mb-4">Supported Letters (24 total)</h3>
            <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-3">
              {letters.map((letter) => (
                <div
                  key={letter}
                  className="aspect-square bg-dark/50 border border-secondary/30 rounded-xl flex items-center justify-center hover:border-primary/50 transition-colors"
                >
                  <span className="text-3xl font-bold">{letter}</span>
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-500 mt-4 italic">
              Note: Letters J and Z require hand motion and are not included in static recognition.
            </p>
          </div>
          
          {/* How It Works */}
          <div className="bg-secondary/10 border border-secondary/30 rounded-xl p-4">
            <h3 className="font-bold text-secondary mb-2">⚡ How It Works:</h3>
            <ol className="text-sm text-gray-300 space-y-2">
              <li><strong>1. Detection:</strong> AI identifies your hand and tracks 21 landmarks</li>
              <li><strong>2. Classification:</strong> Ultra-lenient algorithm recognizes the ASL letter</li>
              <li><strong>3. Hold Time:</strong> Keep the gesture for 1 second to confirm</li>
              <li><strong>4. Cooldown:</strong> 1.5 second pause prevents duplicate letters</li>
              <li><strong>5. Output:</strong> Letter is added to your text!</li>
            </ol>
          </div>
          
          {/* Controls Reference */}
          <div>
            <h3 className="font-bold text-lg mb-3">🎮 Controls</h3>
            <div className="grid sm:grid-cols-3 gap-3">
              <div className="bg-accent/10 border border-accent/30 rounded-lg p-3 text-center">
                <div className="text-2xl mb-1">⎵</div>
                <div className="font-semibold text-sm">Space</div>
                <div className="text-xs text-gray-400">Add space</div>
              </div>
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-center">
                <div className="text-2xl mb-1">⌫</div>
                <div className="font-semibold text-sm">Backspace</div>
                <div className="text-xs text-gray-400">Delete last</div>
              </div>
              <div className="bg-gray-500/10 border border-gray-500/30 rounded-lg p-3 text-center">
                <div className="text-2xl mb-1">🗑️</div>
                <div className="font-semibold text-sm">Clear</div>
                <div className="text-xs text-gray-400">Clear all</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
