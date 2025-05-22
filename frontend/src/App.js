import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://localhost:8000/posts/');
        if (!response.ok) {
          throw new Error('Failed to fetch posts');
        }
        const postsData = await response.json();
        setPosts(postsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (loading) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>Instagram Clone</h1>
        </header>
        <div className="loading">Loading posts...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>Instagram Clone</h1>
        </header>
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Instagram Clone</h1>
      </header>
      <main className="feed">
        {posts.length === 0 ? (
          <div className="no-posts">No posts available</div>
        ) : (
          posts.map((post) => (
            <div key={post.id} className="post-card">
              <div className="post-image">
                <img src={post.image_url} alt="Post" />
              </div>
              <div className="post-content">
                <p className="post-caption">{post.caption}</p>
                <div className="post-meta">
                  <span className="post-date">
                    {new Date(post.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </main>
    </div>
  );
}

export default App;
