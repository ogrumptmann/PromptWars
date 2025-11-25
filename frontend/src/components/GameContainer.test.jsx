import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import GameContainer from './GameContainer'
import * as api from '../services/api'

// Mock the API module
vi.mock('../services/api', () => ({
  fetchCards: vi.fn(),
  drawHand: vi.fn(),
  submitBattle: vi.fn(),
}))

describe('GameContainer', () => {
  const mockCards = [
    { id: 'fire', name: 'Fire', type: 'element', description: 'Flames' },
    { id: 'sword', name: 'Sword', type: 'action', description: 'Strike' },
    { id: 'steel', name: 'Steel', type: 'material', description: 'Metal' },
  ]

  const mockBattleResult = {
    winner_id: 'player_1',
    damage_dealt: 25,
    reasoning: 'Player 1 had a more creative prompt',
    creativity_score: 9.0,
    adherence_score: 8.5,
    visual_effects: [
      { effect: 'fire', intensity: 0.8, color: '#ff4500' }
    ]
  }

  beforeEach(() => {
    vi.clearAllMocks()
    api.fetchCards.mockResolvedValue(mockCards)
    api.drawHand.mockResolvedValue(mockCards)
    api.submitBattle.mockResolvedValue(mockBattleResult)
  })

  it('renders loading state initially', () => {
    render(<GameContainer />)
    expect(screen.getByText(/Loading game/i)).toBeInTheDocument()
  })

  it('fetches cards and draws initial hand on mount', async () => {
    render(<GameContainer />)

    await waitFor(() => {
      expect(api.fetchCards).toHaveBeenCalled()
      expect(api.drawHand).toHaveBeenCalledWith(3)
    })
  })

  it('displays player and opponent status', async () => {
    render(<GameContainer />)

    await waitFor(() => {
      expect(screen.getByText('You')).toBeInTheDocument()
      expect(screen.getByText('Enemy')).toBeInTheDocument()
    })
  })

  it('displays cards in hand after loading', async () => {
    render(<GameContainer />)

    await waitFor(() => {
      expect(screen.getByText('Fire')).toBeInTheDocument()
      expect(screen.getByText('Sword')).toBeInTheDocument()
      expect(screen.getByText('Steel')).toBeInTheDocument()
    })
  })

  it('allows selecting cards', async () => {
    render(<GameContainer />)

    await waitFor(() => {
      expect(screen.getByText('Fire')).toBeInTheDocument()
    })

    const fireCard = screen.getByText('Fire').closest('div')
    fireEvent.click(fireCard)

    await waitFor(() => {
      expect(screen.getByText('✓')).toBeInTheDocument()
    })
  })

  it('submits prompt and updates battle log', async () => {
    render(<GameContainer />)

    await waitFor(() => {
      expect(screen.getByText('Fire')).toBeInTheDocument()
    })

    // Select a card
    const fireCard = screen.getByText('Fire').closest('div')
    fireEvent.click(fireCard)

    // Enter prompt
    const promptInput = screen.getByPlaceholderText(/blazing phoenix/i)
    fireEvent.change(promptInput, { target: { value: 'A mighty fire spell' } })

    // Submit
    const submitButton = screen.getByText('Submit Prompt')
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(api.submitBattle).toHaveBeenCalled()
    })

    // Check battle log updated
    await waitFor(() => {
      expect(screen.getByText(/Player 1 had a more creative prompt/i)).toBeInTheDocument()
    })
  })

  it('updates HP after battle', async () => {
    render(<GameContainer />)

    await waitFor(() => {
      expect(screen.getByText('Fire')).toBeInTheDocument()
    })

    // Initial HP should be 100
    expect(screen.getAllByText('100 / 100')).toHaveLength(2)

    // Select card and submit
    const fireCard = screen.getByText('Fire').closest('div')
    fireEvent.click(fireCard)

    const promptInput = screen.getByPlaceholderText(/blazing phoenix/i)
    fireEvent.change(promptInput, { target: { value: 'A mighty fire spell' } })

    const submitButton = screen.getByText('Submit Prompt')
    fireEvent.click(submitButton)

    // Wait for HP to update (opponent should lose 25 HP)
    await waitFor(() => {
      expect(screen.getByText('75 / 100')).toBeInTheDocument()
    }, { timeout: 3000 })
  })

  it('draws new hand after turn', async () => {
    render(<GameContainer />)

    await waitFor(() => {
      expect(screen.getByText('Fire')).toBeInTheDocument()
    })

    // Select card and submit
    const fireCard = screen.getByText('Fire').closest('div')
    fireEvent.click(fireCard)

    const promptInput = screen.getByPlaceholderText(/blazing phoenix/i)
    fireEvent.change(promptInput, { target: { value: 'A mighty fire spell' } })

    const submitButton = screen.getByText('Submit Prompt')
    fireEvent.click(submitButton)

    // Should draw new hand
    await waitFor(() => {
      expect(api.drawHand).toHaveBeenCalledTimes(2) // Once on init, once after turn
    })
  })

  it('displays error message on API failure', async () => {
    api.drawHand.mockRejectedValueOnce(new Error('Network error'))

    render(<GameContainer />)

    await waitFor(() => {
      expect(screen.getByText(/Network error/i)).toBeInTheDocument()
    })
  })
})

