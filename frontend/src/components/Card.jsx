/**
 * Card Component
 * Displays a single card with type-based styling
 */
import PropTypes from 'prop-types'

const Card = ({ card, isSelected, onSelect, disabled }) => {
  const getCardColor = (type) => {
    switch (type) {
      case 'element':
        return 'from-red-500 to-orange-500'
      case 'action':
        return 'from-blue-500 to-cyan-500'
      case 'material':
        return 'from-green-500 to-emerald-500'
      default:
        return 'from-gray-500 to-gray-600'
    }
  }

  const getCardIcon = (type) => {
    switch (type) {
      case 'element':
        return '🔥'
      case 'action':
        return '⚔️'
      case 'material':
        return '🛡️'
      default:
        return '🎴'
    }
  }

  const handleClick = () => {
    if (!disabled && onSelect) {
      onSelect(card.id)
    }
  }

  return (
    <div
      onClick={handleClick}
      className={`
        relative p-4 rounded-lg cursor-pointer transition-all duration-200
        bg-gradient-to-br ${getCardColor(card.type)}
        ${isSelected ? 'ring-4 ring-yellow-400 scale-105 shadow-xl' : 'hover:scale-105 shadow-lg'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      {/* Card Icon */}
      <div className="text-3xl mb-2 text-center">
        {getCardIcon(card.type)}
      </div>
      
      {/* Card Name */}
      <h3 className="text-white font-bold text-center text-lg mb-1">
        {card.name}
      </h3>
      
      {/* Card Type Badge */}
      <div className="text-center mb-2">
        <span className="inline-block px-2 py-1 bg-black bg-opacity-30 rounded text-white text-xs uppercase">
          {card.type}
        </span>
      </div>
      
      {/* Card Description */}
      <p className="text-white text-opacity-90 text-sm text-center italic">
        {card.description}
      </p>
      
      {/* Selection Indicator */}
      {isSelected && (
        <div className="absolute top-2 right-2 bg-yellow-400 rounded-full w-6 h-6 flex items-center justify-center">
          <span className="text-black font-bold">✓</span>
        </div>
      )}
    </div>
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

