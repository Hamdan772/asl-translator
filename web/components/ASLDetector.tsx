import { useEffect, useRef, useState, useCallback } from 'react'
import Webcam from 'react-webcam'
import { Hands, Results } from '@mediapipe/hands'
import { Camera } from '@mediapipe/camera_utils'
import { ASLClassifier } from '@/utils/aslClassifier'
import LetterDisplay from './LetterDisplay'
import TextOutput from './TextOutput'
import Controls from './Controls'
import HelpGuide from './HelpGuide'

export default function ASLDetector() {
  const webcamRef = useRef<Webcam>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const cameraRef = useRef<Camera | null>(null)
  const classifierRef = useRef<ASLClassifier | null>(null)
  
  const [detectedLetter, setDetectedLetter] = useState<string>('')
  const [confidence, setConfidence] = useState<number>(0)
  const [text, setText] = useState<string>('')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [cooldownRemaining, setCooldownRemaining] = useState<number>(0)
  const [holdProgress, setHoldProgress] = useState<number>(0)
  const [showHelp, setShowHelp] = useState(false)
  const [fps, setFps] = useState<number>(0)
  
  const lastDetectionTime = useRef<number>(0)
  const holdStartTime = useRef<number>(0)
  const lastLetter = useRef<string>('')
  const frameCount = useRef<number>(0)
  const fpsInterval = useRef<number>(0)

  // Initialize MediaPipe Hands
  useEffect(() => {
    const initializeHands = async () => {
      try {
        classifierRef.current = new ASLClassifier()
        
        const hands = new Hands({
          locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
          }
        })
        
        hands.setOptions({
          maxNumHands: 1,
          modelComplexity: 1,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5
        })
        
        hands.onResults(onResults)
        
        if (webcamRef.current && webcamRef.current.video) {
          const camera = new Camera(webcamRef.current.video, {
            onFrame: async () => {
              if (webcamRef.current?.video) {
                await hands.send({ image: webcamRef.current.video })
              }
            },
            width: 1280,
            height: 720
          })
          cameraRef.current = camera
          camera.start()
        }
        
        setIsLoading(false)
      } catch (err) {
        console.error('Error initializing MediaPipe:', err)
        setError('Failed to initialize camera. Please check permissions.')
        setIsLoading(false)
      }
    }
    
    initializeHands()
    
    return () => {
      if (cameraRef.current) {
        cameraRef.current.stop()
      }
    }
  }, [])

  // Cooldown timer
  useEffect(() => {
    if (cooldownRemaining > 0) {
      const timer = setTimeout(() => {
        setCooldownRemaining(Math.max(0, cooldownRemaining - 0.1))
      }, 100)
      return () => clearTimeout(timer)
    }
  }, [cooldownRemaining])

  // FPS calculation
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now()
      const elapsed = (now - fpsInterval.current) / 1000
      if (elapsed > 0) {
        setFps(Math.round(frameCount.current / elapsed))
        frameCount.current = 0
        fpsInterval.current = now
      }
    }, 1000)
    
    fpsInterval.current = Date.now()
    return () => clearInterval(interval)
  }, [])

  const onResults = useCallback((results: Results) => {
    if (!canvasRef.current || !classifierRef.current) return
    
    frameCount.current++
    
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    // Draw video frame
    if (results.image) {
      ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height)
    }
    
    const now = Date.now()
    
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
      const landmarks = results.multiHandLandmarks[0]
      
      // Draw hand landmarks
      drawLandmarks(ctx, landmarks, canvas.width, canvas.height)
      
      // Classify letter
      const classification = classifierRef.current.classify(landmarks)
      
      if (classification && classification.confidence >= 0.40) {
        setDetectedLetter(classification.letter)
        setConfidence(classification.confidence)
        
        // Check cooldown
        const timeSinceLastDetection = (now - lastDetectionTime.current) / 1000
        
        if (timeSinceLastDetection < 1.5) {
          setCooldownRemaining(1.5 - timeSinceLastDetection)
          setHoldProgress(0)
          holdStartTime.current = 0
          return
        }
        
        setCooldownRemaining(0)
        
        // Hold detection
        if (classification.letter === lastLetter.current) {
          if (holdStartTime.current === 0) {
            holdStartTime.current = now
          }
          
          const holdDuration = (now - holdStartTime.current) / 1000
          setHoldProgress(Math.min(holdDuration / 1.0, 1.0))
          
          if (holdDuration >= 1.0 && classification.confidence >= 0.45) {
            // Add letter to text
            setText(prev => prev + classification.letter)
            lastDetectionTime.current = now
            setCooldownRemaining(1.5)
            setHoldProgress(0)
            holdStartTime.current = 0
            lastLetter.current = ''
            
            // Visual feedback
            flashCanvas(ctx, canvas)
          }
        } else {
          lastLetter.current = classification.letter
          holdStartTime.current = 0
          setHoldProgress(0)
        }
      } else {
        setDetectedLetter('')
        setConfidence(0)
        holdStartTime.current = 0
        setHoldProgress(0)
      }
    } else {
      setDetectedLetter('')
      setConfidence(0)
      holdStartTime.current = 0
      setHoldProgress(0)
    }
  }, [])

  const drawLandmarks = (
    ctx: CanvasRenderingContext2D,
    landmarks: any[],
    width: number,
    height: number
  ) => {
    // Draw connections
    const connections = [
      [0, 1], [1, 2], [2, 3], [3, 4], // Thumb
      [0, 5], [5, 6], [6, 7], [7, 8], // Index
      [0, 9], [9, 10], [10, 11], [11, 12], // Middle
      [0, 13], [13, 14], [14, 15], [15, 16], // Ring
      [0, 17], [17, 18], [18, 19], [19, 20], // Pinky
      [5, 9], [9, 13], [13, 17] // Palm
    ]
    
    ctx.strokeStyle = '#00D9FF'
    ctx.lineWidth = 2
    
    connections.forEach(([start, end]) => {
      const startPoint = landmarks[start]
      const endPoint = landmarks[end]
      
      ctx.beginPath()
      ctx.moveTo(startPoint.x * width, startPoint.y * height)
      ctx.lineTo(endPoint.x * width, endPoint.y * height)
      ctx.stroke()
    })
    
    // Draw points
    landmarks.forEach((landmark, index) => {
      const x = landmark.x * width
      const y = landmark.y * height
      
      ctx.beginPath()
      ctx.arc(x, y, index === 0 ? 8 : 5, 0, 2 * Math.PI)
      ctx.fillStyle = index === 0 ? '#FFD700' : '#FF00E5'
      ctx.fill()
      ctx.strokeStyle = '#FFFFFF'
      ctx.lineWidth = 1
      ctx.stroke()
    })
  }

  const flashCanvas = (ctx: CanvasRenderingContext2D, canvas: HTMLCanvasElement) => {
    ctx.fillStyle = 'rgba(0, 217, 255, 0.3)'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    setTimeout(() => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }, 100)
  }

  const handleAddSpace = () => {
    setText(prev => prev + ' ')
  }

  const handleBackspace = () => {
    setText(prev => prev.slice(0, -1))
  }

  const handleClear = () => {
    setText('')
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(text)
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="bg-red-500/10 border border-red-500/30 rounded-2xl p-8 text-center max-w-md">
          <div className="text-4xl mb-4">⚠️</div>
          <h3 className="text-xl font-bold text-red-400 mb-2">Error</h3>
          <p className="text-gray-300">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Main Detection Area */}
      <div className="bg-dark-light/50 backdrop-blur-sm border border-primary/20 rounded-2xl p-6">
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Camera View */}
          <div className="relative">
            <div className="relative aspect-video bg-black rounded-xl overflow-hidden">
              <Webcam
                ref={webcamRef}
                audio={false}
                className="absolute inset-0 w-full h-full object-cover opacity-0"
                screenshotFormat="image/jpeg"
                videoConstraints={{
                  facingMode: 'user',
                  width: 1280,
                  height: 720
                }}
              />
              <canvas
                ref={canvasRef}
                width={1280}
                height={720}
                className="absolute inset-0 w-full h-full"
              />
              
              {isLoading && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/50">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-white">Loading camera...</p>
                  </div>
                </div>
              )}
              
              {/* FPS Counter */}
              <div className="absolute top-2 left-2 bg-black/50 backdrop-blur-sm px-2 py-1 rounded text-xs">
                {fps} FPS
              </div>
              
              {/* Hold Progress Bar */}
              {holdProgress > 0 && (
                <div className="absolute bottom-4 left-4 right-4">
                  <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-100"
                      style={{ width: `${holdProgress * 100}%` }}
                    />
                  </div>
                  <p className="text-xs text-center mt-1 text-white">Hold for {(1.0 - holdProgress).toFixed(1)}s</p>
                </div>
              )}
              
              {/* Cooldown Indicator */}
              {cooldownRemaining > 0 && (
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                  <div className="bg-black/70 backdrop-blur-sm px-6 py-3 rounded-xl border border-yellow-500/50">
                    <p className="text-yellow-400 font-bold text-lg">
                      Cooldown: {cooldownRemaining.toFixed(1)}s
                    </p>
                  </div>
                </div>
              )}
            </div>
            
            <button
              onClick={() => setShowHelp(true)}
              className="mt-4 w-full bg-primary/10 hover:bg-primary/20 border border-primary/30 rounded-xl py-3 font-semibold transition-colors"
            >
              📖 View Letter Guide
            </button>
          </div>
          
          {/* Detection Info & Text Output */}
          <div className="space-y-6">
            <LetterDisplay
              letter={detectedLetter}
              confidence={confidence}
              holdProgress={holdProgress}
            />
            
            <TextOutput
              text={text}
              onCopy={handleCopy}
            />
            
            <Controls
              onSpace={handleAddSpace}
              onBackspace={handleBackspace}
              onClear={handleClear}
            />
          </div>
        </div>
      </div>
      
      {/* Help Modal */}
      {showHelp && <HelpGuide onClose={() => setShowHelp(false)} />}
    </div>
  )
}
