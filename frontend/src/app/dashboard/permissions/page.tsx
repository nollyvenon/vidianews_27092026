'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Permission {
  id: number
  name: string
  resource: string
  action: string
  category: string
}

interface Role {
  id: number
  name: string
  description: string | null
  is_system: boolean
}

/** Roles and permissions of the platform, with role creation and role assignment to a user. */
export default function PermissionsPage() {
  const [permissions, setPermissions] = useState<Permission[] | null>(null)
  const [roles, setRoles] = useState<Role[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [roleName, setRoleName] = useState('')
  const [roleDescription, setRoleDescription] = useState('')
  const [userId, setUserId] = useState('')
  const [roleId, setRoleId] = useState('')
  const [userRoles, setUserRoles] = useState<Role[] | null>(null)

  const load = () => {
    ApiClient.get('/permissions?skip=0&limit=200')
      .then((data: Permission[]) => setPermissions(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Permissions could not be loaded.')))
    ApiClient.get('/roles?skip=0&limit=200')
      .then((data: Role[]) => setRoles(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Roles could not be loaded.')))
  };

  useEffect(() => {
    load();
  }, []);

  const createRole = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      await ApiClient.post('/roles', { name: roleName.trim(), description: roleDescription.trim() });
      setRoleName('');
      setRoleDescription('');
      setNotice('Role created.');
      load();
    } catch (err) {
      setError(errorMessage(err, 'The role could not be created.'));
    }
  };

  const showUserRoles = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      setUserRoles(await ApiClient.get(`/users/${Number(userId)}/roles`));
    } catch (err) {
      setError(errorMessage(err, 'The user’s roles could not be loaded.'));
    }
  };

  const assignRole = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    try {
      await ApiClient.post(`/users/${Number(userId)}/roles/${Number(roleId)}`, {});
      setNotice('Role assigned.');
      setUserRoles(await ApiClient.get(`/users/${Number(userId)}/roles`));
    } catch (err) {
      setError(errorMessage(err, 'The role could not be assigned.'));
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Permissions</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      {notice && <p role="status" className="text-green-700">{notice}</p>}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Roles</h2>
        {roles === null ? (
          <p className="text-gray-500">Loading roles…</p>
        ) : roles.length === 0 ? (
          <p className="text-gray-500">No roles defined yet.</p>
        ) : (
          <ul className="space-y-2">
            {roles.map((role) => (
              <li key={role.id} className="border rounded p-3">
                <span className="font-medium">{role.name}</span>
                {role.is_system && <span className="ml-2 text-xs text-gray-500">(system)</span>}
                {role.description && <p className="text-sm text-gray-600">{role.description}</p>}
              </li>
            ))}
          </ul>
        )}
        <form onSubmit={createRole} className="mt-4 flex flex-wrap gap-2 items-end">
          <input className="border rounded px-2 py-1" placeholder="Role name" value={roleName} onChange={(e) => setRoleName(e.target.value)} required />
          <input className="border rounded px-2 py-1" placeholder="Description" value={roleDescription} onChange={(e) => setRoleDescription(e.target.value)} />
          <button type="submit" disabled={!roleName.trim()} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50">Create role</button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Permissions</h2>
        {permissions === null ? (
          <p className="text-gray-500">Loading permissions…</p>
        ) : permissions.length === 0 ? (
          <p className="text-gray-500">No permissions defined yet.</p>
        ) : (
          <table className="min-w-full text-sm">
            <thead className="text-left text-gray-600">
              <tr>
                <th className="py-2">Name</th>
                <th className="py-2">Resource</th>
                <th className="py-2">Action</th>
                <th className="py-2">Category</th>
              </tr>
            </thead>
            <tbody>
              {permissions.map((permission) => (
                <tr key={permission.id} className="border-t">
                  <td className="py-2">{permission.name}</td>
                  <td className="py-2">{permission.resource}</td>
                  <td className="py-2">{permission.action}</td>
                  <td className="py-2">{permission.category}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <h2 className="text-xl font-semibold">Member roles</h2>
        <form onSubmit={showUserRoles} className="flex gap-2 items-end">
          <label className="text-sm">
            <span className="block text-xs text-gray-600">User ID</span>
            <input type="number" min={1} className="border rounded px-2 py-1" value={userId} onChange={(e) => setUserId(e.target.value)} required />
          </label>
          <button type="submit" className="px-3 py-1 border border-blue-600 text-blue-600 rounded">Show roles</button>
        </form>
        {userRoles && (
          <ul className="text-sm space-y-1">
            {userRoles.length === 0 ? <li className="text-gray-500">No roles assigned.</li> : userRoles.map((role) => <li key={role.id}>{role.name}</li>)}
          </ul>
        )}
        <form onSubmit={assignRole} className="flex gap-2 items-end">
          <label className="text-sm">
            <span className="block text-xs text-gray-600">Role</span>
            <select aria-label="Role to assign" className="border rounded px-2 py-1" value={roleId} onChange={(e) => setRoleId(e.target.value)} required>
              <option value="">Choose a role</option>
              {(roles ?? []).map((role) => (
                <option key={role.id} value={role.id}>{role.name}</option>
              ))}
            </select>
          </label>
          <button type="submit" disabled={!userId || !roleId} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50">Assign role</button>
        </form>
      </div>
    </div>
  );
}
