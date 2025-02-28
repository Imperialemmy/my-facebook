async function fetchVideos() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        console.error("No token found! Redirecting to login...");
        window.location.href = loginpage;
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/watch/", {
            method: "GET",
            headers: {
                "Authorization": `JWT ${token}`,
                "Content-Type": "application/json"
            }
        });

        if (response.status === 401) {  // Token is invalid/expired
            console.error("Invalid token! Redirecting to login...");
            localStorage.removeItem("access_token");  // Remove invalid token
            window.location.href = loginpage;
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to fetch videos");
        }

        const data = await response.json();
        renderVideos(data);
    } catch (error) {
        console.error("Error fetching videos:", error);
    }
}

function renderVideos(videos) {
    const watchContainer = document.getElementById("watch-container");
    watchContainer.innerHTML = "";

    if (videos.length === 0) {
        watchContainer.innerHTML = "<p>No videos available.</p>";
        return;
    }

    videos.forEach(video => {
        const videoElement = document.createElement("div");
        videoElement.classList.add("video-card");

        videoElement.innerHTML = `
             <p>${video.username}</p>
             <h3>${video.description}</h3>
             <h5>${video.created_at}</h5>
            <video controls>
                <source src="${video.video}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="video-actions">
                <button class="like-btn">Like (${video.likes})</button>
                <button class="comment-btn">Comment</button>
                <button class="save-btn">Save</button>
            </div>
        `;

        watchContainer.appendChild(videoElement);
    });
}

document.addEventListener("DOMContentLoaded", fetchVideos);


console.log("watch.js loaded");
