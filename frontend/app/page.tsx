import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">AetherCMS AI</h1>
        <p className="text-xl text-gray-600 mb-8">
          Enterprise AI Publishing Platform
        </p>
        <p className="text-gray-500 mb-6">
          Module 1: System Architecture - Foundation Complete
        </p>
        <Link
          href="/news"
          className="inline-block rounded-lg bg-blue-600 px-5 py-2.5 font-medium text-white hover:bg-blue-700"
        >
          Read the latest news →
        </Link>
      </div>
    </main>
  );
}
