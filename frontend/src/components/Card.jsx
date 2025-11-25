/**
 * Card Component
 * Displays a single card with type-based styling
 */
import PropTypes from 'prop-types'

const Card = ({ card, isSelected, onSelect, disabled }) => {
  const handleClick = () => {
    if (!disabled && onSelect) {
      onSelect(card.id)
    }
  }

  return (
    <button
      onClick={handleClick}
      disabled={disabled}
      className={`
        w-full p-3 rounded border-2 transition-all duration-200 text-left
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105'}
        ${isSelected
          ? 'border-yellow-400 bg-yellow-900 bg-opacity-30'
          : 'border-gray-600 bg-gray-800 hover:border-gray-500'
        }
      `}
    >
      {/* Card Name */}
      <div className="text-white font-bold text-base uppercase tracking-wide">
        {card.name}
      </div>

      {/* Card Type */}
      <div className="text-gray-400 text-xs uppercase mt-1">
        {card.type}
      </div>
    </button>
  )
}

Card.propTypes = {
  card: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    type: PropTypes.oneOf(['element', 'action', 'material']).isRequired,
    description: PropTypes.string.isRequired,
  }).isRequired,
  isSelected: PropTypes.bool,
  onSelect: PropTypes.func,
  disabled: PropTypes.bool,
}

Card.defaultProps = {
  isSelected: false,
  onSelect: null,
  disabled: false,
}

export default Card

