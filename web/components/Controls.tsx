interface ControlsProps {
  onSpace: () => void
  onBackspace: () => void
  onClear: () => void
}

export default function Controls({ onSpace, onBackspace, onClear }: ControlsProps) {
  return (
    <div className="grid grid-cols-3 gap-3">
      <button
        onClick={onSpace}
        className="bg-accent/10 hover:bg-accent/20 border border-accent/30 rounded-xl py-4 font-semibold transition-colors"
      >
        ⎵ Space
      </button>
      <button
        onClick={onBackspace}
        className="bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 rounded-xl py-4 font-semibold transition-colors"
      >
        ⌫ Backspace
      </button>
      <button
        onClick={onClear}
        className="bg-gray-500/10 hover:bg-gray-500/20 border border-gray-500/30 rounded-xl py-4 font-semibold transition-colors"
      >
        🗑️ Clear
      </button>
    </div>
  )
}
