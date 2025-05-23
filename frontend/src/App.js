import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [creating, setCreating] = useState(false);
  const [comments, setComments] = useState({});
  const [newComments, setNewComments] = useState({});
  const [postingComment, setPostingComment] = useState({});
  const [showAllComments, setShowAllComments] = useState({});

  const fetchPosts = async () => {
    try {
      const response = await fetch('http://localhost:8000/posts/');
      if (!response.ok) {
        throw new Error('Failed to fetch posts');
      }
      const postsData = await response.json();
      setPosts(postsData);
      
      // Fetch comments for each post
      const commentsData = {};
      for (const post of postsData) {
        try {
          const commentsResponse = await fetch(`http://localhost:8000/posts/${post.id}/comments/`);
          if (commentsResponse.ok) {
            commentsData[post.id] = await commentsResponse.json();
          }
        } catch (err) {
          console.warn(`Failed to fetch comments for post ${post.id}:`, err);
        }
      }
      setComments(commentsData);
    } catch (err) {
      setError(err.message);
    }
  };

  const fetchPostComments = async (postId) => {
    try {
      const response = await fetch(`http://localhost:8000/posts/${postId}/comments/`);
      if (response.ok) {
        const postComments = await response.json();
        setComments(prev => ({
          ...prev,
          [postId]: postComments
        }));
      }
    } catch (err) {
      console.warn(`Failed to fetch comments for post ${postId}:`, err);
    }
  };

  const createComment = async (postId, commentText) => {
    if (!commentText.trim()) return;
    
    setPostingComment(prev => ({ ...prev, [postId]: true }));
    try {
      const response = await fetch(`http://localhost:8000/comments/?post_id=${postId}&user_id=1`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: commentText.trim()
        }),
      });
      
      if (response.ok) {
        setNewComments(prev => ({ ...prev, [postId]: '' }));
        await fetchPostComments(postId);
      } else {
        throw new Error('Failed to create comment');
      }
    } catch (err) {
      setError('Failed to create comment: ' + err.message);
    } finally {
      setPostingComment(prev => ({ ...prev, [postId]: false }));
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

      // Create posts and collect their IDs
      const createdPostIds = [];
      for (const post of samplePosts) {
        const response = await fetch(`http://localhost:8000/posts/?owner_id=${userId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(post),
        });
        if (response.ok) {
          const createdPost = await response.json();
          createdPostIds.push(createdPost.id);
        }
      }

      // Sample comments for posts
      const sampleComments = [
        "Amazing shot! 📸",
        "Love this! 😍",
        "So beautiful!",
        "Great composition 👌",
        "Wow, incredible! 🔥",
        "This is gorgeous! ✨",
        "Perfect timing!",
        "Absolutely stunning 🌟",
        "Love the colors!",
        "This made my day! 😊"
      ];

      // Create comments for each post
      for (const postId of createdPostIds) {
        // Create 2-4 random comments per post
        const numComments = Math.floor(Math.random() * 3) + 2;
        const shuffledComments = [...sampleComments].sort(() => 0.5 - Math.random());
        
        for (let i = 0; i < numComments; i++) {
          try {
            await fetch(`http://localhost:8000/comments/?post_id=${postId}&user_id=${userId}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                text: shuffledComments[i]
              }),
            });
          } catch (err) {
            console.warn(`Failed to create comment for post ${postId}:`, err);
          }
        }
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
            {posts.map((post) => {
              const postComments = comments[post.id] || [];
              const displayComments = showAllComments[post.id] ? postComments : postComments.slice(0, 3);
              const hasMoreComments = postComments.length > 3;

              return (
                <div key={post.id} className="post-card">
                  <div className="post-image">
                    <img src={post.image_url} alt="Post" />
                  </div>
                  <div className="post-content">
                    <p className="post-caption">{post.caption}</p>
                    
                    {/* Comments Section */}
                    {postComments.length > 0 && (
                      <div className="comments-section">
                        <div className="comments-list">
                          {displayComments.map((comment, index) => (
                            <div key={comment.id} className="comment">
                              <span className="comment-text">{comment.text}</span>
                              <span className="comment-date">
                                {new Date(comment.created_at).toLocaleDateString()}
                              </span>
                            </div>
                          ))}
                        </div>
                        
                        {hasMoreComments && !showAllComments[post.id] && (
                          <button 
                            className="more-comments-btn"
                            onClick={() => setShowAllComments(prev => ({ ...prev, [post.id]: true }))}
                          >
                            View all {postComments.length} comments
                          </button>
                        )}
                        
                        {showAllComments[post.id] && hasMoreComments && (
                          <button 
                            className="more-comments-btn"
                            onClick={() => setShowAllComments(prev => ({ ...prev, [post.id]: false }))}
                          >
                            Show fewer comments
                          </button>
                        )}
                      </div>
                    )}
                    
                    {/* Add Comment Form */}
                    <div className="add-comment">
                      <input
                        type="text"
                        placeholder="Add a comment..."
                        value={newComments[post.id] || ''}
                        onChange={(e) => setNewComments(prev => ({ 
                          ...prev, 
                          [post.id]: e.target.value 
                        }))}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') {
                            createComment(post.id, newComments[post.id] || '');
                          }
                        }}
                        disabled={postingComment[post.id]}
                        className="comment-input"
                      />
                      <button
                        onClick={() => createComment(post.id, newComments[post.id] || '')}
                        disabled={postingComment[post.id] || !(newComments[post.id] || '').trim()}
                        className="post-comment-btn"
                      >
                        {postingComment[post.id] ? 'Posting...' : 'Post'}
                      </button>
                    </div>
                    
                    <div className="post-meta">
                      <span className="post-date">
                        {new Date(post.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
