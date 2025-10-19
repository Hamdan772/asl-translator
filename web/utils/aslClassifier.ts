// ASL Classifier - Ported from Python to TypeScript
// Ultra-lenient detection thresholds

interface Landmark {
  x: number
  y: number
  z: number
}

interface Classification {
  letter: string
  confidence: number
}

export class ASLClassifier {
  private detectionHistory: Map<string, number[]> = new Map()
  private readonly historySize = 7
  private readonly smoothingThreshold = 1 // Need 1 out of 7 frames (ultra-lenient)

  constructor() {
    // Initialize detection history for temporal smoothing
    const letters = 'ABCDEFGHIKLMNOPQRSTUVWXY'.split('')
    letters.forEach(letter => {
      this.detectionHistory.set(letter, [])
    })
  }

  classify(landmarks: any[]): Classification | null {
    if (!landmarks || landmarks.length !== 21) {
      return null
    }

    // Convert landmarks to typed array
    const lm: Landmark[] = landmarks.map((l: any) => ({
      x: l.x,
      y: l.y,
      z: l.z || 0
    }))

    // Get finger states (ultra-lenient)
    const fingerStates = this.fingersUp(lm)
    
    // Try to detect letter (order matters for overlapping patterns)
    let letter = ''
    let confidence = 0

    // Check each letter pattern
    // O must come before C (O is tighter circle)
    if (this.isLetterO(lm, fingerStates)) {
      letter = 'O'
      confidence = 1.0
    } else if (this.isLetterC(lm, fingerStates)) {
      letter = 'C'
      confidence = 0.95
    } else if (this.isLetterA(lm, fingerStates)) {
      letter = 'A'
      confidence = 0.98
    } else if (this.isLetterB(lm, fingerStates)) {
      letter = 'B'
      confidence = 0.95
    } else if (this.isLetterD(lm, fingerStates)) {
      letter = 'D'
      confidence = 0.95
    } else if (this.isLetterE(lm, fingerStates)) {
      letter = 'E'
      confidence = 0.90
    } else if (this.isLetterF(lm, fingerStates)) {
      letter = 'F'
      confidence = 0.92
    } else if (this.isLetterG(lm, fingerStates)) {
      letter = 'G'
      confidence = 0.90
    } else if (this.isLetterH(lm, fingerStates)) {
      letter = 'H'
      confidence = 0.90
    } else if (this.isLetterI(lm, fingerStates)) {
      letter = 'I'
      confidence = 0.95
    } else if (this.isLetterK(lm, fingerStates)) {
      letter = 'K'
      confidence = 0.88
    } else if (this.isLetterL(lm, fingerStates)) {
      letter = 'L'
      confidence = 0.98
    } else if (this.isLetterM(lm, fingerStates)) {
      letter = 'M'
      confidence = 0.85
    } else if (this.isLetterN(lm, fingerStates)) {
      letter = 'N'
      confidence = 0.85
    } else if (this.isLetterP(lm, fingerStates)) {
      letter = 'P'
      confidence = 0.88
    } else if (this.isLetterQ(lm, fingerStates)) {
      letter = 'Q'
      confidence = 0.88
    } else if (this.isLetterR(lm, fingerStates)) {
      letter = 'R'
      confidence = 0.90
    } else if (this.isLetterS(lm, fingerStates)) {
      letter = 'S'
      confidence = 0.92
    } else if (this.isLetterT(lm, fingerStates)) {
      letter = 'T'
      confidence = 0.88
    } else if (this.isLetterU(lm, fingerStates)) {
      letter = 'U'
      confidence = 0.92
    } else if (this.isLetterV(lm, fingerStates)) {
      letter = 'V'
      confidence = 0.95
    } else if (this.isLetterW(lm, fingerStates)) {
      letter = 'W'
      confidence = 0.92
    } else if (this.isLetterX(lm, fingerStates)) {
      letter = 'X'
      confidence = 0.85
    } else if (this.isLetterY(lm, fingerStates)) {
      letter = 'Y'
      confidence = 0.95
    }

    if (!letter) {
      return null
    }

    // Apply temporal smoothing (ultra-lenient: 1/7 frames + bonus)
    const smoothedConfidence = this.applyTemporalSmoothing(letter, confidence)
    
    if (smoothedConfidence >= 0.40) { // Ultra-low threshold
      return {
        letter,
        confidence: smoothedConfidence
      }
    }

    return null
  }

