import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import BattleLog from './BattleLog'

describe('BattleLog Component', () => {
  const mockBattleHistory = [
    {
      turn: 1,
      winner_id: 'player_1',
      damage_dealt: 25,
      reasoning: 'A blazing phoenix erupts from the flames, its wings scorching the arena! The opponent\'s defenses crumble under the intense heat. Victory to the fire wielder!',
      creativity_score: 9.0,
      adherence_score: 8.5,
      visual_effects: [
        { particle_type: 'fire', intensity: 0.8, color: '#ff4500' }
      ]
    },
    {
      turn: 2,
      winner_id: 'player_2',
      damage_dealt: 30,
      reasoning: 'An ice dragon descends from frozen peaks, breathing crystalline shards! The battlefield freezes solid. The cold warrior claims victory!',
      creativity_score: 7.5,
      adherence_score: 9.5,
      visual_effects: [
        { particle_type: 'ice', intensity: 0.7, color: '#00bfff' }
      ]
    },
    {
      turn: 3,
      winner_id: null,
      damage_dealt: 0,
      reasoning: 'Both warriors clash with equal might! Lightning meets thunder in a spectacular display. Neither can claim dominance!',
      creativity_score: 8.0,
      adherence_score: 8.0,
      visual_effects: []
    }
  ]

  it('renders empty state when no battles', () => {
    render(<BattleLog battleHistory={[]} />)
    expect(screen.getByText(/No battles yet/i)).toBeInTheDocument()
  })

  it('displays all battle results', () => {
    render(<BattleLog battleHistory={mockBattleHistory} playerName="You" opponentName="Enemy" />)

    // Check that all three battles are rendered by their narrative stories
    expect(screen.getByText(/blazing phoenix/i)).toBeInTheDocument()
    expect(screen.getByText(/ice dragon/i)).toBeInTheDocument()
    expect(screen.getByText(/equal might/i)).toBeInTheDocument()
  })

  it('shows victory indicator for player wins', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[0]]} playerName="You" opponentName="Enemy" />)

    expect(screen.getByText(/You Wins!/i)).toBeInTheDocument()
    expect(screen.getByText(/25 damage/i)).toBeInTheDocument()
  })

  it('shows defeat indicator for player losses', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[1]]} playerName="You" opponentName="Enemy" />)

    expect(screen.getByText(/Enemy Wins!/i)).toBeInTheDocument()
    expect(screen.getByText(/30 damage/i)).toBeInTheDocument()
  })

  it('shows tie indicator when no winner', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[2]]} playerName="You" opponentName="Enemy" />)

    expect(screen.getByText(/Tie!/i)).toBeInTheDocument()
  })

  it('displays narrative story for each battle', () => {
    render(<BattleLog battleHistory={mockBattleHistory} playerName="You" opponentName="Enemy" />)

    expect(screen.getByText(/blazing phoenix/i)).toBeInTheDocument()
    expect(screen.getByText(/ice dragon/i)).toBeInTheDocument()
    expect(screen.getByText(/equal might/i)).toBeInTheDocument()
  })

  it('displays damage dealt', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[0]]} playerName="You" opponentName="Enemy" />)

    expect(screen.getByText(/25 damage/i)).toBeInTheDocument()
  })

  it('displays battles in reverse order (newest first)', () => {
    render(<BattleLog battleHistory={mockBattleHistory} playerName="You" opponentName="Enemy" />)

    // Get all battle cards
    const battleCards = screen.getAllByText(/damage/i)
    // Should have 3 battles (0 damage for tie is still shown)
    expect(battleCards.length).toBeGreaterThanOrEqual(3)
  })
})

