
const myVideo = document.getElementById('contentVideo');
const playPromise = myVideo.play() || Promise.reject('');
playPromise.then(() => {
  // Video could be autoplayed, do nothing.
}).catch(err => {
  // Video couldn't be autoplayed because of autoplay policy. Mute it and play.
  myVideo.muted = true;
  myVideo.loop = true;
  myVideo.volume = 0.25;
  myVideo.play();
});