  private applyTemporalSmoothing(letter: string, confidence: number): number {
    const history = this.detectionHistory.get(letter) || []
    
    // Add current confidence
    history.push(confidence)
    
    // Keep only recent history
    if (history.length > this.historySize) {
      history.shift()
    }
    
    this.detectionHistory.set(letter, history)
    
    // Ultra-lenient: if ANY recent detection, give big bonus
    if (history.length >= this.smoothingThreshold) {
      const avg = history.reduce((a, b) => a + b, 0) / history.length
      return Math.min(1.0, avg + 0.30) // +30% bonus
    }
    
    return confidence
  }

  private fingersUp(lm: Landmark[]): boolean[] {
    // Ultra-lenient finger detection
    const fingers: boolean[] = []
    
    // Thumb (check x position)
    const thumbTipX = lm[4].x
    const thumbIpX = lm[3].x
    fingers.push(Math.abs(thumbTipX - thumbIpX) > 0.04) // Very lenient
    
    // Other fingers (check y position with lenient threshold)
    const fingerTips = [8, 12, 16, 20]
    const fingerPips = [6, 10, 14, 18]
    
    for (let i = 0; i < fingerTips.length; i++) {
      const tipY = lm[fingerTips[i]].y
      const pipY = lm[fingerPips[i]].y
      fingers.push(tipY < pipY - 0.02) // Very lenient (was 0.03)
    }
    
    return fingers
  }

  private distance(p1: Landmark, p2: Landmark): number {
    return Math.sqrt(
      Math.pow(p1.x - p2.x, 2) +
      Math.pow(p1.y - p2.y, 2)
    )
  }

  private angle(p1: Landmark, p2: Landmark, p3: Landmark): number {
    const a = this.distance(p2, p3)
    const b = this.distance(p1, p3)
    const c = this.distance(p1, p2)
    
    if (a === 0 || c === 0) return 180
    
    const cosAngle = (a * a + c * c - b * b) / (2 * a * c)
    const clampedCos = Math.max(-1, Math.min(1, cosAngle))
    return Math.acos(clampedCos) * (180 / Math.PI)
  }

  // Letter detection methods (ultra-lenient thresholds)
  
  private isLetterA(lm: Landmark[], fingers: boolean[]): boolean {
    // Thumb up, all fingers down
    return fingers[0] && !fingers[1] && !fingers[2] && !fingers[3] && !fingers[4]
  }

  private isLetterB(lm: Landmark[], fingers: boolean[]): boolean {
    // All fingers up except thumb
    return !fingers[0] && fingers[1] && fingers[2] && fingers[3] && fingers[4]
  }

  private isLetterC(lm: Landmark[], fingers: boolean[]): boolean {
    // Curved hand - wider gap than O
    const thumbIndexDist = this.distance(lm[4], lm[8])
    return thumbIndexDist > 0.35 && thumbIndexDist < 0.80 // Wider than O
  }

  private isLetterD(lm: Landmark[], fingers: boolean[]): boolean {
    // Index up, others down
    return !fingers[0] && fingers[1] && !fingers[2] && !fingers[3] && !fingers[4]
  }

  private isLetterE(lm: Landmark[], fingers: boolean[]): boolean {
    // All fingers down including thumb
    const allDown = !fingers[1] && !fingers[2] && !fingers[3] && !fingers[4]
    const thumbIndexDist = this.distance(lm[4], lm[8])
    return allDown && thumbIndexDist < 0.50 // Very lenient
  }

  private isLetterF(lm: Landmark[], fingers: boolean[]): boolean {
    // Index and thumb touch, others up
    const thumbIndexDist = this.distance(lm[4], lm[8])
    return thumbIndexDist < 0.50 && fingers[2] && fingers[3] && fingers[4] // Very lenient touch
  }

  private isLetterG(lm: Landmark[], fingers: boolean[]): boolean {
    // Index and thumb extended horizontally
    return fingers[0] && fingers[1] && !fingers[2] && !fingers[3] && !fingers[4]
  }

  private isLetterH(lm: Landmark[], fingers: boolean[]): boolean {
    // Index and middle extended horizontally
    return !fingers[0] && fingers[1] && fingers[2] && !fingers[3] && !fingers[4]
  }

  private isLetterI(lm: Landmark[], fingers: boolean[]): boolean {
    // Only pinky up
    return !fingers[0] && !fingers[1] && !fingers[2] && !fingers[3] && fingers[4]
  }

