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

function initCopyVersesButton() {
  const btn = document.getElementById('copyVersesButton');
  const container = document.getElementById('versesContainer');
  if (!btn || !container) return;
  btn.addEventListener('click', async () => {
    const text = container.innerText.trim();
    try {
      await navigator.clipboard.writeText(text);
      btn.innerText = 'Copied!';
      setTimeout(() => (btn.innerText = 'Copy Verses'), 2000);
    } catch (err) {
      prompt('Copy these verses:', text);
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initShareButton();
  initCopyVersesButton();
});
