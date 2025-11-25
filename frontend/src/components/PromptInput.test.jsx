import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import PromptInput from './PromptInput'

describe('PromptInput Component', () => {
  it('renders prompt input textarea', () => {
    render(<PromptInput value="" onChange={() => {}} onSubmit={() => {}} selectedCards={[]} />)
    
    const textarea = screen.getByPlaceholderText(/blazing phoenix/i)
    expect(textarea).toBeInTheDocument()
  })

  it('displays character count', () => {
    render(<PromptInput value="Hello" onChange={() => {}} onSubmit={() => {}} selectedCards={[]} />)
    
    expect(screen.getByText('5 / 500')).toBeInTheDocument()
  })

  it('calls onChange when text is entered', () => {
    const onChange = vi.fn()
    render(<PromptInput value="" onChange={onChange} onSubmit={() => {}} selectedCards={[]} />)
    
    const textarea = screen.getByPlaceholderText(/blazing phoenix/i)
    fireEvent.change(textarea, { target: { value: 'Test prompt' } })
    
    expect(onChange).toHaveBeenCalledWith('Test prompt')
  })

  it('calls onSubmit when submit button is clicked', () => {
    const onSubmit = vi.fn()
    render(
      <PromptInput 
        value="Test prompt" 
        onChange={() => {}} 
        onSubmit={onSubmit} 
        selectedCards={['fire']} 
      />
    )
    
    const submitButton = screen.getByText('Submit Prompt')
    fireEvent.click(submitButton)
    
    expect(onSubmit).toHaveBeenCalled()
  })

  it('disables submit button when no prompt', () => {
    render(
      <PromptInput 
        value="" 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={['fire']} 
      />
    )
    
    const submitButton = screen.getByText('Submit Prompt')
    expect(submitButton).toBeDisabled()
  })

  it('disables submit button when no cards selected', () => {
    render(
      <PromptInput 
        value="Test prompt" 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={[]} 
      />
    )
    
    const submitButton = screen.getByText('Submit Prompt')
    expect(submitButton).toBeDisabled()
  })

  it('enables submit button when prompt and cards are present', () => {
    render(
      <PromptInput 
        value="Test prompt" 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={['fire']} 
      />
    )
    
    const submitButton = screen.getByText('Submit Prompt')
    expect(submitButton).not.toBeDisabled()
  })

  it('shows selected cards count', () => {
    render(
      <PromptInput 
        value="" 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={['fire', 'sword', 'steel']} 
      />
    )
    
    expect(screen.getByText(/3 cards selected/i)).toBeInTheDocument()
  })

  it('shows warning when approaching character limit', () => {
    const longText = 'a'.repeat(460) // 92% of 500
    render(
      <PromptInput 
        value={longText} 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={['fire']} 
      />
    )
    
    const charCount = screen.getByText('460 / 500')
    expect(charCount).toHaveClass('text-yellow-400')
  })

  it('enforces max length of 500 characters', () => {
    render(
      <PromptInput 
        value="" 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={[]} 
        maxLength={500}
      />
    )
    
    const textarea = screen.getByPlaceholderText(/blazing phoenix/i)
    expect(textarea).toHaveAttribute('maxLength', '500')
  })

  it('disables input when disabled prop is true', () => {
    render(
      <PromptInput 
        value="" 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={[]} 
        disabled={true}
      />
    )
    
    const textarea = screen.getByPlaceholderText(/blazing phoenix/i)
    expect(textarea).toBeDisabled()
  })

  it('shows validation message when no cards selected', () => {
    render(
      <PromptInput 
        value="Test prompt" 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={[]} 
      />
    )
    
    expect(screen.getByText(/Select at least 1 card/i)).toBeInTheDocument()
  })

  it('shows validation message when prompt is empty', () => {
    render(
      <PromptInput 
        value="" 
        onChange={() => {}} 
        onSubmit={() => {}} 
        selectedCards={['fire']} 
      />
    )
    
    expect(screen.getByText(/Write a prompt/i)).toBeInTheDocument()
  })
})

