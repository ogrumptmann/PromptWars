/**
 * GameContainer Component
 * Main game orchestrator - manages game flow and state
 */
import { useEffect, useState } from 'react'
import { useGameStore } from '../store/gameStore'
import { fetchCards, drawHand, submitBattle } from '../services/api'
import Header from './Header'
import Arena from './Arena'
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
    currentTurn,
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

  // Timer state (placeholder for Phase 2.6 WebSocket integration)
  const [timeRemaining, setTimeRemaining] = useState(45)

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
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Header with Round and Timer */}
      <Header round={currentTurn + 1} timeRemaining={timeRemaining} />

      {/* Arena with Player Avatars and HP */}
      <Arena
        playerHP={player.hp}
        opponentHP={opponent.hp}
        playerName={player.username || 'You'}
        opponentName={opponent.username || 'Opponent'}
      />

      {/* Error Display */}
      {error && (
        <div className="mx-4 my-2 p-3 bg-red-900 bg-opacity-50 border-2 border-red-500 rounded-lg">
          <p className="text-white text-sm">❌ {error}</p>
          <button
            onClick={() => {
              resetGame()
              window.location.reload()
            }}
            className="mt-2 px-3 py-1 bg-red-700 hover:bg-red-600 rounded text-xs"
          >
            Reset Game
          </button>
        </div>
      )}

      {/* Battle Log */}
      <div className="border-b-2 border-gray-700">
        <BattleLog
          battleHistory={battleHistory}
          playerName={player.username || 'You'}
          opponentName={opponent.username || 'Opponent'}
        />
      </div>

      {/* Cards Hand */}
      <div className="border-b-2 border-gray-700 p-4 bg-gray-900">
        <CardHand
          cards={player.hand}
          selectedCards={mySelectedCards}
          onCardSelect={toggleCardSelection}
          disabled={hasSubmitted || isLoading}
        />
      </div>

      {/* Prompt Input (Bottom) */}
      <div className="p-4 bg-gray-900">
        <PromptInput
          value={myPrompt}
          onChange={setMyPrompt}
          onSubmit={handlePromptSubmit}
          selectedCards={mySelectedCards}
          disabled={hasSubmitted || isLoading}
        />
      </div>
    </div>
  )
}

export default GameContainer

