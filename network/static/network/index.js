document.addEventListener('DOMContentLoaded', function () {
  
  const postForm = document.querySelector('#compose-post')
  if(postForm) {
    postForm.addEventListener('submit', compose_post)
  }

  const allPostsSection = document.querySelector('#all-posts');
  load_posts();

/*   const socket = new WebSocket('ws://127.0.0.1:8000/ws/posts');
  socket.onmessage = function (e) {
    const post = JSON.parse(e.data);
    add_post_to_dom(post);
  }; */

  async function load_posts() {
    try {
      allPostsSection.innerHTML = '';
  
      const response = await fetch('http://127.0.0.1:8000/posts');
  
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
  
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Expected JSON response');
      }
  
      const posts = await response.json();
  
      posts.forEach((post) => {
        allPostsSection.innerHTML += add_post_to_dom(post);
      });
  
    } catch (err) {
      console.error('Error loading posts', err);
      allPostsSection.innerHTML = '<p>Error loading posts. Please try again later.</p>';
    }
  }
  

  async function compose_post(e) {
    e.preventDefault();
    try {
      const content = document.querySelector('#content').value;
      const csrftoken = getCookie('csrftoken');
      const response = await fetch('http://127.0.0.1:8000/compose', {
        method: 'POST',
        headers: {
          Accept: 'application/json, text/plain, */*',
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
          content: content,
        }),
      });

      document.querySelector('#content').value = '';
      const responseData = await response.json(); 

      if (response.status === 'success') {
        load_posts();
        alert(response.message);
      } else {
        // Handle error response
        alert(responseData.message);
        throw new Error(responseData.message || 'Post creation failed');
      }
    } catch (err) {
      throw new Error(err, 'Post creation failed');
    }
  }
});

async function like_post(postId) {
  try {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(`http://127.0.0.1:8000/like/${postId}`, {
      headers: {
        Accept: 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      method: 'POST',
    });
    const responseData = await response.json();
    if (responseData.status === 'success') {
      window.location.reload();
      alert(responseData.message);
    } else {
      alert('Post like failed');
      throw new Error('Post like failed');
    }
  } catch (err) {
    console.error('Error liking post', err);
  }
}


// Template

function add_post_to_dom(post) {
  const postElement = document.createElement('div');
  return postElement.innerHTML = `
    <div class="card mb-3 d-flex flex-row justify-content-between">
      <div class="card-body">
        <h5 class="card-title">${post.user}</h5>
        <p class="card-text">${post.content}</p>
        <p class="card-text"><small class="text-muted">${post.timestamp}</small></p>
        <span class="d-flex">
          <span onclick="like_post(${post.id})" class="material-symbols-outlined icon">favorite</span> 
          <span>${post.likes.length}</span>
        </span>
      </div>
      <div>
        <button class="btn text-primary">Edit</button>
      </div>
    </div>
  `;
}

// Utils

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
