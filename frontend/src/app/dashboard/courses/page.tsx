'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

interface Course {
  id: number;
  title: string;
  description: string;
  instructor_id: number;
  price: number;
  status: string;
  average_rating: number;
  total_enrollments: number;
  thumbnail_url: string;
  difficulty_level: string;
}

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [filteredCourses, setFilteredCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('all');

  useEffect(() => {
    fetch('/api/v1/courses')
      .then(r => r.json())
      .then(data => {
        setCourses(data);
        setFilteredCourses(data);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    let filtered = courses;

    if (searchTerm) {
      filtered = filtered.filter(c =>
        c.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (category !== 'all') {
      filtered = filtered.filter(c => c.difficulty_level === category);
    }

    setFilteredCourses(filtered);
  }, [searchTerm, category, courses]);

  if (loading) return <div>Loading courses...</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Courses</h1>

      <div className="flex gap-4 mb-6">
        <Input
          placeholder="Search courses..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1"
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="border rounded px-3 py-2"
        >
          <option value="all">All Levels</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        <Link href="/dashboard/courses/create">
          <Button>Create Course</Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCourses.map(course => (
          <Card key={course.id} className="overflow-hidden hover:shadow-lg transition">
            {course.thumbnail_url && (
              <img
                src={course.thumbnail_url}
                alt={course.title}
                className="w-full h-40 object-cover"
              />
            )}
            <div className="p-4">
              <h3 className="text-lg font-bold mb-2">{course.title}</h3>
              <p className="text-sm text-gray-600 mb-2">{course.description}</p>
              <div className="flex justify-between items-center mb-3 text-sm">
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {course.difficulty_level}
                </span>
                <span className="text-yellow-500">★ {course.average_rating.toFixed(1)}</span>
              </div>
              <p className="text-sm text-gray-500 mb-3">{course.total_enrollments} students</p>
              <p className="text-lg font-bold mb-3">${course.price.toFixed(2)}</p>
              <Link href={`/dashboard/courses/${course.id}`}>
                <Button className="w-full">View Course</Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
