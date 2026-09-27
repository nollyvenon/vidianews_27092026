'use client'

import { useState, useEffect, useRef } from 'react'
import { ApiClient } from '@/lib/api-client'

interface ChatSession {
  id: number
  title: string
  created_at: string
}

interface Message {
  id: number
  role: string
  content: string
  tokens: number
  created_at: string
}

export default function ChatPage() {
  const [chats, setChats] = useState<ChatSession[]>([])
  const [selectedChat, setSelectedChat] = useState<ChatSession | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEnd = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetchChats()
  }, [])

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchChats = async () => {
    try {
      const data = await ApiClient.get('/ai/chats')
      setChats(data)
      if (data.length > 0) {
        selectChat(data[0])
      }
    } catch (err) {
      console.error('Failed to fetch chats', err)
    }
  }

  const selectChat = async (chat: ChatSession) => {
    setSelectedChat(chat)
    try {
      const data = await ApiClient.get(`/ai/chats/${chat.id}`)
      setMessages(data.messages || [])
    } catch (err) {
      console.error('Failed to load chat', err)
    }
  }

  const createNewChat = async () => {
    try {
      const chat = await ApiClient.post('/ai/chats', { title: 'New Chat' })
      setChats([...chats, chat])
      setSelectedChat(chat)
      setMessages([])
    } catch (err) {
      console.error('Failed to create chat', err)
    }
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !selectedChat) return

    const userMessage = { role: 'user', content: input }
    setInput('')
    setLoading(true)

    try {
      const message = await ApiClient.post(`/ai/chats/${selectedChat.id}/messages`, {
        role: 'user',
        content: input,
        tokens: Math.ceil(input.length / 4),
      })
      setMessages([...messages, message])

      // TODO: Get AI response from streaming endpoint
      // For now, just simulate a response
      setTimeout(() => {
        setMessages((prev) => [...prev, {
          id: Date.now(),
          role: 'assistant',
          content: 'Thanks for your message!',
          tokens: 5,
          created_at: new Date().toISOString(),
        }])
      }, 500)
    } catch (err) {
      console.error('Failed to send message', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col">
      <div className="flex-1 flex gap-6 p-6">
        <div className="w-64 bg-white rounded-lg shadow p-4">
          <button
            onClick={createNewChat}
            className="w-full mb-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            + New Chat
          </button>
          <div className="space-y-2">
            {chats.map((chat) => (
              <button
                key={chat.id}
                onClick={() => selectChat(chat)}
                className={`w-full text-left px-4 py-2 rounded-md ${
                  selectedChat?.id === chat.id
                    ? 'bg-blue-100 text-blue-900'
                    : 'hover:bg-gray-100'
                }`}
              >
                <div className="font-medium truncate">{chat.title}</div>
                <div className="text-xs text-gray-500">
                  {new Date(chat.created_at).toLocaleDateString()}
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="flex-1 flex flex-col bg-white rounded-lg shadow">
          {selectedChat ? (
            <>
              <div className="flex-1 p-4 overflow-y-auto space-y-4">
                {messages.length === 0 && (
                  <div className="flex items-center justify-center h-full text-gray-600">
                    Start a conversation...
                  </div>
                )}
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs px-4 py-2 rounded-lg ${
                        msg.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-900'
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}
                <div ref={messagesEnd} />
              </div>

              <form onSubmit={handleSendMessage} className="p-4 border-t flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask anything..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  Send
                </button>
              </form>
            </>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-600">
              Create a new chat to get started
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
