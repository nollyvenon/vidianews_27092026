'use client'

export default function AIPage() {
  const aiFeatures = [
    {
      title: 'AI Chat',
      description: 'Multi-turn AI conversations with context memory',
      icon: '💬',
      href: '/dashboard/ai/chat'
    },
    {
      title: 'Prompt Library',
      description: 'Reusable prompts and templates for common tasks',
      icon: '📝',
      href: '/dashboard/ai/prompts'
    },
    {
      title: 'AI Workflows',
      description: 'Automate tasks with AI workflow builders',
      icon: '⚙️',
      href: '/dashboard/ai/workflows'
    },
    {
      title: 'AI Agents',
      description: 'Autonomous agents for complex operations',
      icon: '🤖',
      href: '/dashboard/ai/agents'
    },
    {
      title: 'Document Research',
      description: 'Semantic search across your documents',
      icon: '🔍',
      href: '/dashboard/ai/research'
    },
    {
      title: 'AI Monitoring',
      description: 'Track usage, costs, and performance metrics',
      icon: '📊',
      href: '/dashboard/ai/monitoring'
    },
  ]

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">AI Features</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {aiFeatures.map((feature, i) => (
          <a
            key={i}
            href={feature.href}
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition cursor-pointer"
          >
            <div className="text-4xl mb-2">{feature.icon}</div>
            <h3 className="text-lg font-semibold">{feature.title}</h3>
            <p className="text-gray-600 text-sm">{feature.description}</p>
          </a>
        ))}
      </div>
    </div>
  )
}
