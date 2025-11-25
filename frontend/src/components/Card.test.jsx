import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import Card from './Card'

describe('Card Component', () => {
  const mockCard = {
    id: 'fire',
    name: 'Fire',
    type: 'element',
    description: 'Harness the power of flames',
  }

  it('renders card with correct information', () => {
    render(<Card card={mockCard} />)
    
    expect(screen.getByText('Fire')).toBeInTheDocument()
    expect(screen.getByText('Harness the power of flames')).toBeInTheDocument()
    expect(screen.getByText('element')).toBeInTheDocument()
  })

  it('calls onSelect when clicked', () => {
    const onSelect = vi.fn()
    render(<Card card={mockCard} onSelect={onSelect} />)
    
    const card = screen.getByText('Fire').closest('div')
    fireEvent.click(card)
    
    expect(onSelect).toHaveBeenCalledWith('fire')
  })

  it('shows selection indicator when selected', () => {
    render(<Card card={mockCard} isSelected={true} />)
    
    expect(screen.getByText('✓')).toBeInTheDocument()
  })

  it('does not call onSelect when disabled', () => {
    const onSelect = vi.fn()
    render(<Card card={mockCard} onSelect={onSelect} disabled={true} />)
    
    const card = screen.getByText('Fire').closest('div')
    fireEvent.click(card)
    
    expect(onSelect).not.toHaveBeenCalled()
  })

  it('renders different icons for different card types', () => {
    const { rerender } = render(<Card card={mockCard} />)
    expect(screen.getByText('🔥')).toBeInTheDocument()
    
    rerender(<Card card={{ ...mockCard, type: 'action' }} />)
    expect(screen.getByText('⚔️')).toBeInTheDocument()
    
    rerender(<Card card={{ ...mockCard, type: 'material' }} />)
    expect(screen.getByText('🛡️')).toBeInTheDocument()
  })
})

