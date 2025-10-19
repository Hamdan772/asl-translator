import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'
import Head from 'next/head'

const ASLDetector = dynamic(() => import('@/components/ASLDetector'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-primary"></div>
    </div>
  ),
})

export default function Home() {
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

  return (
    <>
      <Head>
        <title>ASL Translator - Real-time Sign Language Recognition</title>
        <meta name="description" content="Translate ASL to text in real-time" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-dark via-dark-light to-dark">
        {/* Header */}
        <header className="bg-dark-light/50 backdrop-blur-sm border-b border-primary/20">
          <div className="container mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  🤟 ASL Translator
                </h1>
                <p className="text-gray-400 text-sm md:text-base mt-1">
                  Real-time Sign Language Recognition
                </p>
              </div>
              <div className="flex items-center gap-4">
                <a
                  href="https://github.com/Hamdan772/asl-translator"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-primary transition-colors"
                >
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="container mx-auto px-4 py-8">
          {/* Info Banner */}
          <div className="mb-8 bg-dark-light/50 backdrop-blur-sm border border-primary/20 rounded-2xl p-6">
            <div className="flex items-start gap-4">
              <div className="text-4xl">👋</div>
              <div className="flex-1">
                <h2 className="text-xl font-bold text-primary mb-2">Welcome to ASL Translator!</h2>
                <p className="text-gray-300 mb-3">
                  Show the <strong>back of your hand</strong> to the camera and make ASL letters. 
                  Hold each gesture for 1 second to add it to your text.
                </p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1 bg-primary/10 border border-primary/30 rounded-full text-sm">
                    ✅ 24 Letters (A-Y)
                  </span>
                  <span className="px-3 py-1 bg-secondary/10 border border-secondary/30 rounded-full text-sm">
                    🚀 Ultra-lenient Detection
                  </span>
                  <span className="px-3 py-1 bg-accent/10 border border-accent/30 rounded-full text-sm">
                    ⚡ Real-time Processing
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* ASL Detector Component */}
          {isClient && <ASLDetector />}

          {/* Features */}
          <div className="mt-12 grid md:grid-cols-3 gap-6">
            <div className="bg-dark-light/50 backdrop-blur-sm border border-primary/20 rounded-2xl p-6">
              <div className="text-3xl mb-3">🎯</div>
              <h3 className="text-xl font-bold text-primary mb-2">Accurate Detection</h3>
              <p className="text-gray-400">
                Ultra-lenient AI model recognizes ASL letters with high accuracy, even with imperfect hand positions.
              </p>
            </div>
            <div className="bg-dark-light/50 backdrop-blur-sm border border-secondary/20 rounded-2xl p-6">
              <div className="text-3xl mb-3">⚡</div>
              <h3 className="text-xl font-bold text-secondary mb-2">Real-time Processing</h3>
              <p className="text-gray-400">
                Instant recognition powered by MediaPipe and TensorFlow.js running directly in your browser.
              </p>
            </div>
            <div className="bg-dark-light/50 backdrop-blur-sm border border-accent/20 rounded-2xl p-6">
              <div className="text-3xl mb-3">🔒</div>
              <h3 className="text-xl font-bold text-accent mb-2">Privacy First</h3>
              <p className="text-gray-400">
                All processing happens in your browser. No video data is sent to any server.
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-16 border-t border-primary/20 bg-dark-light/50 backdrop-blur-sm">
          <div className="container mx-auto px-4 py-8 text-center text-gray-400">
            <p>
              Built with ❤️ by{' '}
              <a
                href="https://github.com/Hamdan772"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:text-secondary transition-colors"
              >
                Hamdan Nishad
              </a>
            </p>
            <p className="mt-2 text-sm">
              ASL Translator v2.0 - Open Source Project
            </p>
          </div>
        </footer>
      </main>
    </>
  )
}
