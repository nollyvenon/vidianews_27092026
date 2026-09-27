'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import axios from 'axios';

interface Member {
  id: number;
  user_id: number;
  role: string;
  status: string;
  is_owner: boolean;
  joined_at: string;
}

export default function MembersPage() {
  const params = useParams();
  const tenantId = params.id as string;
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showInviteForm, setShowInviteForm] = useState(false);
  const [inviteData, setInviteData] = useState({
    email: '',
    role: 'member',
  });

  useEffect(() => {
    fetchMembers();
  }, [tenantId]);

  const fetchMembers = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/v1/tenants/${tenantId}/members`);
      setMembers(response.data);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load members');
    } finally {
      setLoading(false);
    }
  };

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post(`/api/v1/tenants/${tenantId}/invite`, inviteData);
      setInviteData({ email: '', role: 'member' });
      setShowInviteForm(false);
      setError('');
      // Refresh members
      await fetchMembers();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send invitation');
    }
  };

  const handleRemoveMember = async (userId: number) => {
    if (window.confirm('Remove this member from the tenant?')) {
      try {
        await axios.delete(`/api/v1/tenants/${tenantId}/members/${userId}`);
        await fetchMembers();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to remove member');
      }
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <Link href={`/dashboard/tenants/${tenantId}`} className="text-blue-600 hover:text-blue-700">
            ← Back to Tenant
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 mt-4">Team Members</h1>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <div className="flex justify-end mb-6">
          <button
            onClick={() => setShowInviteForm(!showInviteForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
          >
            + Invite Member
          </button>
        </div>

        {showInviteForm && (
          <form onSubmit={handleInvite} className="bg-white p-6 rounded-lg shadow-md mb-8">
            <h2 className="text-xl font-semibold mb-4">Invite Member</h2>
            <div className="grid grid-cols-2 gap-4">
              <input
                type="email"
                placeholder="Email"
                required
                className="border rounded-lg px-4 py-2"
                value={inviteData.email}
                onChange={(e) => setInviteData({ ...inviteData, email: e.target.value })}
              />
              <select
                className="border rounded-lg px-4 py-2"
                value={inviteData.role}
                onChange={(e) => setInviteData({ ...inviteData, role: e.target.value })}
              >
                <option value="member">Member</option>
                <option value="editor">Editor</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div className="flex gap-4 mt-4">
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
              >
                Send Invitation
              </button>
              <button
                type="button"
                onClick={() => setShowInviteForm(false)}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Member</th>
                <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Role</th>
                <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Status</th>
                <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Joined</th>
                <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody divide-y divide-gray-200">
              {members.map((member) => (
                <tr key={member.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm text-gray-900">
                    <span className="font-medium">User #{member.user_id}</span>
                    {member.is_owner && <span className="ml-2 text-blue-600 text-xs font-medium">OWNER</span>}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-700">{member.role}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      member.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {member.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-700">
                    {new Date(member.joined_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    {!member.is_owner && (
                      <button
                        onClick={() => handleRemoveMember(member.user_id)}
                        className="text-red-600 hover:text-red-700 font-medium"
                      >
                        Remove
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
