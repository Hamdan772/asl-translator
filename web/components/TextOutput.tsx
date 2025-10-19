interface TextOutputProps {
  text: string
  onCopy: () => void
}

export default function TextOutput({ text, onCopy }: TextOutputProps) {
  return (
    <div className="bg-dark/50 border border-secondary/30 rounded-xl p-6">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-sm font-semibold text-gray-400">Translated Text</h3>
        <button
          onClick={onCopy}
          disabled={!text}
          className="text-xs bg-secondary/10 hover:bg-secondary/20 border border-secondary/30 rounded-lg px-3 py-1 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          📋 Copy
        </button>
      </div>
      
      <div className="bg-black/30 border border-gray-700 rounded-lg p-4 min-h-[120px] max-h-[200px] overflow-y-auto">
        {text ? (
          <p className="text-white text-lg font-mono break-words">{text}</p>
        ) : (
          <p className="text-gray-500 text-sm italic">Your translated text will appear here...</p>
        )}
      </div>
      
      <div className="mt-2 text-xs text-gray-500 text-right">
        {text.length} characters
      </div>
    </div>
  )
}
