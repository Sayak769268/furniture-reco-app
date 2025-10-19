import { useState, useEffect, useRef } from 'react'
import { API_ENDPOINTS } from './config'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I\'m your furniture assistant. Tell me what you\'re looking for! 🪑' }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [products, setProducts] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [currentPage, setCurrentPage] = useState('chat')
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, products])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading) return

    const userMessage = inputMessage.trim()
    setInputMessage('')
    setIsLoading(true)
    setError(null)

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])

    try {
      const response = await fetch(API_ENDPOINTS.CHAT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: userMessage,
          history: messages.slice(1).map(m => ({ role: m.role, content: m.content }))
        })
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()
      
      if (data.error) throw new Error(data.error)

      // Add assistant response
      setMessages(prev => [...prev, { role: 'assistant', content: data.message }])
      setProducts(data.recommendations || [])
    } catch (error) {
      console.error('Chat error:', error)
      setError(error.message)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `Sorry, I couldn't connect to the server. Make sure your backend is running on ${API_ENDPOINTS.CHAT}` 
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const loadAnalytics = async () => {
    try {
      setError(null)
      console.log('Fetching analytics from:', API_ENDPOINTS.ANALYTICS)
      
      const response = await fetch(API_ENDPOINTS.ANALYTICS)
      
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('Analytics data received:', data)
      console.log('Available keys:', Object.keys(data))
      console.log('top_brands:', data.top_brands)
      console.log('top_categories:', data.top_categories)
      setAnalytics(data)
    } catch (error) {
      console.error('Analytics error:', error)
      setError(`Could not load analytics. Make sure your backend is running on ${API_ENDPOINTS.ANALYTICS}`)
    }
  }

  const clearChat = () => {
    setMessages([{ role: 'assistant', content: 'Hi! I\'m your furniture assistant. Tell me what you\'re looking for! 🪑' }])
    setProducts([])
    setError(null)
    setIsLoading(false) // Stop any ongoing loading
  }

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-brand">
          <h1>🪑 Furniture AI</h1>
          <span className="nav-subtitle">Smart Furniture Recommendations</span>
      </div>
        <div className="nav-buttons">
          <button 
            className={currentPage === 'chat' ? 'active' : ''} 
            onClick={() => setCurrentPage('chat')}
          >
            💬 Chat
          </button>
          <button 
            className={currentPage === 'analytics' ? 'active' : ''} 
            onClick={() => {
              setCurrentPage('analytics')
              if (!analytics) loadAnalytics()
            }}
          >
            📊 Analytics
        </button>
        </div>
      </nav>

      <main className="main">
        {currentPage === 'chat' ? (
          <div className="chat-container">
            <div className="chat-header">
              <h2>Furniture Assistant</h2>
              <button onClick={clearChat} className="clear-btn">🗑️ Clear Chat</button>
            </div>
            
            <div className="chat-messages">
              {messages.map((msg, i) => (
                <div key={i} className={`message ${msg.role}`}>
                  <div className="message-avatar">
                    {msg.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    {msg.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message assistant">
                  <div className="message-avatar">🤖</div>
                  <div className="message-content">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {error && (
              <div className="error-banner">
                ⚠️ {error}
              </div>
            )}

            {products.length > 0 && (
              <div className="products-section">
                <h3>🎯 Recommended Products ({products.length})</h3>
                <div className="products-grid">
                   {products.map((product, i) => {
                     const firstImage = Array.isArray(product.images) && product.images.length > 0 
                       ? product.images[0] 
                       : null;
                     const matchScore = product.score ? Math.round(product.score * 100) : 0;
                     const getMatchColor = (score) => {
                       if (score >= 70) return '#10b981'; // Green
                       if (score >= 40) return '#f59e0b'; // Yellow
                       return '#ef4444'; // Red
                     };
                     const getMatchLabel = (score) => {
                       if (score >= 70) return 'High Match';
                       if (score >= 40) return 'Medium Match';
                       return 'Low Match';
                     };
                     
                     return (
                       <div key={i} className="product-card">
                         <div className="product-image-container">
                           {firstImage ? (
                             <img 
                               src={firstImage} 
                               alt={product.title || 'Product'}
                               onError={(e) => {
                                 e.target.src = 'https://via.placeholder.com/300x200?text=No+Image'
                               }}
                             />
                           ) : (
                             <div className="no-image-placeholder">
                               <span>📷</span>
                               <p>No Image</p>
                             </div>
                           )}
                           {product.score && (
                             <div 
                               className="product-score" 
                               style={{ 
                                 backgroundColor: getMatchColor(matchScore),
                                 color: 'white'
                               }}
                               title={`${getMatchLabel(matchScore)}: Based on category, price, and brand relevance`}
                             >
                               {matchScore}% match
                             </div>
                           )}
                         </div>
                         <div className="product-info">
                           <h4 className="product-title">{product.title || 'Untitled Product'}</h4>
                           <div className="product-meta">
                             <p className="product-brand">🏷️ {product.brand || 'Unknown Brand'}</p>
                             <p className="product-price">
                               💰 {product.price ? `$${product.price}` : 'N/A'}
                             </p>
                           </div>
                           <div className="product-details">
                             {product.categories && (
                               <span className="product-tag">📂 {product.categories}</span>
                             )}
                             {product.material && (
                               <span className="product-tag">🪵 {product.material}</span>
                             )}
                           </div>
                           <p className="product-description">
                             {product.generated_description || product.description || 'No description available'}
                           </p>
                         </div>
                       </div>
                     );
                   })}
                </div>
              </div>
            )}

            <form onSubmit={sendMessage} className="chat-input">
              <div className="input-container">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Describe what furniture you're looking for... (e.g., 'modern sofa under $500')"
                  disabled={isLoading}
                  className="message-input"
                />
                <button 
                  type="submit" 
                  disabled={isLoading || !inputMessage.trim()}
                  className="send-button"
                >
                  {isLoading ? '⏳' : '🚀'}
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="analytics">
            <div className="analytics-header">
              <h2>📊 Dataset Analytics</h2>
              <p>Insights from our furniture recommendation database</p>
            </div>
            
            {error && (
              <div className="error-banner">
                ⚠️ {error}
              </div>
            )}
            
            <div style={{width: "100%", padding: "2rem", background: "white", borderRadius: "10px", margin: "0"}}>
              <h2 style={{color: "#333", fontSize: "2rem", marginBottom: "1rem"}}>Analytics Dashboard</h2>
              {analytics ? (
                <div>
                  <p style={{color: "#333", fontSize: "1.2rem", marginBottom: "0.5rem"}}>Total Products: {analytics.summary.total_products}</p>
                  <p style={{color: "#333", fontSize: "1.2rem"}}>With Price: {analytics.summary.with_price}</p>
                </div>
              ) : (
                <p style={{color: "#333", fontSize: "1.2rem"}}>Loading...</p>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
