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

function showUpgradeModalIfNeeded() {
  const modalEl = document.getElementById('upgradeModal');
  if (modalEl && modalEl.dataset.show === 'true') {
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initShareButton();
  showUpgradeModalIfNeeded();
});
