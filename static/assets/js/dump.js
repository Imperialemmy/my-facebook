
//for fetching posts individually

// document.addEventListener('DOMContentLoaded', () => {
//   fetchOtherPostsDetails();
//   fetchPostsDetails();
//   fetchMyContent();
// });
//
//
//
// async function fetchPostsDetails() {
//   const token = localStorage.getItem('access_token');
//   if (!token) return;
//
//   try {
//     const response = await fetch('/auth/users/me/', {
//       headers: {
//         'Authorization': `JWT ${token}`,
//         'Content-Type': 'application/json'
//       }
//     });
//
//     if (!response.ok) throw new Error('Failed to fetch user details');
//
//     const user = await response.json();
//     document.getElementById('username').innerText = user.username;
//   } catch (error) {
//     console.error('Error fetching user details:', error);
//   }
// }
//
//
//
// async function fetchOtherPostsDetails() {
//   const token = localStorage.getItem('access_token');
//   if (!token) return;
//
//   try {
//     const response = await fetch('/api/users/2/', {
//       headers: {
//         'Authorization': `JWT ${token}`,
//         'Content-Type': 'application/json'
//       }
//     });
//
//     if (!response.ok) throw new Error('Failed to fetch user details');
//
//     const user = await response.json();
//     document.getElementById('user').innerText = user.username;
//   } catch (error) {
//     console.error('Error fetching user details:', error);
//   }
// }
//
//
// async function fetchMyContent() {
//   const token = localStorage.getItem('access_token');
//   if (!token) return;
//
//   try {
//     const response = await fetch('/api/posts/1/', {
//       headers: {
//         'Authorization': `JWT ${token}`,
//         'Content-Type': 'application/json'
//       }
//     });
//
//     if (!response.ok) throw new Error('Failed to fetch user details');
//
//     const user = await response.json();
//     document.getElementById('my_content').innerText = user.content;
//   } catch (error) {
//     console.error('Error fetching user details:', error);
//   }
// }