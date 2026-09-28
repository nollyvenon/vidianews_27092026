'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

interface Lesson {
  id: number;
  title: string;
  video_url: string;
  video_duration: number;
  is_completed: boolean;
}

interface Section {
  id: number;
  title: string;
  lessons: Lesson[];
}

interface Review {
  id: number;
  user_id: number;
  rating: number;
  title: string;
  content: string;
}

interface Course {
  id: number;
  title: string;
  description: string;
  instructor_id: number;
  price: number;
  average_rating: number;
  total_reviews: number;
  difficulty_level: string;
  duration_hours: number;
  learning_objectives: string[];
}

interface Enrollment {
  id: number;
  course_id: number;
  status: string;
  progress_percentage: number;
  lessons_completed: number;
  certificate_issued: boolean;
}

export default function CourseDetailPage() {
  const params = useParams();
  const courseId = params.id as string;

  const [course, setCourse] = useState<Course | null>(null);
  const [sections, setSections] = useState<Section[]>([]);
  const [enrollment, setEnrollment] = useState<Enrollment | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedSection, setExpandedSection] = useState<number | null>(null);
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState('');

  useEffect(() => {
    Promise.all([
      fetch(`/api/v1/courses/${courseId}`).then(r => r.json()),
      fetch(`/api/v1/courses/${courseId}/sections`).then(r => r.json()),
      fetch(`/api/v1/courses/${courseId}/reviews`).then(r => r.json()),
    ]).then(([courseData, sectionsData, reviewsData]) => {
      setCourse(courseData);
      setSections(sectionsData);
      setReviews(reviewsData);
      setLoading(false);
    });
  }, [courseId]);

  const handleEnroll = async () => {
    try {
      const response = await fetch(`/api/v1/courses/${courseId}/enroll`, {
        method: 'POST'
      });
      const enrollmentData = await response.json();
      setEnrollment(enrollmentData);
    } catch (error) {
      console.error('Enrollment failed:', error);
    }
  };

  const handleLessonComplete = async (lessonId: number) => {
    if (!enrollment) return;
    try {
      await fetch(`/api/v1/enrollments/${enrollment.id}/lessons/${lessonId}/complete`, {
        method: 'POST'
      });
      // Refresh enrollment progress
      const response = await fetch(`/api/v1/enrollments/${enrollment.id}`);
      const updatedEnrollment = await response.json();
      setEnrollment(updatedEnrollment);
    } catch (error) {
      console.error('Lesson completion failed:', error);
    }
  };

  const handleSubmitReview = async () => {
    try {
      await fetch(`/api/v1/courses/${courseId}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rating,
          content: reviewText
        })
      });
      setRating(5);
      setReviewText('');
      // Refresh reviews
      const response = await fetch(`/api/v1/courses/${courseId}/reviews`);
      const reviewsData = await response.json();
      setReviews(reviewsData);
    } catch (error) {
      console.error('Review submission failed:', error);
    }
  };

  if (loading) return <div>Loading course...</div>;
  if (!course) return <div>Course not found</div>;

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-4xl font-bold mb-2">{course.title}</h1>
        <p className="text-gray-600 mb-4">{course.description}</p>

        <div className="flex gap-4 mb-4">
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded">
            {course.difficulty_level}
          </span>
          <span className="text-yellow-500">★ {course.average_rating.toFixed(1)} ({course.total_reviews} reviews)</span>
          <span className="text-gray-600">{course.duration_hours}h total duration</span>
        </div>

        {!enrollment ? (
          <Button onClick={handleEnroll} size="lg">
            Enroll Now - ${course.price.toFixed(2)}
          </Button>
        ) : (
          <Card className="p-4 bg-green-50">
            <p className="font-semibold mb-2">Enrollment Status: {enrollment.status}</p>
            <div className="mb-2">
              <p className="text-sm text-gray-600 mb-1">Progress</p>
              <Progress value={enrollment.progress_percentage} className="h-2" />
            </div>
            <p className="text-sm text-gray-600">{enrollment.lessons_completed} lessons completed</p>
            {enrollment.certificate_issued && (
              <p className="text-green-600 font-semibold mt-2">✓ Certificate Earned</p>
            )}
          </Card>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <h2 className="text-2xl font-bold mb-4">Course Content</h2>
          {sections.map(section => (
            <Card key={section.id} className="mb-4">
              <button
                onClick={() => setExpandedSection(expandedSection === section.id ? null : section.id)}
                className="w-full p-4 text-left hover:bg-gray-50 flex justify-between items-center"
              >
                <h3 className="font-bold">{section.title}</h3>
                <span>{expandedSection === section.id ? '▼' : '▶'}</span>
              </button>

              {expandedSection === section.id && (
                <div className="border-t p-4">
                  {section.lessons && section.lessons.map(lesson => (
                    <div key={lesson.id} className="mb-3 p-3 bg-gray-50 rounded">
                      <p className="font-semibold mb-1">{lesson.title}</p>
                      <p className="text-sm text-gray-600 mb-2">{lesson.video_duration} minutes</p>
                      {enrollment && (
                        <Button
                          onClick={() => handleLessonComplete(lesson.id)}
                          size="sm"
                          variant={lesson.is_completed ? 'default' : 'outline'}
                        >
                          {lesson.is_completed ? '✓ Completed' : 'Mark Complete'}
                        </Button>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </Card>
          ))}
        </div>

        <div>
          <h2 className="text-2xl font-bold mb-4">Reviews</h2>

          {enrollment && (
            <Card className="p-4 mb-4">
              <h3 className="font-bold mb-3">Leave a Review</h3>
              <div className="mb-3">
                <label className="block text-sm font-medium mb-1">Rating</label>
                <select
                  value={rating}
                  onChange={(e) => setRating(parseInt(e.target.value))}
                  className="w-full border rounded px-2 py-1"
                >
                  {[1, 2, 3, 4, 5].map(r => (
                    <option key={r} value={r}>{r} Stars</option>
                  ))}
                </select>
              </div>
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder="Share your experience..."
                className="w-full border rounded p-2 mb-2"
                rows={3}
              />
              <Button onClick={handleSubmitReview} className="w-full">Submit Review</Button>
            </Card>
          )}

          {reviews.length > 0 && (
            <div>
              <h3 className="font-bold mb-3">Student Reviews</h3>
              {reviews.map(review => (
                <Card key={review.id} className="p-3 mb-2">
                  <div className="flex justify-between items-start mb-1">
                    <span className="text-yellow-500">★ {review.rating}</span>
                  </div>
                  <p className="text-sm font-medium">{review.title}</p>
                  <p className="text-sm text-gray-600">{review.content}</p>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
