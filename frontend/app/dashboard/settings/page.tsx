'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

export default function SettingsPage() {
  const [settings, setSettings] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('notifications');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get('/api/v1/settings/me');
      setSettings(response.data);
    } catch (error) {
      console.error('Error loading settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (section: string, key: string, value: boolean) => {
    try {
      await axios.put(`/api/v1/settings/me/${section}`, {
        [key]: value
      });
      setSettings(prev => ({
        ...prev,
        [section]: { ...prev[section], [key]: value }
      }));
    } catch (error) {
      console.error('Error updating settings:', error);
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;
  if (!settings) return <div className="p-8">Settings not found</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Settings</h1>

        <div className="bg-white rounded-lg shadow-md">
          {/* Tabs */}
          <div className="border-b border-gray-200 flex space-x-8 px-6">
            {['notifications', 'privacy', 'display'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="p-6 space-y-4">
            {activeTab === 'notifications' && settings.notifications && (
              <>
                <div className="flex justify-between items-center">
                  <label className="font-medium">Activity Notifications</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.email_on_activity}
                    onChange={(e) => handleToggle('notifications', 'email_on_activity', e.target.checked)}
                    className="w-4 h-4"
                  />
                </div>
                <div className="flex justify-between items-center">
                  <label className="font-medium">Push Notifications</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.push_enabled}
                    onChange={(e) => handleToggle('notifications', 'push_enabled', e.target.checked)}
                    className="w-4 h-4"
                  />
                </div>
                <div className="flex justify-between items-center">
                  <label className="font-medium">In-App Notifications</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.inapp_enabled}
                    onChange={(e) => handleToggle('notifications', 'inapp_enabled', e.target.checked)}
                    className="w-4 h-4"
                  />
                </div>
              </>
            )}

            {activeTab === 'privacy' && settings.privacy && (
              <>
                <div className="flex justify-between items-center">
                  <label className="font-medium">Public Profile</label>
                  <select
                    value={settings.privacy.profile_visibility}
                    onChange={(e) => handleToggle('privacy', 'profile_visibility', e.target.value === 'public')}
                    className="border rounded px-2 py-1"
                  >
                    <option value="private">Private</option>
                    <option value="public">Public</option>
                  </select>
                </div>
                <div className="flex justify-between items-center">
                  <label className="font-medium">Allow Messages</label>
                  <input
                    type="checkbox"
                    checked={settings.privacy.allow_messages === 'everyone'}
                    onChange={(e) => handleToggle('privacy', 'allow_messages', e.target.checked)}
                    className="w-4 h-4"
                  />
                </div>
              </>
            )}

            {activeTab === 'display' && settings.display && (
              <>
                <div className="flex justify-between items-center">
                  <label className="font-medium">Theme</label>
                  <select
                    value={settings.display.theme}
                    onChange={(e) => handleToggle('display', 'theme', e.target.value === 'dark')}
                    className="border rounded px-2 py-1"
                  >
                    <option value="light">Light</option>
                    <option value="dark">Dark</option>
                    <option value="auto">Auto</option>
                  </select>
                </div>
                <div className="flex justify-between items-center">
                  <label className="font-medium">Language</label>
                  <select
                    value={settings.display.language}
                    className="border rounded px-2 py-1"
                  >
                    <option value="en">English</option>
                    <option value="es">Español</option>
                    <option value="fr">Français</option>
                  </select>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
