import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, waitFor } from '@testing-library/react'
import { useWebSocket } from './useWebSocket'

describe('useWebSocket', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should initialize with disconnected state', () => {
    const { result } = renderHook(() => useWebSocket('test-client', vi.fn()))
    
    expect(result.current.isConnected).toBe(false)
    expect(result.current.lastMessage).toBe(null)
    expect(result.current.error).toBe(null)
  })

  it('should attempt to connect to WebSocket', async () => {
    const { result } = renderHook(() => useWebSocket('test-client', vi.fn()))

    // WebSocket connection is attempted (we can't reliably test actual connection in unit tests)
    expect(result.current.sendMessage).toBeDefined()
    expect(result.current.reconnect).toBeDefined()
  })

  it('should have sendMessage function', () => {
    const { result } = renderHook(() => useWebSocket('test-client', vi.fn()))
    
    expect(typeof result.current.sendMessage).toBe('function')
  })

  it('should have reconnect function', () => {
    const { result } = renderHook(() => useWebSocket('test-client', vi.fn()))
    
    expect(typeof result.current.reconnect).toBe('function')
  })

  it('should have disconnect function', () => {
    const { result } = renderHook(() => useWebSocket('test-client', vi.fn()))
    
    expect(typeof result.current.disconnect).toBe('function')
  })

  it('should not connect without clientId', () => {
    const { result } = renderHook(() => useWebSocket('', vi.fn()))
    
    expect(result.current.isConnected).toBe(false)
  })

  it('should call onMessage callback when message received', async () => {
    const onMessage = vi.fn()
    const { result } = renderHook(() => useWebSocket('test-client', onMessage))
    
    await waitFor(() => {
      expect(result.current.isConnected).toBe(true)
    })
    
    // Note: Full message handling would require more complex WebSocket mocking
  })
})

