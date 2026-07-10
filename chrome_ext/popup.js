document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('playBtn').addEventListener('click', (e) => {
    e.preventDefault();
    chrome.tabs.create({ url: 'https://playtree.game' });
  });

  document.getElementById('downloadBtn').addEventListener('click', (e) => {
    e.preventDefault();
    chrome.tabs.create({ url: 'https://playtree.game/#download' });
  });

  document.getElementById('rateBtn').addEventListener('click', () => {
    chrome.tabs.create({ url: 'https://chrome.google.com/webstore/detail/playtree' });
  });

  document.getElementById('siteBtn').addEventListener('click', () => {
    chrome.tabs.create({ url: 'https://playtree.game' });
  });
});
