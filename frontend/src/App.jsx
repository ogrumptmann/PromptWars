import { useState, useEffect } from 'react'

function App() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Test backend connection
    fetch('http://localhost:3001/api/health')
      .then(res => res.json())
      .then(data => {
        setHealth(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to connect to backend:', err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black text-white">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            ⚔️ Prompt Wars
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            AI-Powered Text-Based Strategy Game
          </p>

          <div className="max-w-md mx-auto bg-gray-800 rounded-lg p-6 shadow-xl">
            <h2 className="text-2xl font-semibold mb-4">System Status</h2>
            
            {loading ? (
              <p className="text-gray-400">Connecting to backend...</p>
            ) : health ? (
              <div className="space-y-3 text-left">
                <div className="flex justify-between">
                  <span className="text-gray-400">API Status:</span>
                  <span className="text-green-400 font-semibold">{health.api}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Redis:</span>
                  <span className={health.redis === 'connected' ? 'text-green-400' : 'text-red-400'}>
                    {health.redis}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Environment:</span>
                  <span className="text-blue-400">{health.environment}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">LLM Provider:</span>
                  <span className="text-purple-400">{health.llm_provider}</span>
                </div>
              </div>
            ) : (
              <p className="text-red-400">Failed to connect to backend</p>
            )}
          </div>

          <div className="mt-8 text-gray-400">
            <p>Phase 1: Infrastructure Setup Complete ✅</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

