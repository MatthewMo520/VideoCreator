import { useState, useEffect } from 'react'
import { Upload, Play, Download, Sparkles, Video, Music, Image as ImageIcon } from 'lucide-react'

const API_BASE = 'http://localhost:8001'

const styles = [
  { id: 'trendy', name: '🔥 Trendy', description: 'Popular social media style', color: 'from-pink-500 to-violet-500' },
  { id: 'business', name: '💼 Business', description: 'Professional and clean', color: 'from-blue-500 to-cyan-500' },
  { id: 'lifestyle', name: '✨ Lifestyle', description: 'Casual and personal', color: 'from-green-500 to-teal-500' },
  { id: 'tech', name: '🚀 Tech', description: 'Modern and sleek', color: 'from-purple-500 to-indigo-500' },
  { id: 'finance', name: '📈 Finance', description: 'Stock market focused', color: 'from-yellow-500 to-orange-500' },
  { id: 'fitness', name: '💪 Fitness', description: 'Health and wellness', color: 'from-red-500 to-pink-500' },
]

function App() {
  const [formData, setFormData] = useState({
    prompt: '',
    style: 'trendy',
    duration: 15,
    includeTrending: true
  })
  const [files, setFiles] = useState({
    images: [],
    audio: null
  })
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedVideo, setGeneratedVideo] = useState(null)
  const [error, setError] = useState('')
  const [trends, setTrends] = useState(null)

  useEffect(() => {
    loadTrends()
  }, [])

  const loadTrends = async () => {
    try {
      const response = await fetch(`${API_BASE}/trends`)
      const data = await response.json()
      setTrends(data)
    } catch (err) {
      console.error('Failed to load trends:', err)
    }
  }

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleFileChange = (e, type) => {
    const selectedFiles = Array.from(e.target.files)
    setFiles(prev => ({
      ...prev,
      [type]: type === 'images' ? selectedFiles : selectedFiles[0]
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsGenerating(true)
    setError('')
    setGeneratedVideo(null)

    try {
      const submitData = new FormData()
      submitData.append('prompt', formData.prompt)
      submitData.append('style', formData.style)
      submitData.append('duration', formData.duration.toString())
      submitData.append('include_trending', formData.includeTrending.toString())

      // Add images
      files.images.forEach(image => {
        submitData.append('images', image)
      })

      // Add audio
      if (files.audio) {
        submitData.append('audio', files.audio)
      }

      const response = await fetch(`${API_BASE}/generate-reel`, {
        method: 'POST',
        body: submitData
      })

      const result = await response.json()

      if (result.success) {
        setGeneratedVideo(result)
      } else {
        throw new Error(result.message || 'Failed to generate reel')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setIsGenerating(false)
    }
  }

  const selectedStyle = styles.find(s => s.id === formData.style)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent mb-4">
            🎬 AI Reel Generator
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Create viral reels instantly with AI-powered content generation
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Form Section */}
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <Sparkles className="text-yellow-400" />
              Create Your Reel
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Prompt */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Content Prompt *
                </label>
                <textarea
                  name="prompt"
                  value={formData.prompt}
                  onChange={handleInputChange}
                  placeholder="Describe what you want your reel to be about... (e.g., 'My top 3 stock picks that gained 500% this year')"
                  required
                  rows={4}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent resize-none"
                />
              </div>

              {/* Style Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Style
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {styles.map(style => (
                    <label
                      key={style.id}
                      className={`relative flex items-center p-3 rounded-xl cursor-pointer transition-all ${
                        formData.style === style.id
                          ? `bg-gradient-to-r ${style.color} text-white shadow-lg`
                          : 'bg-white/5 text-gray-300 hover:bg-white/10'
                      }`}
                    >
                      <input
                        type="radio"
                        name="style"
                        value={style.id}
                        checked={formData.style === style.id}
                        onChange={handleInputChange}
                        className="sr-only"
                      />
                      <div className="text-center w-full">
                        <div className="font-medium">{style.name}</div>
                        <div className="text-xs opacity-80">{style.description}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Duration */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Duration: {formData.duration} seconds
                </label>
                <input
                  type="range"
                  name="duration"
                  min="5"
                  max="60"
                  value={formData.duration}
                  onChange={handleInputChange}
                  className="w-full accent-purple-400"
                />
                <div className="flex justify-between text-xs text-gray-400 mt-1">
                  <span>5s</span>
                  <span>60s</span>
                </div>
              </div>

              {/* File Uploads */}
              <div className="grid grid-cols-2 gap-4">
                {/* Images */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Images (optional)
                  </label>
                  <label className="flex flex-col items-center justify-center w-full h-24 border-2 border-dashed border-white/20 rounded-xl cursor-pointer hover:bg-white/5 transition-colors">
                    <ImageIcon className="w-6 h-6 text-gray-400 mb-1" />
                    <span className="text-sm text-gray-400">
                      {files.images.length > 0 ? `${files.images.length} files` : 'Upload Images'}
                    </span>
                    <input
                      type="file"
                      multiple
                      accept="image/*"
                      onChange={(e) => handleFileChange(e, 'images')}
                      className="hidden"
                    />
                  </label>
                </div>

                {/* Audio */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Audio (optional)
                  </label>
                  <label className="flex flex-col items-center justify-center w-full h-24 border-2 border-dashed border-white/20 rounded-xl cursor-pointer hover:bg-white/5 transition-colors">
                    <Music className="w-6 h-6 text-gray-400 mb-1" />
                    <span className="text-sm text-gray-400">
                      {files.audio ? files.audio.name.slice(0, 15) + '...' : 'Upload Audio'}
                    </span>
                    <input
                      type="file"
                      accept="audio/*"
                      onChange={(e) => handleFileChange(e, 'audio')}
                      className="hidden"
                    />
                  </label>
                </div>
              </div>

              {/* Trending */}
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  name="includeTrending"
                  checked={formData.includeTrending}
                  onChange={handleInputChange}
                  className="w-4 h-4 accent-purple-400"
                />
                <label className="text-gray-300">Include trending elements</label>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isGenerating || !formData.prompt}
                className={`w-full py-4 rounded-xl font-semibold text-lg transition-all ${
                  isGenerating || !formData.prompt
                    ? 'bg-gray-600 cursor-not-allowed'
                    : `bg-gradient-to-r ${selectedStyle.color} hover:shadow-lg hover:scale-105`
                } text-white`}
              >
                {isGenerating ? (
                  <div className="flex items-center justify-center gap-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Generating...
                  </div>
                ) : (
                  <div className="flex items-center justify-center gap-2">
                    <Video className="w-5 h-5" />
                    Generate Reel
                  </div>
                )}
              </button>
            </form>
          </div>

          {/* Preview Section */}
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <Play className="text-green-400" />
              Preview
            </h2>

            {/* Error */}
            {error && (
              <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 mb-6">
                <p className="text-red-200">{error}</p>
              </div>
            )}

            {/* Preview Area */}
            <div className="bg-black/30 rounded-2xl p-8 min-h-[300px] flex items-center justify-center">
              {isGenerating ? (
                <div className="text-center">
                  <div className="w-16 h-16 border-4 border-white/30 border-t-white rounded-full animate-spin mx-auto mb-4" />
                  <p className="text-white text-lg font-medium">Creating your viral reel...</p>
                  <p className="text-gray-400 mt-2">This may take 3-5 minutes for complex animations</p>
                </div>
              ) : generatedVideo ? (
                <div className="w-full text-center">
                  <video
                    controls
                    autoPlay
                    muted
                    className="w-full max-w-md mx-auto rounded-xl shadow-2xl mb-4"
                  >
                    <source src={`${API_BASE}${generatedVideo.download_url}`} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                  <a
                    href={`${API_BASE}${generatedVideo.download_url}`}
                    download
                    className="inline-flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-xl font-semibold transition-colors"
                  >
                    <Download className="w-5 h-5" />
                    Download Reel
                  </a>
                </div>
              ) : (
                <div className="text-center text-gray-400">
                  <Video className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p className="text-lg">Your generated reel will appear here</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Trending Section */}
        {trends && (
          <div className="max-w-7xl mx-auto mt-8">
            <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20">
              <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                🔥 Currently Trending
              </h3>
              <div className="grid md:grid-cols-2 gap-6">
                {trends.hashtags && trends.hashtags.length > 0 && (
                  <div>
                    <h4 className="text-yellow-400 font-medium mb-2">Trending Hashtags:</h4>
                    <div className="flex flex-wrap gap-2">
                      {trends.hashtags.slice(0, 8).map((tag, index) => (
                        <span
                          key={index}
                          className="bg-white/10 text-gray-300 px-3 py-1 rounded-full text-sm"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {trends.topics && trends.topics.length > 0 && (
                  <div>
                    <h4 className="text-yellow-400 font-medium mb-2">Hot Topics:</h4>
                    <div className="flex flex-wrap gap-2">
                      {trends.topics.slice(0, 6).map((topic, index) => (
                        <span
                          key={index}
                          className="bg-white/10 text-gray-300 px-3 py-1 rounded-full text-sm"
                        >
                          {topic.replace(/_/g, ' ')}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
