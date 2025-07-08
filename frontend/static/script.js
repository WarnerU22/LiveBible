function initShareButton() {
  const btn = document.getElementById('shareButton');
  if (!btn) return;
  btn.addEventListener('click', async () => {
    const url = 'https://livebible.live';
    try {
      await navigator.clipboard.writeText(url);
      btn.innerText = 'Link Copied!';
      setTimeout(() => (btn.innerText = 'Copy Link'), 2000);
    } catch (err) {
      prompt('Share this link:', url);
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initShareButton();
});
