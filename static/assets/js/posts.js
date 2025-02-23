

// Function to fetch and render posts
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
    const posts = data.results;
    const feedContainer = document.getElementById('feed-container');
    feedContainer.innerHTML = '';

    posts.forEach(post => {
      const imagesHTML = post.post_images.map(img => `<img src="${img.image}" alt="Post Image">`).join('');
      const postHTML = `
        <div class="feed-post" id="post-${post.id}">
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
            <button onclick="likePost(${post.id})"><i class="fas fa-thumbs-up"></i></button>
            <button onclick="toggleComments(${post.id})"><i class="fas fa-comment"></i></button>
            <button onclick="sendPost(${post.id})"><i class="fas fa-paper-plane"></i></button>
            <button onclick="sharePost(${post.id})"><i class="fas fa-share-alt"></i></button>
          </div>

          <div class="comments-container" id="comments-${post.id}" style="display: none;">
            <div class="add-comment-form">
              <textarea style= "font-family: Segoe UI Historic, Segoe UI, Helvetica, Arial, sans-serif;" id="new-comment-text-${post.id}" placeholder="Write a comment..."></textarea>
              <button class="comment-btn" onclick=" postComment(${post.id})">comment</button>
            </div>
          </div>
        </div>
      `;
      feedContainer.innerHTML += postHTML;
    });
  } catch (error) {
    console.error('Error fetching posts:', error);
  }
}

// Function to toggle the visibility of the comments section
async function toggleComments(postId) {
  const commentsContainer = document.getElementById(`comments-${postId}`);
  const commentsBtn = document.querySelector(`#post-${postId} .post-actions .comments-btn`);

  if (commentsContainer.style.display === "none") {
    commentsContainer.style.display = "block";

    if (!commentsContainer.dataset.loaded) {
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.error('No access token found');
        return;
      }

      // Decode the JWT token to get the logged-in user's ID
      const decodedToken = jwt_decode(token);
      const loggedInUserId = decodedToken.user_id;
      const response = await fetch(`/api/posts/${postId}/comments/`, {
        headers: {
          'Authorization': `JWT ${token}`,  // Use 'Bearer' if using Simple JWT
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        console.error('Failed to fetch comments:', response.statusText);
        return;
      }

      const comments = await response.json();
      console.log('Comments response:', comments);

      comments.forEach(comment => {
        const commentElement = document.createElement("div");
        commentElement.classList.add("comment");
        commentElement.innerHTML = `
          <p>${comment.username}: ${comment.content}</p>
          ${comment.user == loggedInUserId ? `
            <button onclick="editComment(${postId}, ${comment.id})">Edit</button>
            <button onclick="deleteComment(${postId}, ${comment.id})">Delete</button>
          ` : ''}
        `;
        // console.log(comment.user.id == loggedInUserId); // Debugging the comparison

        commentsContainer.appendChild(commentElement);
      });

      commentsContainer.dataset.loaded = true;
    }

    commentsBtn.innerText = "Hide Comments";
  } else {
    commentsContainer.style.display = "none";
    commentsBtn.innerText = "Show Comments";
  }
}


// Function to delete a comment
async function deleteComment(postId, commentId) {
  const confirmation = confirm("Are you sure you want to delete this comment?");
  if (!confirmation) return;

  try {
    const response = await fetch(`/api/posts/${postId}/comments/${commentId}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `JWT ${localStorage.getItem('access_token')}`,
      },
    });

    if (response.ok) {
      removeCommentFromUI(postId, commentId);
    } else {
      alert("Failed to delete comment.");
    }
  } catch (error) {
    console.error("Error deleting comment:", error);
    alert("An error occurred while deleting the comment.");
  }
}

// Helper function to remove the comment from the UI after deletion
function removeCommentFromUI(postId, commentId) {
  const commentElement = document.getElementById(`comment-${commentId}`);
  if (commentElement) {
    commentElement.remove();
  }
}


// Function to post a new comment
async function postComment(postId) {
  const commentText = document.getElementById(`new-comment-text-${postId}`).value;
  if (!commentText) return;

  const formData = new FormData();
  formData.append('content', commentText);  // 'text' should match the field name in your serializer
  formData.append('post', postId);  // Include the post ID

  const response = await fetch(`/api/posts/${postId}/comments/`, {
    method: 'POST',
    headers: {
      'Authorization': `JWT ${localStorage.getItem('access_token')}`,  // Assuming JWT token is used
    },
    body: formData,  // Send the FormData
  });

  if (response.ok) {
    const newComment = await response.json();
    const commentsContainer = document.getElementById(`comments-${postId}`);
    const newCommentElement = document.createElement("div");
    newCommentElement.classList.add("comment");
    newCommentElement.innerHTML = `
      <p>${newComment.username}: ${newComment.content}</p>
      <button onclick="editComment(${postId}, ${newComment.id})">Edit</button>
      <button onclick="deleteComment(${postId}, ${newComment.id})">Delete</button>
    `;
    commentsContainer.appendChild(newCommentElement);
    document.getElementById(`new-comment-text-${postId}`).value = ''; // Clear the textarea
  } else {
    alert("Failed to post comment.");
  }
}

// Function for liking a post (this is just a placeholder, you can implement it later)
async function likePost(postId) {
  // Like post implementation here
}


document.addEventListener('DOMContentLoaded', fetchAndRenderPosts);









