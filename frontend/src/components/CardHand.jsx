/**
 * CardHand Component
 * Displays the player's hand of cards
 */
import PropTypes from 'prop-types'
import Card from './Card'

const CardHand = ({ cards, selectedCards, onCardSelect, disabled }) => {
  if (!cards || cards.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-400 text-lg">No cards in hand</p>
      </div>
    )
  }

  return (
    <div className="w-full">
      <div className="flex gap-3 justify-center max-w-2xl mx-auto">
        {cards.map((card) => (
          <Card
            key={card.id}
            card={card}
            isSelected={selectedCards.includes(card.id)}
            onSelect={onCardSelect}
            disabled={disabled}
          />
        ))}
      </div>
    </div>
  )
}

CardHand.propTypes = {
  cards: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      type: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
    })
  ).isRequired,
  selectedCards: PropTypes.arrayOf(PropTypes.string),
  onCardSelect: PropTypes.func,
  disabled: PropTypes.bool,
}

CardHand.defaultProps = {
  selectedCards: [],
  onCardSelect: null,
  disabled: false,
}

export default CardHand

