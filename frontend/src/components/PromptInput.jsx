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
    <div className="w-full max-w-4xl mx-auto">
      {/* Text Area */}
      <textarea
        value={value}
        onChange={handleChange}
        disabled={disabled}
        maxLength={maxLength}
        placeholder="I shoot a fire arrow at the opponent..."
        className="w-full h-24 px-3 py-2 bg-gray-800 text-white rounded border-2 border-gray-600
                   focus:border-blue-500 focus:outline-none resize-none text-sm
                   disabled:opacity-50 disabled:cursor-not-allowed"
      />

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={!canSubmit}
        className={`
          mt-2 w-full py-3 px-6 rounded font-bold text-base transition-all
          ${canSubmit
            ? 'bg-blue-600 hover:bg-blue-700 text-white'
            : 'bg-gray-700 text-gray-500 cursor-not-allowed'
          }
        `}
      >
        {disabled ? 'Waiting...' : 'CAST'}
      </button>

      {/* Validation Messages */}
      {!disabled && selectedCards.length === 0 && (
        <p className="mt-1 text-xs text-yellow-400 text-center">Select at least 1 card</p>
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

