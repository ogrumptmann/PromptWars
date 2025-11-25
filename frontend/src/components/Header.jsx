/**
 * Header Component
 * Displays round number and countdown timer
 */
import PropTypes from 'prop-types'

const Header = ({ round, timeRemaining, maxTime = 45 }) => {
  // Calculate percentage for visual indicator
  const timePercentage = (timeRemaining / maxTime) * 100
  
  // Determine color based on time remaining
  const getTimeColor = () => {
    if (timePercentage > 66) return 'text-green-400'
    if (timePercentage > 33) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getTimerBgColor = () => {
    if (timePercentage > 66) return 'bg-green-500'
    if (timePercentage > 33) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className="w-full bg-gray-900 border-b-2 border-gray-700 p-4">
      <div className="flex justify-between items-center max-w-4xl mx-auto">
        {/* Round Number */}
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-sm uppercase tracking-wide">Round</span>
          <span className="text-white text-2xl font-bold">{round}</span>
        </div>

        {/* Timer */}
        <div className="flex items-center gap-3">
          <div className="flex flex-col items-end">
            <div className="flex items-center gap-2">
              <span className="text-2xl">⏱</span>
              <span className={`text-2xl font-bold ${getTimeColor()}`}>
                {timeRemaining}s
              </span>
            </div>
            {/* Timer progress bar */}
            <div className="w-24 h-1 bg-gray-700 rounded-full mt-1 overflow-hidden">
              <div
                className={`h-full ${getTimerBgColor()} transition-all duration-1000`}
                style={{ width: `${timePercentage}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

Header.propTypes = {
  round: PropTypes.number.isRequired,
  timeRemaining: PropTypes.number.isRequired,
  maxTime: PropTypes.number,
}

export default Header

