/**
 * Arena Component
 * Visual battle area showing player avatars and HP bars
 * Placeholder for future PixiJS integration (Phase 2)
 */
import PropTypes from 'prop-types'

const Arena = ({ playerHP, opponentHP, playerName = 'You', opponentName = 'Opponent' }) => {
  const maxHP = 100

  // Calculate HP percentages
  const playerHPPercent = (playerHP / maxHP) * 100
  const opponentHPPercent = (opponentHP / maxHP) * 100

  // Get HP bar color based on percentage
  const getHPColor = (percent) => {
    if (percent > 66) return 'bg-green-500'
    if (percent > 33) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className="w-full bg-gray-900 border-b-2 border-gray-700 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Arena Canvas Placeholder */}
        <div className="relative bg-black rounded-lg p-8 min-h-[200px] flex items-center justify-between">
          {/* Player Avatar (Left) */}
          <div className="flex flex-col items-center gap-2">
            <div className="text-6xl">👤</div>
            <div className="text-white text-sm font-semibold">{playerName}</div>
            {/* Player HP Bar */}
            <div className="w-32">
              <div className="flex justify-between text-xs text-gray-400 mb-1">
                <span>HP</span>
                <span>{playerHP}/{maxHP}</span>
              </div>
              <div className="w-full h-3 bg-gray-800 rounded-full overflow-hidden border border-gray-600">
                <div
                  className={`h-full ${getHPColor(playerHPPercent)} transition-all duration-500`}
                  style={{ width: `${playerHPPercent}%` }}
                />
              </div>
            </div>
          </div>

          {/* VS Indicator (Center) */}
          <div className="text-4xl font-bold text-gray-600">VS</div>

          {/* Opponent Avatar (Right) */}
          <div className="flex flex-col items-center gap-2">
            <div className="text-6xl">🤖</div>
            <div className="text-white text-sm font-semibold">{opponentName}</div>
            {/* Opponent HP Bar */}
            <div className="w-32">
              <div className="flex justify-between text-xs text-gray-400 mb-1">
                <span>HP</span>
                <span>{opponentHP}/{maxHP}</span>
              </div>
              <div className="w-full h-3 bg-gray-800 rounded-full overflow-hidden border border-gray-600">
                <div
                  className={`h-full ${getHPColor(opponentHPPercent)} transition-all duration-500`}
                  style={{ width: `${opponentHPPercent}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Note for future PixiJS integration */}
        <div className="text-center text-gray-500 text-xs mt-2">
          ✨ Visual effects will appear here in Phase 2 (PixiJS)
        </div>
      </div>
    </div>
  )
}

Arena.propTypes = {
  playerHP: PropTypes.number.isRequired,
  opponentHP: PropTypes.number.isRequired,
  playerName: PropTypes.string,
  opponentName: PropTypes.string,
}

export default Arena

