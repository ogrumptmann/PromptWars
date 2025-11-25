/**
 * PromptInput Component
 * Text input for player's creative prompt
 */
import { useState } from 'react'
import PropTypes from 'prop-types'

const PromptInput = ({ value, onChange, onSubmit, disabled, selectedCards, maxLength }) => {
  const [charCount, setCharCount] = useState(value?.length || 0)

  const handleChange = (e) => {
    const newValue = e.target.value
    setCharCount(newValue.length)
    if (onChange) {
      onChange(newValue)
    }
  }

  const handleSubmit = () => {
    if (onSubmit && value.trim() && selectedCards.length > 0) {
      onSubmit()
    }
  }

  const canSubmit = value.trim().length > 0 && selectedCards.length > 0 && !disabled

  return (
    <div className="w-full bg-gray-800 rounded-lg p-6 shadow-xl">
      <h2 className="text-2xl font-bold text-white mb-4">Your Prompt</h2>
      
      {/* Instructions */}
      <p className="text-gray-300 text-sm mb-4">
        Write a creative prompt using your selected cards. Be imaginative!
      </p>
      
      {/* Text Area */}
      <textarea
        value={value}
        onChange={handleChange}
        disabled={disabled}
        maxLength={maxLength}
        placeholder="A blazing phoenix rises from the ashes, wielding a flaming sword..."
        className="w-full h-32 px-4 py-3 bg-gray-900 text-white rounded-lg border-2 border-gray-700 
                   focus:border-purple-500 focus:outline-none resize-none
                   disabled:opacity-50 disabled:cursor-not-allowed"
      />
      
      {/* Character Count */}
      <div className="flex justify-between items-center mt-2">
        <span className={`text-sm ${charCount > maxLength * 0.9 ? 'text-yellow-400' : 'text-gray-400'}`}>
          {charCount} / {maxLength} characters
        </span>
        
        {/* Selected Cards Indicator */}
        <span className={`text-sm ${selectedCards.length === 0 ? 'text-red-400' : 'text-green-400'}`}>
          {selectedCards.length > 0 ? `${selectedCards.length} card(s) selected` : 'Select at least 1 card'}
        </span>
      </div>
      
      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={!canSubmit}
        className={`
          mt-4 w-full py-3 px-6 rounded-lg font-bold text-lg transition-all duration-200
          ${canSubmit
            ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
            : 'bg-gray-700 text-gray-500 cursor-not-allowed'
          }
        `}
      >
        {disabled ? 'Waiting for opponent...' : 'Submit Prompt'}
      </button>
      
      {/* Validation Messages */}
      {!disabled && (
        <div className="mt-2 text-sm text-center">
          {value.trim().length === 0 && (
            <p className="text-yellow-400">⚠️ Write a prompt to continue</p>
          )}
          {value.trim().length > 0 && selectedCards.length === 0 && (
            <p className="text-yellow-400">⚠️ Select at least one card</p>
          )}
        </div>
      )}
    </div>
  )
}

PromptInput.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  selectedCards: PropTypes.arrayOf(PropTypes.string),
  maxLength: PropTypes.number,
}

PromptInput.defaultProps = {
  disabled: false,
  selectedCards: [],
  maxLength: 500,
}

export default PromptInput

