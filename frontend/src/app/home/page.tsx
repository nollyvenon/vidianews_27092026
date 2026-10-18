import Link from 'next/link'

/** Public introduction to the platform, with the entry points to sign in or create an account. */
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="text-center max-w-xl">
        <h1 className="text-4xl font-bold mb-4">AetherCMS AI</h1>
        <p className="text-xl text-gray-600 mb-8">
          Enterprise AI Publishing Platform
        </p>
        <p className="text-gray-500 mb-8">
          Write, publish and distribute content with AI assistance, and measure how it performs.
        </p>
        <div className="flex gap-3 justify-center">
          <Link href="/auth/login" className="px-4 py-2 border border-blue-600 text-blue-600 rounded-md hover:bg-blue-50">
            Sign in
          </Link>
          <Link href="/auth/signup" className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Create account
          </Link>
        </div>
      </div>
    </main>
  )
}
