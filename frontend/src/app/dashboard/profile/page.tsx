'use client';

import { FormEvent, useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';

interface Profile {
  title: string | null;
  location: string | null;
  bio: string | null;
  timezone: string;
  is_public: boolean;
}

interface Skill {
  id: number;
  name: string;
  category: string | null;
  proficiency: string;
  years_experience: number;
  endorsed_count: number;
}

interface Experience {
  id: number;
  company: string;
  title: string;
  start_date: string;
  end_date: string | null;
  current: boolean;
  description: string | null;
}

interface Education {
  id: number;
  school: string;
  degree: string | null;
  field: string | null;
  start_date: string;
  end_date: string | null;
}

type Tab = 'profile' | 'skills' | 'experience' | 'education';
const TABS: Tab[] = ['profile', 'skills', 'experience', 'education'];
const PROFICIENCY = ['beginner', 'intermediate', 'advanced', 'expert'];

/** A date from a date input as the start of that day, in the form the API expects. */
const asDateTime = (day: string) => `${day}T00:00:00Z`;

export default function ProfilePage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [profileError, setProfileError] = useState<string | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState<Profile | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('profile');
  const [error, setError] = useState<string | null>(null);
  const [skills, setSkills] = useState<Skill[] | null>(null);
  const [experiences, setExperiences] = useState<Experience[] | null>(null);
  const [educations, setEducations] = useState<Education[] | null>(null);
  const [skillName, setSkillName] = useState('');
  const [skillLevel, setSkillLevel] = useState(PROFICIENCY[1]);
  const [skillYears, setSkillYears] = useState('0');
  const [expForm, setExpForm] = useState({ company: '', title: '', start: '', end: '', current: false, description: '' });
  const [eduForm, setEduForm] = useState({ school: '', degree: '', field: '', start: '', end: '' });

  useEffect(() => {
    ApiClient.get('/profiles/me')
      .then((data: Profile) => {
        setProfile(data);
        setFormData(data);
      })
      .catch((err) => setProfileError(errorMessage(err, 'Your profile could not be loaded.')));
  }, []);

  useEffect(() => {
    if (!user) return;
    loadSections(user.id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.id]);

  const loadSections = (userId: number) => {
    ApiClient.get(`/profiles/${userId}/skills`)
      .then((data: Skill[]) => setSkills(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Skills could not be loaded.')));
    ApiClient.get(`/profiles/${userId}/experiences`)
      .then((data: Experience[]) => setExperiences(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Experience could not be loaded.')));
    ApiClient.get(`/profiles/${userId}/educations`)
      .then((data: Education[]) => setEducations(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Education could not be loaded.')));
  };

  const handleUpdate = async (e: FormEvent) => {
    e.preventDefault();
    if (!formData) return;
    setError(null);
    try {
      const updated: Profile = await ApiClient.put('/profiles/me', formData);
      setProfile(updated);
      setFormData(updated);
      setEditMode(false);
    } catch (err) {
      setError(errorMessage(err, 'Your profile could not be saved.'));
    }
  };

  const addSkill = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await ApiClient.post('/profiles/me/skills', {
        name: skillName.trim(),
        proficiency: skillLevel,
        years_experience: Number(skillYears) || 0,
      });
      setSkillName('');
      setSkillYears('0');
      if (user) loadSections(user.id);
    } catch (err) {
      setError(errorMessage(err, 'The skill could not be added.'));
    }
  };

  const removeItem = async (path: string, reload: () => void) => {
    setError(null);
    try {
      await ApiClient.delete(path);
      reload();
    } catch (err) {
      setError(errorMessage(err, 'The entry could not be removed.'));
    }
  };

  const addExperience = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await ApiClient.post('/profiles/me/experiences', {
        company: expForm.company.trim(),
        title: expForm.title.trim(),
        start_date: asDateTime(expForm.start),
        end_date: expForm.current || !expForm.end ? null : asDateTime(expForm.end),
        current: expForm.current,
        description: expForm.description.trim() || null,
      });
      setExpForm({ company: '', title: '', start: '', end: '', current: false, description: '' });
      if (user) loadSections(user.id);
    } catch (err) {
      setError(errorMessage(err, 'The experience could not be added.'));
    }
  };

  const addEducation = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await ApiClient.post('/profiles/me/educations', {
        school: eduForm.school.trim(),
        degree: eduForm.degree.trim() || null,
        field: eduForm.field.trim() || null,
        start_date: asDateTime(eduForm.start),
        end_date: eduForm.end ? asDateTime(eduForm.end) : null,
      });
      setEduForm({ school: '', degree: '', field: '', start: '', end: '' });
      if (user) loadSections(user.id);
    } catch (err) {
      setError(errorMessage(err, 'The education could not be added.'));
    }
  };

  if (!profile && !profileError) return <div className="p-8">Loading...</div>;
  if (!profile) return <div role="alert" className="p-8 text-red-700">{profileError}</div>;

  const reloadSections = () => {
    if (user) loadSections(user.id);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md">
          {/* Tabs */}
          <div className="border-b border-gray-200 flex space-x-8 px-6">
            {TABS.map((tab) => (
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
            {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

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
                      value={formData?.title ?? ''}
                      onChange={(e) => setFormData({ ...(formData as Profile), title: e.target.value })}
                      className="border rounded-lg px-4 py-2 w-full mb-4"
                    />
                    <input
                      type="text"
                      placeholder="Location"
                      value={formData?.location ?? ''}
                      onChange={(e) => setFormData({ ...(formData as Profile), location: e.target.value })}
                      className="border rounded-lg px-4 py-2 w-full mb-4"
                    />
                    <textarea
                      placeholder="Bio"
                      value={formData?.bio ?? ''}
                      onChange={(e) => setFormData({ ...(formData as Profile), bio: e.target.value })}
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
                        onClick={() => {
                          setFormData(profile);
                          setEditMode(false);
                        }}
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
              <div className="space-y-4">
                {skills === null ? (
                  <p className="text-gray-500">Loading skills…</p>
                ) : skills.length === 0 ? (
                  <p className="text-gray-500">No skills added yet.</p>
                ) : (
                  <ul className="space-y-2">
                    {skills.map((skill) => (
                      <li key={skill.id} className="flex justify-between items-center border rounded p-3">
                        <span>
                          <span className="font-medium">{skill.name}</span> · {skill.proficiency} · {skill.years_experience} yrs · {skill.endorsed_count} endorsements
                        </span>
                        <button type="button" onClick={() => removeItem(`/profiles/skills/${skill.id}`, reloadSections)} className="text-sm text-red-600 hover:underline">
                          Remove
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
                <form onSubmit={addSkill} className="flex flex-wrap gap-2 items-end">
                  <input className="border rounded px-2 py-1" placeholder="Skill" value={skillName} onChange={(e) => setSkillName(e.target.value)} required />
                  <select aria-label="Proficiency" className="border rounded px-2 py-1" value={skillLevel} onChange={(e) => setSkillLevel(e.target.value)}>
                    {PROFICIENCY.map((level) => (
                      <option key={level} value={level}>{level}</option>
                    ))}
                  </select>
                  <input type="number" min={0} aria-label="Years" className="border rounded px-2 py-1 w-24" value={skillYears} onChange={(e) => setSkillYears(e.target.value)} />
                  <button type="submit" disabled={!skillName.trim()} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50">Add skill</button>
                </form>
              </div>
            )}

            {activeTab === 'experience' && (
              <div className="space-y-4">
                {experiences === null ? (
                  <p className="text-gray-500">Loading experience…</p>
                ) : experiences.length === 0 ? (
                  <p className="text-gray-500">No experience added yet.</p>
                ) : (
                  <ul className="space-y-2">
                    {experiences.map((item) => (
                      <li key={item.id} className="flex justify-between items-start border rounded p-3">
                        <span>
                          <span className="font-medium">{item.title}</span> at {item.company}
                          <span className="block text-sm text-gray-600">
                            {new Date(item.start_date).toLocaleDateString()} – {item.current ? 'Present' : item.end_date ? new Date(item.end_date).toLocaleDateString() : '—'}
                          </span>
                        </span>
                        <button type="button" onClick={() => removeItem(`/profiles/experiences/${item.id}`, reloadSections)} className="text-sm text-red-600 hover:underline">
                          Remove
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
                <form onSubmit={addExperience} className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <input className="border rounded px-2 py-1" placeholder="Title" value={expForm.title} onChange={(e) => setExpForm({ ...expForm, title: e.target.value })} required />
                  <input className="border rounded px-2 py-1" placeholder="Company" value={expForm.company} onChange={(e) => setExpForm({ ...expForm, company: e.target.value })} required />
                  <label className="text-sm">
                    <span className="block text-xs text-gray-600">Start date</span>
                    <input type="date" className="border rounded px-2 py-1 w-full" value={expForm.start} onChange={(e) => setExpForm({ ...expForm, start: e.target.value })} required />
                  </label>
                  <label className="text-sm">
                    <span className="block text-xs text-gray-600">End date</span>
                    <input type="date" className="border rounded px-2 py-1 w-full" value={expForm.end} disabled={expForm.current} onChange={(e) => setExpForm({ ...expForm, end: e.target.value })} />
                  </label>
                  <label className="flex items-center gap-2 text-sm">
                    <input type="checkbox" checked={expForm.current} onChange={(e) => setExpForm({ ...expForm, current: e.target.checked })} />
                    I currently work here
                  </label>
                  <input className="border rounded px-2 py-1" placeholder="Description" value={expForm.description} onChange={(e) => setExpForm({ ...expForm, description: e.target.value })} />
                  <button type="submit" disabled={!expForm.title.trim() || !expForm.company.trim() || !expForm.start} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50 md:col-span-2">
                    Add experience
                  </button>
                </form>
              </div>
            )}

            {activeTab === 'education' && (
              <div className="space-y-4">
                {educations === null ? (
                  <p className="text-gray-500">Loading education…</p>
                ) : educations.length === 0 ? (
                  <p className="text-gray-500">No education added yet.</p>
                ) : (
                  <ul className="space-y-2">
                    {educations.map((item) => (
                      <li key={item.id} className="flex justify-between items-start border rounded p-3">
                        <span>
                          <span className="font-medium">{item.school}</span>
                          {item.degree ? ` · ${item.degree}` : ''}{item.field ? ` in ${item.field}` : ''}
                          <span className="block text-sm text-gray-600">
                            {new Date(item.start_date).toLocaleDateString()} – {item.end_date ? new Date(item.end_date).toLocaleDateString() : 'Present'}
                          </span>
                        </span>
                        <button type="button" onClick={() => removeItem(`/profiles/educations/${item.id}`, reloadSections)} className="text-sm text-red-600 hover:underline">
                          Remove
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
                <form onSubmit={addEducation} className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <input className="border rounded px-2 py-1" placeholder="School" value={eduForm.school} onChange={(e) => setEduForm({ ...eduForm, school: e.target.value })} required />
                  <input className="border rounded px-2 py-1" placeholder="Degree" value={eduForm.degree} onChange={(e) => setEduForm({ ...eduForm, degree: e.target.value })} />
                  <input className="border rounded px-2 py-1" placeholder="Field of study" value={eduForm.field} onChange={(e) => setEduForm({ ...eduForm, field: e.target.value })} />
                  <label className="text-sm">
                    <span className="block text-xs text-gray-600">Start date</span>
                    <input type="date" className="border rounded px-2 py-1 w-full" value={eduForm.start} onChange={(e) => setEduForm({ ...eduForm, start: e.target.value })} required />
                  </label>
                  <label className="text-sm">
                    <span className="block text-xs text-gray-600">End date</span>
                    <input type="date" className="border rounded px-2 py-1 w-full" value={eduForm.end} onChange={(e) => setEduForm({ ...eduForm, end: e.target.value })} />
                  </label>
                  <button type="submit" disabled={!eduForm.school.trim() || !eduForm.start} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50 md:col-span-2">
                    Add education
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
