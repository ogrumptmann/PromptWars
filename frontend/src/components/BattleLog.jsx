/**
 * BattleLog Component
 * Displays battle results and history
 */
import PropTypes from 'prop-types'

const BattleLog = ({ battleHistory, playerName, opponentName }) => {
  if (!battleHistory || battleHistory.length === 0) {
    return (
      <div className="w-full bg-gray-900 p-4">
        <h2 className="text-lg font-bold text-white mb-2">Battle Log</h2>
        <p className="text-gray-500 text-sm">No battles yet. Submit your first prompt!</p>
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
    <div className="w-full bg-gray-900 p-4 max-w-4xl mx-auto">
      <h2 className="text-lg font-bold text-white mb-3">Battle Log</h2>

      <div className="space-y-3 max-h-48 overflow-y-auto">
        {[...battleHistory].reverse().map((battle, index) => {
          const isPlayerWinner = battle.winner_id === 'player_1'
          const isOpponentWinner = battle.winner_id === 'player_2'
          const isTie = !battle.winner_id

          // Get visual effect color if available
          let effectColor = 'text-gray-400'
          if (battle.visual_effects && battle.visual_effects.length > 0) {
            const effect = battle.visual_effects[0].particle_type
            effectColor = getEffectColor(effect)
          }

          return (
            <div key={index} className="bg-gray-800 rounded-lg p-3 border-l-4 border-gray-700">
              {/* Winner Badge */}
              <div className="flex items-center gap-2 mb-2">
                {isPlayerWinner && (
                  <span className="px-2 py-1 bg-green-900 text-green-400 text-xs font-bold rounded uppercase">
                    🏆 {playerName} Wins!
                  </span>
                )}
                {isOpponentWinner && (
                  <span className="px-2 py-1 bg-red-900 text-red-400 text-xs font-bold rounded uppercase">
                    💀 {opponentName} Wins!
                  </span>
                )}
                {isTie && (
                  <span className="px-2 py-1 bg-gray-700 text-gray-400 text-xs font-bold rounded uppercase">
                    ⚔️ Tie!
                  </span>
                )}
                <span className="text-yellow-400 text-xs font-semibold">
                  {battle.damage_dealt} damage
                </span>
              </div>

              {/* AI Story */}
              {battle.reasoning && (
                <p className={`text-sm leading-relaxed ${effectColor} italic`}>
                  "{battle.reasoning}"
                </p>
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
      reasoning: PropTypes.string,
      creativity_score: PropTypes.number,
      adherence_score: PropTypes.number,
      visual_effects: PropTypes.array,
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

