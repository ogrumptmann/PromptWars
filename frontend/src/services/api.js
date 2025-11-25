/**
 * API Service for backend communication
 * Handles all HTTP requests to the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001'

/**
 * Fetch all available cards
 * @returns {Promise<Array>} Array of card objects
 */
export const fetchCards = async () => {
  const response = await fetch(`${API_BASE_URL}/api/cards`)
  if (!response.ok) {
    throw new Error('Failed to fetch cards')
  }
  return response.json()
}

/**
 * Draw a random hand of cards
 * @param {number} handSize - Number of cards to draw (default: 3)
 * @returns {Promise<Array>} Array of card objects
 */
export const drawHand = async (handSize = 3) => {
  const response = await fetch(`${API_BASE_URL}/api/cards/draw/hand?hand_size=${handSize}`)
  if (!response.ok) {
    throw new Error('Failed to draw hand')
  }
  return response.json()
}

/**
 * Get cards by type
 * @param {string} type - Card type (element, action, material)
 * @returns {Promise<Array>} Array of card objects
 */
export const fetchCardsByType = async (type) => {
  const response = await fetch(`${API_BASE_URL}/api/cards/type/${type}`)
  if (!response.ok) {
    throw new Error(`Failed to fetch ${type} cards`)
  }
  return response.json()
}

/**
 * Submit a battle for judging (for testing)
 * @param {Object} battleData - Battle data with player prompts and cards
 * @returns {Promise<Object>} Battle result
 */
export const submitBattle = async (battleData) => {
  const response = await fetch(`${API_BASE_URL}/api/judge/battle`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(battleData),
  })
  if (!response.ok) {
    throw new Error('Failed to submit battle')
  }
  return response.json()
}

/**
 * Check judge health status
 * @returns {Promise<Object>} Judge health status
 */
export const checkJudgeHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/api/judge/health`)
  if (!response.ok) {
    throw new Error('Failed to check judge health')
  }
  return response.json()
}

/**
 * Get backend health status
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/api/health`)
  if (!response.ok) {
    throw new Error('Failed to check health')
  }
  return response.json()
}

export default {
  fetchCards,
  drawHand,
  fetchCardsByType,
  submitBattle,
  checkJudgeHealth,
  checkHealth,
}

