'use client'
import { useState, useEffect } from 'react'

export default function LocalizationPage() {
  const [languages, setLanguages] = useState([])
  const [selectedLanguage, setSelectedLanguage] = useState('en')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchLanguages()
  }, [])

  const fetchLanguages = async () => {
    try {
      const res = await fetch('/api/v1/languages')
      if (res.ok) {
        const data = await res.json()
        setLanguages(data)
      }
    } catch (err) {
      console.error('Failed to fetch languages:', err)
    }
  }

  const handleSetLanguage = async (langCode) => {
    setLoading(true)
    try {
      const res = await fetch('/api/v1/localization/language', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language_code: langCode })
      })
      if (res.ok) {
        setSelectedLanguage(langCode)
      }
    } catch (err) {
      console.error('Failed to set language:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Language & Localization</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-2xl font-semibold mb-4">Select Language</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {languages.map(lang => (
            <button
              key={lang.code}
              onClick={() => handleSetLanguage(lang.code)}
              disabled={loading}
              className={`p-4 rounded-lg font-semibold transition ${
                selectedLanguage === lang.code
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
              } disabled:opacity-50`}
            >
              {lang.name}
            </button>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-semibold mb-4">Localization Settings</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Current Language</label>
            <p className="text-lg">{selectedLanguage.toUpperCase()}</p>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Date Format</label>
            <select className="w-full px-3 py-2 border rounded-lg">
              <option>MM/DD/YYYY</option>
              <option>DD/MM/YYYY</option>
              <option>YYYY-MM-DD</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Time Zone</label>
            <select className="w-full px-3 py-2 border rounded-lg">
              <option>UTC</option>
              <option>EST</option>
              <option>PST</option>
            </select>
          </div>
          <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
            Save Settings
          </button>
        </div>
      </div>
    </div>
  )
}
