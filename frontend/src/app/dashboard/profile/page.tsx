'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState<any>({});
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await axios.get('/api/v1/profiles/me');
      setProfile(response.data);
      setFormData(response.data);
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.put('/api/v1/profiles/me', formData);
      setProfile(response.data);
      setEditMode(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;
  if (!profile) return <div className="p-8">Profile not found</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md">
          {/* Tabs */}
          <div className="border-b border-gray-200 flex space-x-8 px-6">
            {['profile', 'skills', 'experience', 'education'].map((tab) => (
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
          <div className="p-6">
            {activeTab === 'profile' && (
              <div>
                {!editMode ? (
                  <>
                    <div className="grid grid-cols-2 gap-6 mb-6">
                      <div>
                        <label className="text-sm text-gray-500">Title</label>
                        <p className="text-lg font-semibold">{profile.title || '-'}</p>
                      </div>
                      <div>
                        <label className="text-sm text-gray-500">Location</label>
                        <p className="text-lg">{profile.location || '-'}</p>
                      </div>
                      <div className="col-span-2">
                        <label className="text-sm text-gray-500">Bio</label>
                        <p className="text-lg">{profile.bio || '-'}</p>
                      </div>
                    </div>
                    <button
                      onClick={() => setEditMode(true)}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                    >
                      Edit Profile
                    </button>
                  </>
                ) : (
                  <form onSubmit={handleUpdate}>
                    <input
                      type="text"
                      placeholder="Title"
                      value={formData.title || ''}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      className="border rounded-lg px-4 py-2 w-full mb-4"
                    />
                    <input
                      type="text"
                      placeholder="Location"
                      value={formData.location || ''}
                      onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                      className="border rounded-lg px-4 py-2 w-full mb-4"
                    />
                    <textarea
                      placeholder="Bio"
                      value={formData.bio || ''}
                      onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                      className="border rounded-lg px-4 py-2 w-full mb-4"
                      rows={4}
                    />
                    <div className="flex gap-4">
                      <button
                        type="submit"
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                      >
                        Save
                      </button>
                      <button
                        type="button"
                        onClick={() => setEditMode(false)}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-2 rounded-lg"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                )}
              </div>
            )}

            {activeTab === 'skills' && (
              <div>
                <p className="text-gray-500">Skills management coming soon</p>
              </div>
            )}

            {activeTab === 'experience' && (
              <div>
                <p className="text-gray-500">Experience management coming soon</p>
              </div>
            )}

            {activeTab === 'education' && (
              <div>
                <p className="text-gray-500">Education management coming soon</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
