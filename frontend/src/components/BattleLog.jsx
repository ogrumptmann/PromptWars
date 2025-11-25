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

      <div className="space-y-1 max-h-32 overflow-y-auto text-sm font-mono">
        {[...battleHistory].reverse().map((battle, index) => {
          const isPlayerWinner = battle.winner_id === 'player_1'
          const isOpponentWinner = battle.winner_id === 'player_2'
          const isTie = !battle.winner_id

          return (
            <div key={index} className="text-gray-300">
              <span className="text-gray-500">&gt;</span>{' '}
              {isPlayerWinner && (
                <span className="text-green-400">{playerName} Won!</span>
              )}
              {isOpponentWinner && (
                <span className="text-red-400">{opponentName} Won!</span>
              )}
              {isTie && (
                <span className="text-gray-400">Tie!</span>
              )}
              {' '}({battle.damage_dealt} damage)
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

