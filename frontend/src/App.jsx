import { useState } from 'react'
import GameContainer from './components/GameContainer'

function App() {
  const [showGame, setShowGame] = useState(false)

  if (showGame) {
    return <GameContainer />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black text-white flex items-center justify-center">
      <div className="text-center max-w-2xl px-4">
        <h1 className="text-7xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
          ⚔️ Prompt Wars
        </h1>
        <p className="text-2xl text-gray-300 mb-8">
          AI-Powered Text-Based Strategy Game
        </p>
        <p className="text-lg text-gray-400 mb-12">
          Battle with creative prompts! Use cards to craft imaginative scenarios and let the AI judge decide the winner.
        </p>

        <button
          onClick={() => setShowGame(true)}
          className="px-12 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700
                     text-white font-bold text-xl rounded-lg shadow-xl hover:shadow-2xl
                     transform hover:scale-105 transition-all duration-200"
        >
          Start Game
        </button>

        <div className="mt-12 text-gray-500 text-sm">
          <p>Phase 2: Core Game Loop - Text-Based MVP</p>
        </div>
      </div>
    </div>
  )
}

export default App

