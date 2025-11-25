import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import PlayerStatus from './PlayerStatus'

describe('PlayerStatus Component', () => {
  const mockPlayer = {
    id: 'p1',
    username: 'TestPlayer',
    hp: 100,
    elo_rating: 1500,
  }

  it('renders player information', () => {
    render(<PlayerStatus player={mockPlayer} isOpponent={false} />)
    
    expect(screen.getByText('TestPlayer')).toBeInTheDocument()
    expect(screen.getByText('1500')).toBeInTheDocument()
    expect(screen.getByText('100 / 100')).toBeInTheDocument()
  })

  it('shows "You" role for player', () => {
    render(<PlayerStatus player={mockPlayer} isOpponent={false} />)
    
    expect(screen.getByText('You')).toBeInTheDocument()
  })

  it('shows "Enemy" role for opponent', () => {
    render(<PlayerStatus player={mockPlayer} isOpponent={true} />)
    
    expect(screen.getByText('Enemy')).toBeInTheDocument()
  })

  it('displays FULL HP badge at 100 HP', () => {
    render(<PlayerStatus player={mockPlayer} isOpponent={false} />)
    
    expect(screen.getByText('✨ FULL HP')).toBeInTheDocument()
  })

  it('displays LOW HP badge below 33 HP', () => {
    const lowHPPlayer = { ...mockPlayer, hp: 30 }
    render(<PlayerStatus player={lowHPPlayer} isOpponent={false} />)
    
    expect(screen.getByText('⚠️ LOW HP')).toBeInTheDocument()
  })

  it('displays DEFEATED badge at 0 HP', () => {
    const defeatedPlayer = { ...mockPlayer, hp: 0 }
    render(<PlayerStatus player={defeatedPlayer} isOpponent={false} />)
    
    expect(screen.getByText('💀 DEFEATED')).toBeInTheDocument()
  })

  it('shows green HP bar above 66%', () => {
    const player = { ...mockPlayer, hp: 70 }
    const { container } = render(<PlayerStatus player={player} isOpponent={false} />)
    
    const hpBar = container.querySelector('.bg-green-500')
    expect(hpBar).toBeInTheDocument()
  })

  it('shows yellow HP bar between 33% and 66%', () => {
    const player = { ...mockPlayer, hp: 50 }
    const { container } = render(<PlayerStatus player={player} isOpponent={false} />)
    
    const hpBar = container.querySelector('.bg-yellow-500')
    expect(hpBar).toBeInTheDocument()
  })

  it('shows red HP bar below 33%', () => {
    const player = { ...mockPlayer, hp: 30 }
    const { container } = render(<PlayerStatus player={player} isOpponent={false} />)
    
    const hpBar = container.querySelector('.bg-red-500')
    expect(hpBar).toBeInTheDocument()
  })

  it('has blue border for player', () => {
    const { container } = render(<PlayerStatus player={mockPlayer} isOpponent={false} />)
    
    const statusCard = container.querySelector('.border-blue-500')
    expect(statusCard).toBeInTheDocument()
  })

  it('has red border for opponent', () => {
    const { container } = render(<PlayerStatus player={mockPlayer} isOpponent={true} />)
    
    const statusCard = container.querySelector('.border-red-500')
    expect(statusCard).toBeInTheDocument()
  })

  it('displays correct HP percentage width', () => {
    const player = { ...mockPlayer, hp: 75 }
    const { container } = render(<PlayerStatus player={player} isOpponent={false} />)
    
    const hpBar = container.querySelector('[style*="width: 75%"]')
    expect(hpBar).toBeInTheDocument()
  })

  it('handles 0 HP correctly', () => {
    const player = { ...mockPlayer, hp: 0 }
    render(<PlayerStatus player={player} isOpponent={false} />)
    
    expect(screen.getByText('0 / 100')).toBeInTheDocument()
    expect(screen.getByText('💀 DEFEATED')).toBeInTheDocument()
  })
})

