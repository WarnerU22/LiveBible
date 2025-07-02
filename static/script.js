function initShareButton() {
  const btn = document.getElementById('shareButton');
  if (!btn) return;
  btn.addEventListener('click', async () => {
    const shareData = {
      title: 'LiveBible.Live',
      text: 'Find biblical encouragement at LiveBible.Live',
      url: 'https://livebible.live',
    };
    if (navigator.share) {
      try {
        await navigator.share(shareData);
      } catch (err) {
        console.error('Share failed:', err);
      }
    } else {
      prompt('Share this link:', shareData.url);
    }
  });
}

document.addEventListener('DOMContentLoaded', initShareButton);