  private isLetterK(lm: Landmark[], fingers: boolean[]): boolean {
    // Index and middle up, forming V
    if (!fingers[1] || !fingers[2] || fingers[3] || fingers[4]) return false
    
    const angle = this.angle(lm[8], lm[0], lm[12])
    return angle >= 20 && angle <= 80 // Very lenient angle
  }

  private isLetterL(lm: Landmark[], fingers: boolean[]): boolean {
    // Thumb and index form L shape
    if (!fingers[0] || !fingers[1] || fingers[2] || fingers[3] || fingers[4]) return false
    
    const angle = this.angle(lm[4], lm[0], lm[8])
    return angle >= 60 && angle <= 130 // Ultra-lenient L angle
  }

  private isLetterM(lm: Landmark[], fingers: boolean[]): boolean {
    // Three fingers down over thumb
    return !fingers[0] && !fingers[1] && !fingers[2] && !fingers[3] && !fingers[4]
  }

  private isLetterN(lm: Landmark[], fingers: boolean[]): boolean {
    // Two fingers down over thumb
    return !fingers[0] && !fingers[1] && !fingers[2] && !fingers[3] && !fingers[4]
  }

  private isLetterO(lm: Landmark[], fingers: boolean[]): boolean {
    // Tight circle with thumb and index
    const thumbIndexDist = this.distance(lm[4], lm[8])
    return thumbIndexDist >= 0.10 && thumbIndexDist < 0.40 // Tighter than C (was < 0.35)
  }

  private isLetterP(lm: Landmark[], fingers: boolean[]): boolean {
    // Similar to K but pointing down
    if (!fingers[1] || !fingers[2] || fingers[3] || fingers[4]) return false
    
    const angle = this.angle(lm[8], lm[0], lm[12])
    return angle >= 20 && angle <= 80
  }

  private isLetterQ(lm: Landmark[], fingers: boolean[]): boolean {
    // Similar to G but pointing down
    return fingers[0] && fingers[1] && !fingers[2] && !fingers[3] && !fingers[4]
  }

  private isLetterR(lm: Landmark[], fingers: boolean[]): boolean {
    // Index and middle crossed
    if (!fingers[1] || !fingers[2] || fingers[3] || fingers[4]) return false
    
    const indexMiddleDist = this.distance(lm[8], lm[12])
    return indexMiddleDist < 0.60 // Very lenient crossing
  }

  private isLetterS(lm: Landmark[], fingers: boolean[]): boolean {
    // Fist with thumb over fingers
    const allDown = !fingers[1] && !fingers[2] && !fingers[3] && !fingers[4]
    const thumbOverFingers = lm[4].y < lm[8].y
    return allDown && thumbOverFingers
  }

  private isLetterT(lm: Landmark[], fingers: boolean[]): boolean {
    // Thumb between index and middle
    const thumbBetween = lm[4].y > lm[6].y && lm[4].y < lm[10].y
    return !fingers[1] && !fingers[2] && !fingers[3] && !fingers[4] && thumbBetween
  }

  private isLetterU(lm: Landmark[], fingers: boolean[]): boolean {
    // Index and middle up together
    if (!fingers[1] || !fingers[2] || fingers[3] || fingers[4]) return false
    
    const indexMiddleDist = this.distance(lm[8], lm[12])
    return indexMiddleDist < 0.60 // Very lenient (together)
  }

  private isLetterV(lm: Landmark[], fingers: boolean[]): boolean {
    // Index and middle up, separated
    if (!fingers[1] || !fingers[2] || fingers[3] || fingers[4]) return false
    
    const indexMiddleDist = this.distance(lm[8], lm[12])
    return indexMiddleDist >= 0.35 // Very lenient separation (was 0.4)
  }

  private isLetterW(lm: Landmark[], fingers: boolean[]): boolean {
    // Index, middle, ring up
    return !fingers[0] && fingers[1] && fingers[2] && fingers[3] && !fingers[4]
  }

  private isLetterX(lm: Landmark[], fingers: boolean[]): boolean {
    // Index bent/hooked
    if (fingers[1] || fingers[2] || fingers[3] || fingers[4]) return false
    
    const angle = this.angle(lm[8], lm[6], lm[5])
    return angle >= 60 && angle <= 130 // Very lenient hook angle
  }

  private isLetterY(lm: Landmark[], fingers: boolean[]): boolean {
    // Thumb and pinky extended
    return fingers[0] && !fingers[1] && !fingers[2] && !fingers[3] && fingers[4]
  }
}
