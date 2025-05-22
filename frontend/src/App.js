import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [creating, setCreating] = useState(false);

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
    }
  };

  useEffect(() => {
    const loadPosts = async () => {
      await fetchPosts();
      setLoading(false);
    };

    loadPosts();
  }, []);

  const createSamplePosts = async () => {
    setCreating(true);
    setError(null);
    
    try {
      // First create a user if one doesn't exist
      let userId = 1;
      try {
        const userResponse = await fetch('http://localhost:8000/users/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: 'demo_user',
            email: 'demo@example.com',
            password: 'password123'
          }),
        });
        
        if (userResponse.ok) {
          const userData = await userResponse.json();
          userId = userData.id;
        }
      } catch (err) {
        // User might already exist, continue with userId = 1
      }

      // Sample posts data
      const samplePosts = [
        {
          image_url: 'https://picsum.photos/600/600?random=1',
          caption: 'Beautiful sunset over the mountains! 🌅 #nature #sunset'
        },
        {
          image_url: 'https://picsum.photos/600/600?random=2', 
          caption: 'Morning coffee and good vibes ☕️ #coffee #morning'
        },
        {
          image_url: 'https://picsum.photos/600/600?random=3',
          caption: 'Weekend adventures in the city 🏙️ #weekend #city'
        },
        {
          image_url: 'https://picsum.photos/600/600?random=4',
          caption: 'Fresh flowers brighten any day 🌸 #flowers #spring'
        },
        {
          image_url: 'https://picsum.photos/600/600?random=5',
          caption: 'Delicious homemade pasta! 🍝 #food #cooking'
        }
      ];

      // Create posts
      for (const post of samplePosts) {
        await fetch(`http://localhost:8000/posts/?owner_id=${userId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(post),
        });
      }

      // Refresh posts list
      await fetchPosts();
    } catch (err) {
      setError('Failed to create sample posts: ' + err.message);
    } finally {
      setCreating(false);
    }
  };

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
          <div className="no-posts">
            <div>No posts available</div>
            <button 
              className="sample-posts-btn" 
              onClick={createSamplePosts}
              disabled={creating}
            >
              {creating ? 'Creating Sample Posts...' : 'Add Sample Posts'}
            </button>
          </div>
        ) : (
          <>
            <div className="feed-header">
              <button 
                className="sample-posts-btn secondary" 
                onClick={createSamplePosts}
                disabled={creating}
              >
                {creating ? 'Adding...' : 'Add More Sample Posts'}
              </button>
            </div>
            {posts.map((post) => (
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
            ))}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
