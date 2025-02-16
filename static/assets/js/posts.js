async function fetchAndRenderPosts() {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const response = await fetch('/api/posts/', {
      headers: {
        'Authorization': `JWT ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) throw new Error('Failed to fetch posts');

    const data = await response.json();
    const posts = data.results; // Access the results array
    const feedContainer = document.getElementById('feed-container');
    feedContainer.innerHTML = '';

    posts.forEach(post => {
      const imagesHTML = post.post_images.map(img => `<img src="${img.image}" alt="Post Image">`).join('');
      const postHTML = `
        <div class="feed-post">
          <div class="post-header">
            <img src="${post.user.profile_picture}" alt="Profile Picture">
            <div>
              <span class="username">${post.username}</span>
              <span class="timestamp">${new Date(post.created_at).toLocaleString()}</span>
            </div>
          </div>
          <div class="post-content">
            <p>${post.content}</p>
            ${imagesHTML}
          </div>
          <div class="post-actions">
            <button>Like</button>
            <button>Comment</button>
            <button>Send</button>
            <button>Share</button>
          </div>
        </div>
      `;
      feedContainer.innerHTML += postHTML;
    });
  } catch (error) {
    console.error('Error fetching posts:', error);
  }
}

document.addEventListener('DOMContentLoaded', fetchAndRenderPosts);





