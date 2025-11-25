import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { fetchCards, drawHand, fetchCardsByType, submitBattle, checkJudgeHealth, checkHealth } from './api'

describe('API Service', () => {
  beforeEach(() => {
    global.fetch = vi.fn()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('fetchCards', () => {
    it('fetches all cards successfully', async () => {
      const mockCards = [
        { id: 'fire', name: 'Fire', type: 'element' },
        { id: 'sword', name: 'Sword', type: 'action' },
      ]

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockCards,
      })

      const result = await fetchCards()
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/api/cards')
      expect(result).toEqual(mockCards)
    })

    it('throws error on failed fetch', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
      })

      await expect(fetchCards()).rejects.toThrow('Failed to fetch cards')
    })
  })

  describe('drawHand', () => {
    it('draws hand with default size', async () => {
      const mockHand = [
        { id: 'fire', name: 'Fire', type: 'element' },
        { id: 'sword', name: 'Sword', type: 'action' },
        { id: 'steel', name: 'Steel', type: 'material' },
      ]

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockHand,
      })

      const result = await drawHand()
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/api/cards/draw/hand?hand_size=3')
      expect(result).toEqual(mockHand)
    })

    it('draws hand with custom size', async () => {
      const mockHand = [
        { id: 'fire', name: 'Fire', type: 'element' },
        { id: 'sword', name: 'Sword', type: 'action' },
        { id: 'steel', name: 'Steel', type: 'material' },
        { id: 'ice', name: 'Ice', type: 'element' },
        { id: 'shield', name: 'Shield', type: 'action' },
      ]

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockHand,
      })

      const result = await drawHand(5)
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/api/cards/draw/hand?hand_size=5')
      expect(result).toEqual(mockHand)
    })

    it('throws error on failed draw', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
      })

      await expect(drawHand()).rejects.toThrow('Failed to draw hand')
    })
  })

  describe('fetchCardsByType', () => {
    it('fetches cards by type', async () => {
      const mockCards = [
        { id: 'fire', name: 'Fire', type: 'element' },
        { id: 'ice', name: 'Ice', type: 'element' },
      ]

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockCards,
      })

      const result = await fetchCardsByType('element')
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/api/cards/type/element')
      expect(result).toEqual(mockCards)
    })
  })

  describe('submitBattle', () => {
    it('submits battle successfully', async () => {
      const battleData = {
        player1_name: 'Player1',
        player1_prompt: 'A fire spell',
        player1_cards: ['fire', 'sword'],
        player2_name: 'Player2',
        player2_prompt: 'An ice spell',
        player2_cards: ['ice', 'shield'],
      }

      const mockResult = {
        winner_id: 'player_1',
        damage_dealt: 25,
        reasoning: 'Player 1 was more creative',
        creativity_score: 9.0,
        adherence_score: 8.5,
        visual_effects: [],
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResult,
      })

      const result = await submitBattle(battleData)
      
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:3001/api/judge/battle',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(battleData),
        }
      )
      expect(result).toEqual(mockResult)
    })

    it('throws error on failed battle submission', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
      })

      await expect(submitBattle({})).rejects.toThrow('Failed to submit battle')
    })
  })

  describe('checkHealth', () => {
    it('checks backend health', async () => {
      const mockHealth = {
        api: 'healthy',
        redis: 'connected',
        environment: 'development',
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockHealth,
      })

      const result = await checkHealth()
      
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/api/health')
      expect(result).toEqual(mockHealth)
    })
  })
})

