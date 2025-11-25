import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import App from './App'

// Mock fetch
global.fetch = vi.fn()

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    global.fetch.mockResolvedValue({
      json: async () => ({
        status: 'healthy',
        api: 'running',
        redis: 'connected',
        environment: 'test',
        llm_provider: 'openai'
      })
    })
  })

  it('renders without crashing', () => {
    render(<App />)
    expect(screen.getByText(/Prompt Wars/i)).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    render(<App />)
    expect(screen.getByText(/Connecting to backend/i)).toBeInTheDocument()
  })

  it('fetches health data on mount', async () => {
    render(<App />)
    
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/api/health')
    })
  })

  it('displays health status after loading', async () => {
    render(<App />)
    
    await waitFor(() => {
      expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument()
    })
    
    expect(screen.getByText(/API Status/i)).toBeInTheDocument()
  })

  it('displays WebSocket test section', async () => {
    render(<App />)
    
    await waitFor(() => {
      expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument()
    })
    
    expect(screen.getByText(/WebSocket Test/i)).toBeInTheDocument()
  })

  it('has message input field', async () => {
    render(<App />)
    
    await waitFor(() => {
      expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument()
    })
    
    const input = screen.getByPlaceholderText(/Type a message/i)
    expect(input).toBeInTheDocument()
  })

  it('has send button', async () => {
    render(<App />)
    
    await waitFor(() => {
      expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument()
    })
    
    const button = screen.getByRole('button', { name: /Send/i })
    expect(button).toBeInTheDocument()
  })

  it('handles fetch error gracefully', async () => {
    global.fetch.mockRejectedValue(new Error('Network error'))
    
    render(<App />)
    
    await waitFor(() => {
      expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument()
    })
    
    // App should still render even if health check fails
    expect(screen.getByText(/Prompt Wars/i)).toBeInTheDocument()
  })
})

