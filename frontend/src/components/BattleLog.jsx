/**
 * BattleLog Component
 * Displays battle results and history
 */
import PropTypes from 'prop-types'

const BattleLog = ({ battleHistory, playerName, opponentName }) => {
  if (!battleHistory || battleHistory.length === 0) {
    return (
      <div className="w-full bg-gray-800 rounded-lg p-6 shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-4">Battle Log</h2>
        <p className="text-gray-400 text-center py-8">No battles yet. Submit your first prompt!</p>
      </div>
    )
  }

  const getEffectColor = (effect) => {
    const colors = {
      fire: 'text-red-500',
      ice: 'text-blue-400',
      lightning: 'text-yellow-400',
      earth: 'text-green-600',
      water: 'text-cyan-500',
      wind: 'text-gray-300',
      light: 'text-yellow-200',
      dark: 'text-purple-600',
    }
    return colors[effect] || 'text-white'
  }

  return (
    <div className="w-full bg-gray-800 rounded-lg p-6 shadow-xl max-h-96 overflow-y-auto">
      <h2 className="text-2xl font-bold text-white mb-4">Battle Log</h2>
      
      <div className="space-y-4">
        {battleHistory.map((battle, index) => {
          const isPlayerWinner = battle.winner_id === 'player'
          const isTie = !battle.winner_id
          
          return (
            <div
              key={index}
              className={`
                p-4 rounded-lg border-2
                ${isPlayerWinner ? 'bg-green-900 bg-opacity-20 border-green-500' : ''}
                ${!isPlayerWinner && !isTie ? 'bg-red-900 bg-opacity-20 border-red-500' : ''}
                ${isTie ? 'bg-gray-700 border-gray-500' : ''}
              `}
            >
              {/* Turn Header */}
              <div className="flex justify-between items-center mb-2">
                <span className="text-white font-bold">Turn {battle.turn || index + 1}</span>
                <span className={`
                  px-3 py-1 rounded-full text-sm font-bold
                  ${isPlayerWinner ? 'bg-green-600 text-white' : ''}
                  ${!isPlayerWinner && !isTie ? 'bg-red-600 text-white' : ''}
                  ${isTie ? 'bg-gray-600 text-white' : ''}
                `}>
                  {isTie ? 'TIE' : isPlayerWinner ? 'VICTORY' : 'DEFEAT'}
                </span>
              </div>
              
              {/* Damage */}
              <div className="text-white mb-2">
                <span className="font-semibold">Damage:</span>{' '}
                <span className="text-red-400 font-bold">{battle.damage_dealt}</span> HP
              </div>
              
              {/* Reasoning */}
              <p className="text-gray-300 text-sm mb-2 italic">
                "{battle.reasoning}"
              </p>
              
              {/* Scores */}
              <div className="flex gap-4 text-sm">
                <div className="text-gray-400">
                  <span className="font-semibold">Creativity:</span>{' '}
                  <span className="text-purple-400">{battle.creativity_score}/10</span>
                </div>
                <div className="text-gray-400">
                  <span className="font-semibold">Adherence:</span>{' '}
                  <span className="text-blue-400">{battle.adherence_score}/10</span>
                </div>
              </div>
              
              {/* Visual Effects */}
              {battle.visual_effects && battle.visual_effects.length > 0 && (
                <div className="mt-2 flex gap-2 flex-wrap">
                  {battle.visual_effects.map((effect, i) => (
                    <span
                      key={i}
                      className={`text-xs px-2 py-1 rounded ${getEffectColor(effect.effect)} bg-black bg-opacity-30`}
                    >
                      {effect.effect}
                    </span>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

BattleLog.propTypes = {
  battleHistory: PropTypes.arrayOf(
    PropTypes.shape({
      winner_id: PropTypes.string,
      damage_dealt: PropTypes.number.isRequired,
      reasoning: PropTypes.string.isRequired,
      creativity_score: PropTypes.number.isRequired,
      adherence_score: PropTypes.number.isRequired,
      visual_effects: PropTypes.arrayOf(
        PropTypes.shape({
          effect: PropTypes.string.isRequired,
          intensity: PropTypes.number,
          color: PropTypes.string,
        })
      ),
      turn: PropTypes.number,
    })
  ),
  playerName: PropTypes.string,
  opponentName: PropTypes.string,
}

BattleLog.defaultProps = {
  battleHistory: [],
  playerName: 'You',
  opponentName: 'Opponent',
}

export default BattleLog

