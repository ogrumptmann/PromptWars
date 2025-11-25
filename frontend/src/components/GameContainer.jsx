/**
 * GameContainer Component
 * Main game orchestrator - manages game flow and state
 */
import { useEffect } from 'react'
import { useGameStore } from '../store/gameStore'
import { fetchCards, drawHand, submitBattle } from '../services/api'
import PlayerStatus from './PlayerStatus'
import CardHand from './CardHand'
import PromptInput from './PromptInput'
import BattleLog from './BattleLog'

const GameContainer = () => {
  const {
    player,
    opponent,
    myPrompt,
    mySelectedCards,
    hasSubmitted,
    battleHistory,
    isLoading,
    error,
    setPlayerHand,
    setMyPrompt,
    toggleCardSelection,
    setHasSubmitted,
    addBattleResult,
    updatePlayerHP,
    updateOpponentHP,
    incrementTurn,
    setLoading,
    setError,
    setAllCards,
    resetGame,
  } = useGameStore()

  // Initialize game - fetch cards and draw initial hand
  useEffect(() => {
    const initializeGame = async () => {
      try {
        setLoading(true)
        
        // Fetch all cards for reference
        const allCards = await fetchCards()
        setAllCards(allCards)
        
        // Draw initial hand
        const hand = await drawHand(3)
        setPlayerHand(hand)
        
        setLoading(false)
      } catch (err) {
        console.error('Failed to initialize game:', err)
        setError(err.message)
        setLoading(false)
      }
    }

    initializeGame()
  }, [])

  const handlePromptSubmit = async () => {
    try {
      setLoading(true)
      setHasSubmitted(true)

      // For now, simulate a battle against a mock opponent
      // In Phase 2.6, this will be replaced with WebSocket communication
      const battleData = {
        player1_name: player.username || 'You',
        player1_prompt: myPrompt,
        player1_cards: mySelectedCards,
        player2_name: opponent.username || 'AI Opponent',
        player2_prompt: 'A mighty ice dragon descends from frozen peaks, breathing crystalline shards',
        player2_cards: ['ice', 'summon', 'crystal'],
      }

      const result = await submitBattle(battleData)

      console.log('Battle result:', result)

      // Add battle result to history
      addBattleResult({
        ...result,
        turn: battleHistory.length + 1,
      })

      // Update HP based on result
      // Judge API returns winner_id as 'player_1' or 'player_2'
      if (result.winner_id === 'player_1') {
        // Player won - opponent takes damage
        const newOpponentHP = opponent.hp - result.damage_dealt
        console.log(`Opponent takes ${result.damage_dealt} damage. HP: ${opponent.hp} -> ${newOpponentHP}`)
        updateOpponentHP(newOpponentHP)
      } else if (result.winner_id === 'player_2') {
        // Opponent won - player takes damage
        const newPlayerHP = player.hp - result.damage_dealt
        console.log(`Player takes ${result.damage_dealt} damage. HP: ${player.hp} -> ${newPlayerHP}`)
        updatePlayerHP(newPlayerHP)
      } else {
        console.log('Battle was a tie - no damage dealt')
      }

      // Draw new hand for next turn
      const newHand = await drawHand(3)
      setPlayerHand(newHand)

      // Increment turn
      incrementTurn()
      
      setLoading(false)
    } catch (err) {
      console.error('Failed to submit prompt:', err)
      setError(`Failed to submit battle: ${err.message}. Please try again or reset the game.`)
      setLoading(false)
      setHasSubmitted(false)
    }
  }

  if (isLoading && player.hand.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-purple-500 mx-auto mb-4"></div>
          <p className="text-white text-xl">Loading game...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-black text-white p-4">
      <div className="container mx-auto max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8 relative">
          <h1 className="text-5xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            ⚔️ Prompt Wars
          </h1>
          <p className="text-gray-300">Battle with creative prompts!</p>

          {/* Reset Button */}
          <button
            onClick={() => {
              if (confirm('Are you sure you want to reset the game?')) {
                resetGame()
                window.location.reload()
              }
            }}
            className="absolute top-0 right-0 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition-all"
          >
            🔄 Reset Game
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-4 bg-red-900 bg-opacity-50 border-2 border-red-500 rounded-lg">
            <p className="text-white">❌ {error}</p>
          </div>
        )}

        {/* Player Status Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <PlayerStatus player={player} isOpponent={false} />
          <PlayerStatus player={opponent} isOpponent={true} />
        </div>

        {/* Main Game Area */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Cards and Prompt */}
          <div className="lg:col-span-2 space-y-6">
            <CardHand
              cards={player.hand}
              selectedCards={mySelectedCards}
              onCardSelect={toggleCardSelection}
              disabled={hasSubmitted || isLoading}
            />
            <PromptInput
              value={myPrompt}
              onChange={setMyPrompt}
              onSubmit={handlePromptSubmit}
              disabled={hasSubmitted || isLoading}
              selectedCards={mySelectedCards}
            />
          </div>

          {/* Right Column - Battle Log */}
          <div className="lg:col-span-1">
            <BattleLog
              battleHistory={battleHistory}
              playerName={player.username}
              opponentName={opponent.username}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default GameContainer

