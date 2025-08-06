document.getElementById('searchForm').addEventListener('submit', function (e) {
  e.preventDefault();
  const query = new URLSearchParams(new FormData(this)).toString();

  fetch('/search/version_03?' + query)
    .then(res => res.json())
    .then(data => {
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '';

      data.videos.forEach((video, index) => {
        const container = document.createElement('div');
        container.className = 'video-container';

        container.innerHTML = `
          <video id="video${index}" src="${video.url}" preload="metadata" controls></video>
          <div class="controls">
            <button onclick="togglePlay(${index})"><i class="fa-solid fa-play" id="play-icon-${index}"></i></button>
            <input type="range" class="progress" id="progress-${index}" value="0">
            <input type="range" class="volume" id="volume-${index}" min="0" max="1" step="0.01" value="1">
          </div>
        `;

        resultsDiv.appendChild(container);

        const videoElem = document.getElementById(`video${index}`);
        const progress = document.getElementById(`progress-${index}`);
        const volume = document.getElementById(`volume-${index}`);

        videoElem.addEventListener('timeupdate', () => {
          progress.value = videoElem.currentTime / videoElem.duration || 0;
        });

        progress.addEventListener('input', () => {
          videoElem.currentTime = progress.value * videoElem.duration;
        });

        volume.addEventListener('input', () => {
          videoElem.volume = volume.value;
        });

        videoElem.addEventListener('play', () => {
          document.getElementById(`play-icon-${index}`).className = 'fa-solid fa-pause';
        });

        videoElem.addEventListener('pause', () => {
          document.getElementById(`play-icon-${index}`).className = 'fa-solid fa-play';
        });
      });
    });
});

function togglePlay(index) {
  const video = document.getElementById(`video${index}`);
  if (video.paused) {
    video.play();
  } else {
    video.pause();
  }
}
