'use client'
import { useState, useEffect } from 'react'

export default function GamificationPage() {
  const [leaderboard, setLeaderboard] = useState([])
  const [userBadges, setUserBadges] = useState([])

  useEffect(() => {
    fetchLeaderboard()
    fetchUserBadges()
  }, [])

  const fetchLeaderboard = async () => {
    try {
      const res = await fetch('/api/v1/leaderboard')
      if (res.ok) {
        const data = await res.json()
        setLeaderboard(data)
      }
    } catch (err) {
      console.error('Failed to fetch leaderboard:', err)
    }
  }

  const fetchUserBadges = async () => {
    try {
      const res = await fetch('/api/v1/badges/user')
      if (res.ok) {
        const data = await res.json()
        setUserBadges(data)
      }
    } catch (err) {
      console.error('Failed to fetch badges:', err)
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Badges & Gamification</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Your Badges</h2>
          <div className="grid grid-cols-3 gap-4">
            {userBadges.map(badge => (
              <div key={badge.id} className="bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-lg p-4 text-center text-white">
                <div className="text-3xl mb-2">🏅</div>
                <p className="text-sm font-semibold">{badge.name}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Top Leaderboard</h2>
          <div className="space-y-3">
            {leaderboard.map(entry => (
              <div key={entry.rank} className="flex justify-between items-center py-2 border-b">
                <span className="text-lg font-semibold">#{entry.rank}</span>
                <div className="flex-1 ml-4">
                  <p className="font-medium">{entry.points} points</p>
                </div>
                <span className="text-sm text-gray-600">{entry.views} views</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
