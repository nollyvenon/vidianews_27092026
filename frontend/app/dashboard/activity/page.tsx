'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

export default function ActivityPage() {
  const [activities, setActivities] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetchActivities();
    fetchSummary();
  }, [filter]);

  const fetchActivities = async () => {
    try {
      const params = filter ? `?action=${filter}` : '';
      const response = await axios.get(`/api/v1/activity/me${params}`);
      setActivities(response.data);
    } catch (error) {
      console.error('Error loading activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSummary = async () => {
    try {
      const response = await axios.get('/api/v1/activity/me/summary');
      setSummary(response.data);
    } catch (error) {
      console.error('Error loading summary:', error);
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Activity Log</h1>

        {summary && (
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-gray-600">Total Activities</div>
              <div className="text-3xl font-bold text-blue-600">
                {summary.total_activities}
              </div>
              <div className="text-sm text-gray-500">{summary.period_days} days</div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-gray-600">By Action</div>
              <div className="text-lg">
                {Object.keys(summary.by_action || {}).map((action) => (
                  <div key={action} className="text-sm">
                    {action}: {summary.by_action[action]}
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-gray-600">By Entity</div>
              <div className="text-lg">
                {Object.keys(summary.by_entity || {}).map((entity) => (
                  <div key={entity} className="text-sm">
                    {entity}: {summary.by_entity[entity]}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <input
              type="text"
              placeholder="Filter by action..."
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="w-full px-4 py-2 border rounded"
            />
          </div>

          <div className="divide-y divide-gray-200">
            {activities.length === 0 ? (
              <p className="p-6 text-gray-500">No activities found</p>
            ) : (
              activities.map((activity) => (
                <div key={activity.id} className="p-6 hover:bg-gray-50">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold">
                        {activity.action.toUpperCase()} - {activity.entity_type}
                      </h3>
                      {activity.description && (
                        <p className="text-gray-600 mt-1">{activity.description}</p>
                      )}
                      <p className="text-xs text-gray-400 mt-2">
                        {new Date(activity.created_at).toLocaleString()}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded text-sm ${
                        activity.status === 'success'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {activity.status}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
