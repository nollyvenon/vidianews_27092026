'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

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
  const [error, setError] = useState<string | null>(null)
  const messagesEnd = useRef<HTMLDivElement>(null)

  const selectChat = useCallback(async (chat: ChatSession) => {
    setSelectedChat(chat)
    try {
      const data = await ApiClient.get(`/ai/chats/${chat.id}`)
      setMessages(data.messages || [])
    } catch (err) {
      console.error('Failed to load chat', err)
    }
  }, []);

  const fetchChats = useCallback(async () => {
    try {
      const data = await ApiClient.get('/ai/chats')
      setChats(data)
      if (data.length > 0) {
        selectChat(data[0])
      }
    } catch (err) {
      console.error('Failed to fetch chats', err)
    }
  }, [selectChat]);

  useEffect(() => {
    fetchChats()
  }, [fetchChats])

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])



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

    const text = input
    setInput('')
    setLoading(true)

    let stored = false
    try {
      const message = await ApiClient.post(`/ai/chats/${selectedChat.id}/messages`, {
        role: 'user',
        content: text,
        tokens: Math.ceil(text.length / 4),
      })
      setMessages((prev) => [...prev, message])
      stored = true

      // The assistant's answer comes from the model provider and is stored by the server.
      const reply = await ApiClient.post(`/ai/chats/${selectedChat.id}/reply`, {})
      setMessages((prev) => [...prev, reply])
      setError(null)
    } catch (err) {
      // Give the text back only when it was not stored, so a retry never sends it twice.
      console.error('Failed to send message', err)
      if (!stored) setInput(text)
      setError(errorMessage(err, 'The assistant could not reply.'))
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

              {error && (
                <p role="alert" className="px-4 pt-3 text-sm text-red-700">{error}</p>
              )}
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
