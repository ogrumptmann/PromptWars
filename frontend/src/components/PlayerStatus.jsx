/**
 * PlayerStatus Component
 * Displays player HP, name, and Elo rating
 */
import PropTypes from 'prop-types'

const PlayerStatus = ({ player, isOpponent }) => {
  const hpPercentage = (player.hp / 100) * 100
  
  const getHPColor = (hp) => {
    if (hp > 66) return 'bg-green-500'
    if (hp > 33) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className={`
      bg-gray-800 rounded-lg p-6 shadow-xl
      ${isOpponent ? 'border-2 border-red-500' : 'border-2 border-blue-500'}
    `}>
      {/* Player Name and Role */}
      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="text-2xl font-bold text-white">
            {player.username || (isOpponent ? 'Opponent' : 'You')}
          </h3>
          <p className="text-gray-400 text-sm">
            {isOpponent ? '🔴 Enemy' : '🔵 You'}
          </p>
        </div>
        <div className="text-right">
          <p className="text-gray-400 text-sm">Elo Rating</p>
          <p className="text-yellow-400 font-bold text-xl">{player.elo_rating || 1200}</p>
        </div>
      </div>

      {/* HP Bar */}
      <div className="mb-2">
        <div className="flex justify-between items-center mb-1">
          <span className="text-white font-semibold">HP</span>
          <span className="text-white font-bold">{player.hp} / 100</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-6 overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ${getHPColor(player.hp)} flex items-center justify-center`}
            style={{ width: `${hpPercentage}%` }}
          >
            {player.hp > 10 && (
              <span className="text-white text-xs font-bold">{player.hp}%</span>
            )}
          </div>
        </div>
      </div>

      {/* Status Indicators */}
      <div className="flex gap-2 mt-4">
        {player.hp === 0 && (
          <span className="px-3 py-1 bg-red-600 text-white rounded-full text-xs font-bold">
            💀 DEFEATED
          </span>
        )}
        {player.hp === 100 && (
          <span className="px-3 py-1 bg-green-600 text-white rounded-full text-xs font-bold">
            ✨ FULL HP
          </span>
        )}
        {player.hp > 0 && player.hp < 30 && (
          <span className="px-3 py-1 bg-yellow-600 text-white rounded-full text-xs font-bold animate-pulse">
            ⚠️ LOW HP
          </span>
        )}
      </div>
    </div>
  )
}

PlayerStatus.propTypes = {
  player: PropTypes.shape({
    id: PropTypes.string,
    username: PropTypes.string,
    hp: PropTypes.number.isRequired,
    elo_rating: PropTypes.number,
  }).isRequired,
  isOpponent: PropTypes.bool,
}

PlayerStatus.defaultProps = {
  isOpponent: false,
}

export default PlayerStatus

