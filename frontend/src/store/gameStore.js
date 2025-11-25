/**
 * Zustand Store for Game State Management
 * Manages game state, player data, and battle history
 */
import { create } from 'zustand'

export const useGameStore = create((set, get) => ({
  // Game state
  gameId: null,
  gameStatus: 'idle', // idle, waiting, active, finished
  currentTurn: 0,
  
  // Player state
  player: {
    id: null,
    username: null,
    hp: 100,
    hand: [],
    elo_rating: 1200,
  },
  
  // Opponent state
  opponent: {
    id: null,
    username: null,
    hp: 100,
    hand: [], // We don't see opponent's hand
    elo_rating: 1200,
  },
  
  // Current turn state
  myPrompt: '',
  mySelectedCards: [],
  hasSubmitted: false,
  opponentHasSubmitted: false,
  
  // Battle history
  battleHistory: [],
  
  // UI state
  isLoading: false,
  error: null,
  
  // Available cards (for reference)
  allCards: [],
  
  // Actions
  setGameId: (gameId) => set({ gameId }),
  
  setGameStatus: (status) => set({ gameStatus: status }),
  
  setPlayer: (playerData) => set({ 
    player: { ...get().player, ...playerData } 
  }),
  
  setOpponent: (opponentData) => set({ 
    opponent: { ...get().opponent, ...opponentData } 
  }),
  
  setPlayerHand: (hand) => set({ 
    player: { ...get().player, hand } 
  }),
  
  setMyPrompt: (prompt) => set({ myPrompt: prompt }),
  
  setMySelectedCards: (cards) => set({ mySelectedCards: cards }),
  
  toggleCardSelection: (cardId) => set((state) => {
    const isSelected = state.mySelectedCards.includes(cardId)
    return {
      mySelectedCards: isSelected
        ? state.mySelectedCards.filter(id => id !== cardId)
        : [...state.mySelectedCards, cardId]
    }
  }),
  
  setHasSubmitted: (submitted) => set({ hasSubmitted: submitted }),
  
  setOpponentHasSubmitted: (submitted) => set({ opponentHasSubmitted: submitted }),
  
  addBattleResult: (result) => set((state) => ({
    battleHistory: [...state.battleHistory, result]
  })),
  
  setAllCards: (cards) => set({ allCards: cards }),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  setError: (error) => set({ error }),
  
  updatePlayerHP: (hp) => {
    const clampedHP = Math.max(0, Math.min(100, hp))
    console.log(`[Store] Updating player HP to ${clampedHP}`)
    set((state) => ({
      player: { ...state.player, hp: clampedHP }
    }))
  },

  updateOpponentHP: (hp) => {
    const clampedHP = Math.max(0, Math.min(100, hp))
    console.log(`[Store] Updating opponent HP to ${clampedHP}`)
    set((state) => ({
      opponent: { ...state.opponent, hp: clampedHP }
    }))
  },
  
  incrementTurn: () => set((state) => ({
    currentTurn: state.currentTurn + 1,
    myPrompt: '',
    mySelectedCards: [],
    hasSubmitted: false,
    opponentHasSubmitted: false,
  })),
  
  resetGame: () => set({
    gameId: null,
    gameStatus: 'idle',
    currentTurn: 0,
    player: {
      id: null,
      username: null,
      hp: 100,
      hand: [],
      elo_rating: 1200,
    },
    opponent: {
      id: null,
      username: null,
      hp: 100,
      hand: [],
      elo_rating: 1200,
    },
    myPrompt: '',
    mySelectedCards: [],
    hasSubmitted: false,
    opponentHasSubmitted: false,
    battleHistory: [],
    error: null,
  }),
  
  // Initialize game with data from backend
  initializeGame: (gameData) => set({
    gameId: gameData.game_id,
    gameStatus: gameData.status,
    currentTurn: gameData.current_turn,
    player: {
      id: gameData.player1.player_id,
      username: gameData.player1.username,
      hp: gameData.player1.hp,
      hand: gameData.player1.hand,
      elo_rating: gameData.player1.elo_rating,
    },
    opponent: {
      id: gameData.player2.player_id,
      username: gameData.player2.username,
      hp: gameData.player2.hp,
      hand: [], // Don't show opponent's hand
      elo_rating: gameData.player2.elo_rating,
    },
    battleHistory: [],
    myPrompt: '',
    mySelectedCards: [],
    hasSubmitted: false,
    opponentHasSubmitted: false,
  }),
}))

