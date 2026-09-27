'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import axios from 'axios';

interface Setting {
  key: string;
  value: any;
}

export default function SettingsPage() {
  const params = useParams();
  const tenantId = params.id as string;
  const [settings, setSettings] = useState<Setting[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newSetting, setNewSetting] = useState({
    key: '',
    value: '',
  });
  const [editingSetting, setEditingSetting] = useState<string | null>(null);

  const commonSettings = [
    'webhook_url',
    'notification_email',
    'api_rate_limit',
    'retention_days',
    'timezone',
  ];

  const loadSetting = async (key: string) => {
    try {
      const response = await axios.get(`/api/v1/tenants/${tenantId}/settings/${key}`);
      const exists = settings.find((s) => s.key === key);
      if (exists) {
        setSettings(settings.map((s) => (s.key === key ? response.data : s)));
      } else {
        setSettings([...settings, response.data]);
      }
    } catch (err: any) {
      // Setting doesn't exist yet, ignore
    }
  };

  useEffect(() => {
    // Load all common settings
    commonSettings.forEach((key) => loadSetting(key));
  }, [tenantId]);

  const handleSaveSetting = async (key: string, value: any) => {
    try {
      const response = await axios.put(`/api/v1/tenants/${tenantId}/settings/${key}`, {
        key,
        value: typeof value === 'string' ? { value } : value,
      });
      setSettings(settings.map((s) => (s.key === key ? response.data : s)));
      setEditingSetting(null);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save setting');
    }
  };

  const handleAddSetting = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await handleSaveSetting(newSetting.key, newSetting.value);
      setNewSetting({ key: '', value: '' });
      setShowAddForm(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add setting');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <Link href={`/dashboard/tenants/${tenantId}`} className="text-blue-600 hover:text-blue-700">
            ← Back to Tenant
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-4">Tenant Settings</h1>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <div className="flex justify-end mb-6">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            + Add Setting
          </button>
        </div>

        {showAddForm && (
          <form onSubmit={handleAddSetting} className="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 className="text-xl font-semibold mb-4">Add New Setting</h2>
            <div className="grid grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Setting Key"
                required
                className="border rounded-lg px-4 py-2"
                value={newSetting.key}
                onChange={(e) => setNewSetting({ ...newSetting, key: e.target.value })}
              />
              <input
                type="text"
                placeholder="Value"
                required
                className="border rounded-lg px-4 py-2"
                value={newSetting.value}
                onChange={(e) => setNewSetting({ ...newSetting, value: e.target.value })}
              />
            </div>
            <div className="flex gap-4 mt-4">
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
              >
                Save
              </button>
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        <div className="space-y-4">
          {commonSettings.map((key) => (
            <div key={key} className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 capitalize">
                    {key.replace(/_/g, ' ')}
                  </h3>
                  {editingSetting === key ? (
                    <div className="flex gap-2">
                      <input
                        type="text"
                        defaultValue={settings.find((s) => s.key === key)?.value?.value || ''}
                        onBlur={(e) => {
                          if (e.target.value) {
                            handleSaveSetting(key, e.target.value);
                          }
                        }}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' && e.currentTarget.value) {
                            handleSaveSetting(key, e.currentTarget.value);
                          }
                        }}
                        className="border rounded-lg px-4 py-2 flex-1"
                        autoFocus
                      />
                    </div>
                  ) : (
                    <p className="text-gray-600">
                      {settings.find((s) => s.key === key)?.value?.value || 'Not set'}
                    </p>
                  )}
                </div>
                <button
                  onClick={() =>
                    setEditingSetting(editingSetting === key ? null : key)
                  }
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  {editingSetting === key ? 'Done' : 'Edit'}
                </button>
              </div>
            </div>
          ))}
        </div>

        {settings.length === 0 && !showAddForm && (
          <div className="bg-white p-8 rounded-lg shadow-md text-center">
            <p className="text-gray-500">No settings configured. Add your first setting to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
}
