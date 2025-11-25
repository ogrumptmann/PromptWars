import { useState, useEffect } from 'react'
import { useWebSocket } from './hooks/useWebSocket'

function App() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')

  // Generate a random client ID
  const [clientId] = useState(() => `client_${Math.random().toString(36).substr(2, 9)}`)

  // WebSocket connection
  const { isConnected, lastMessage, sendMessage, error: wsError } = useWebSocket(
    clientId,
    (message) => {
      setMessages(prev => [...prev, message])
    }
  )

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

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      sendMessage('TEST_MESSAGE', { text: inputMessage })
      setInputMessage('')
    }
  }

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

          {/* WebSocket Test Section */}
          <div className="mt-8 max-w-2xl mx-auto">
            <div className="bg-gray-800 rounded-lg p-6 shadow-xl">
              <h2 className="text-2xl font-semibold mb-4">WebSocket Test</h2>

              <div className="space-y-3 text-left mb-4">
                <div className="flex justify-between">
                  <span className="text-gray-400">Client ID:</span>
                  <span className="text-blue-400 font-mono text-sm">{clientId}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">WebSocket:</span>
                  <span className={isConnected ? 'text-green-400' : 'text-red-400'}>
                    {isConnected ? 'Connected ✓' : 'Disconnected ✗'}
                  </span>
                </div>
                {wsError && (
                  <div className="text-red-400 text-sm">{wsError}</div>
                )}
              </div>

              {/* Message Input */}
              <div className="flex gap-2 mb-4">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Type a message..."
                  className="flex-1 px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                  disabled={!isConnected}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!isConnected || !inputMessage.trim()}
                  className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed transition"
                >
                  Send
                </button>
              </div>

              {/* Message Log */}
              <div className="bg-gray-900 rounded-lg p-4 h-64 overflow-y-auto">
                <h3 className="text-sm text-gray-400 mb-2">Message Log:</h3>
                {messages.length === 0 ? (
                  <p className="text-gray-500 text-sm">No messages yet...</p>
                ) : (
                  <div className="space-y-2">
                    {messages.map((msg, idx) => (
                      <div key={idx} className="text-sm">
                        <span className="text-purple-400 font-semibold">{msg.type}</span>
                        <span className="text-gray-500 mx-2">→</span>
                        <span className="text-gray-300">{JSON.stringify(msg.data)}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="mt-8 text-gray-400">
            <p>Phase 1: Infrastructure Setup Complete ✅</p>
            <p className="mt-2">WebSocket Echo Server Active 🔌</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

