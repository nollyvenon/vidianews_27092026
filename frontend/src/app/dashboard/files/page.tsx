'use client'

import { useState, useRef } from 'react'
import { ApiClient } from '@/lib/api-client'

export default function FilesPage() {
  const [files, setFiles] = useState<any[]>([])
  const [uploading, setUploading] = useState(false)
  const fileInput = useRef<HTMLInputElement>(null)

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files
    if (!selectedFiles) return

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', selectedFiles[0])

      // Upload file
      const response = await fetch('/api/v1/resources/files/upload', {
        method: 'POST',
        body: formData,
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      })

      if (response.ok) {
        const file = await response.json()
        setFiles([...files, file])
      }
    } catch (err) {
      console.error('Upload failed', err)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Files</h1>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <input
          ref={fileInput}
          type="file"
          onChange={handleFileSelect}
          className="hidden"
        />
        <button
          onClick={() => fileInput.current?.click()}
          disabled={uploading}
          className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {uploading ? 'Uploading...' : 'Upload File'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {files.map((file) => (
          <div key={file.id} className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold truncate">{file.filename}</h3>
            <p className="text-sm text-gray-600">{(file.file_size / 1024 / 1024).toFixed(2)} MB</p>
            <a href={file.url} target="_blank" rel="noopener" className="text-blue-600 hover:underline text-sm">
              Download
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}
