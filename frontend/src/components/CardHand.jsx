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
      <h2 className="text-2xl font-bold text-white mb-4">Your Hand</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
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
      {selectedCards.length > 0 && (
        <div className="mt-4 text-center">
          <p className="text-white text-sm">
            Selected: <span className="font-bold">{selectedCards.length}</span> card(s)
          </p>
        </div>
      )}
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

