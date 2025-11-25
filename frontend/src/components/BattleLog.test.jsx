import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import BattleLog from './BattleLog'

describe('BattleLog Component', () => {
  const mockBattleHistory = [
    {
      turn: 1,
      winner_id: 'player_1',
      damage_dealt: 25,
      reasoning: 'Player 1 had superior creativity',
      creativity_score: 9.0,
      adherence_score: 8.5,
      visual_effects: [
        { effect: 'fire', intensity: 0.8, color: '#ff4500' },
        { effect: 'explosion', intensity: 0.9, color: '#ff6600' }
      ]
    },
    {
      turn: 2,
      winner_id: 'player_2',
      damage_dealt: 30,
      reasoning: 'Player 2 showed better card adherence',
      creativity_score: 7.5,
      adherence_score: 9.5,
      visual_effects: [
        { effect: 'ice', intensity: 0.7, color: '#00bfff' }
      ]
    },
    {
      turn: 3,
      winner_id: null,
      damage_dealt: 0,
      reasoning: 'Both prompts were equally matched',
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
    
    expect(screen.getByText(/Turn 1/i)).toBeInTheDocument()
    expect(screen.getByText(/Turn 2/i)).toBeInTheDocument()
    expect(screen.getByText(/Turn 3/i)).toBeInTheDocument()
  })

  it('shows victory indicator for player wins', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[0]]} playerName="You" opponentName="Enemy" />)
    
    expect(screen.getByText(/You Won!/i)).toBeInTheDocument()
    expect(screen.getByText('25 damage')).toBeInTheDocument()
  })

  it('shows defeat indicator for player losses', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[1]]} playerName="You" opponentName="Enemy" />)
    
    expect(screen.getByText(/Enemy Won!/i)).toBeInTheDocument()
    expect(screen.getByText('30 damage')).toBeInTheDocument()
  })

  it('shows tie indicator when no winner', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[2]]} playerName="You" opponentName="Enemy" />)
    
    expect(screen.getByText(/Tie!/i)).toBeInTheDocument()
  })

  it('displays reasoning for each battle', () => {
    render(<BattleLog battleHistory={mockBattleHistory} playerName="You" opponentName="Enemy" />)
    
    expect(screen.getByText(/superior creativity/i)).toBeInTheDocument()
    expect(screen.getByText(/better card adherence/i)).toBeInTheDocument()
    expect(screen.getByText(/equally matched/i)).toBeInTheDocument()
  })

  it('displays creativity and adherence scores', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[0]]} playerName="You" opponentName="Enemy" />)
    
    expect(screen.getByText('9/10')).toBeInTheDocument()
    expect(screen.getByText('8.5/10')).toBeInTheDocument()
  })

  it('displays visual effects when present', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[0]]} playerName="You" opponentName="Enemy" />)
    
    expect(screen.getByText('fire')).toBeInTheDocument()
    expect(screen.getByText('explosion')).toBeInTheDocument()
  })

  it('does not display visual effects section when empty', () => {
    render(<BattleLog battleHistory={[mockBattleHistory[2]]} playerName="You" opponentName="Enemy" />)
    
    // Should not have any visual effect badges
    expect(screen.queryByText('fire')).not.toBeInTheDocument()
    expect(screen.queryByText('ice')).not.toBeInTheDocument()
  })

  it('displays battles in reverse order (newest first)', () => {
    render(<BattleLog battleHistory={mockBattleHistory} playerName="You" opponentName="Enemy" />)
    
    const turns = screen.getAllByText(/Turn \d/)
    expect(turns[0]).toHaveTextContent('Turn 3')
    expect(turns[1]).toHaveTextContent('Turn 2')
    expect(turns[2]).toHaveTextContent('Turn 1')
  })
})

