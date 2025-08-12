document.addEventListener("DOMContentLoaded", async () => {
	await loadTitle();
});

async function loadTitle() {
	const res = await fetch(`/api/v1/title/${release_id}/info`);
	if (!res.ok) return;

	const data = await res.json();
	document.title = data.name;
}

const episodeNumberElem = document.getElementById('episodeNumber');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const skipBtn = document.getElementById('skipBtn');
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const devBtn = document.getElementById('devBtn');
const devModal = document.getElementById('devModal');
const playersList = document.getElementById('playersList');
const closeSettings = document.getElementById('closeSettings');
const reloadPlayerBtn = document.getElementById('reloadPlayerBtn');
const playerContainer = document.getElementById('playerContainer');

let currentEpisode = 1;
let playersData = {};
let currentPlayer = null;
let currentQuality = null;
let hls = null;

devBtn.onclick = () => {
  settingsModal.classList.add('hidden');
  devModal.classList.remove('hidden');
};



function closeDevModal() {
  devModal.classList.add('hidden');
}

// Чтение эпизода из хэша или 1 по умолчанию
function readEpisodeFromHash() {
  const hash = window.location.hash;
  if (hash.startsWith('#ep=')) {
    const epNum = parseInt(hash.replace('#ep=', ''), 10);
    if (!isNaN(epNum) && epNum > 0) return epNum;
  }
  return 1;
}

// Обновляем хэш и заголовок эпизода
function updateHash() {
  window.location.hash = `ep=${currentEpisode}`;
  episodeNumberElem.textContent = currentEpisode;
}

// Очищаем контейнер плеера, чтобы вставить видео или iframe
function clearPlayer() {
  // Остановим видео и очистим HLS если был
  if (hls) {
    hls.destroy();
    hls = null;
  }
  playerContainer.innerHTML = '';
}

// Вставляем video тег и запускаем HLS или натив
function insertVideoPlayer(m3u8url, startTime=0) {
  clearPlayer();
  const video = document.createElement('video');
  video.id = 'videoPlayer';
  video.className = 'w-full h-full';
  video.controls = true;
  playerContainer.appendChild(video);

  if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = m3u8url;
    video.currentTime = startTime;
    video.play().catch(() => {});
  } else if (window.Hls) {
    hls = new Hls();
    hls.loadSource(m3u8url);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      if (startTime > 0) video.currentTime = startTime;
      video.play().catch(() => {});
    });
  } else {
    alert('Ваш браузер не поддерживает воспроизведение HLS потоков');
  }
}

// Вставляем iframe с нужным src
function insertIframe(src) {
  clearPlayer();
  const iframe = document.createElement('iframe');
  iframe.src = src;
  iframe.width = '100%';
  iframe.height = '100%';
  iframe.allowFullscreen = true;
  iframe.frameBorder = '0';
  playerContainer.appendChild(iframe);
}

function setPlayerQuality(player, quality, startTime=0) {
  currentPlayer = player;
  currentQuality = quality;

  let url = playersData[player][quality];
  if (typeof url !== 'string') {
    alert('Ошибка: ссылка не строка');
    return;
  }

  if (url.startsWith('!iframe ')) {
    const iframeUrl = url.slice('!iframe '.length).trim();
    insertIframe(iframeUrl);
  } else {
    insertVideoPlayer(url, startTime);
  }
}

// Создаем кнопки выбора плеера и качества в модальном окне
function buildSettingsList() {
  playersList.innerHTML = '';
  Object.entries(playersData).forEach(([playerName, qualities]) => {
    const playerDiv = document.createElement('div');
    playerDiv.classList.add('mb-3');

    const playerTitle = document.createElement('div');
    playerTitle.textContent = playerName;
    playerTitle.classList.add('font-semibold', 'mb-1');
    playerDiv.appendChild(playerTitle);

    // Сортируем ключи (качество) по числовому значению по убыванию
    Object.keys(qualities)
      .sort((a, b) => parseInt(b) - parseInt(a))
      .forEach(quality => {
        const btn = document.createElement('button');
        btn.textContent = quality;
        btn.className = 'mr-2 mb-1 px-3 py-1 bg-zinc-700 rounded hover:bg-zinc-600';
        if (playerName === currentPlayer && quality === currentQuality) {
          btn.classList.add('bg-zinc-500');
        }
        btn.onclick = () => {
          setPlayerQuality(playerName, quality);
          buildSettingsList(); // обновляем выделение
        };
        playerDiv.appendChild(btn);
      });

    playersList.appendChild(playerDiv);
  });
}


// Получаем данные с сервера
async function fetchPlayerData() {
  const url = `/api/v1/title/${release_id}/watch?transl=${translation_id}&ep=${currentEpisode}`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('Ошибка при загрузке данных');
    const data = await res.json();
    playersData = data;
    // Выбираем первый плеер и качество по умолчанию
    const firstPlayer = Object.keys(data)[0];
    const firstQuality = Object.keys(data[firstPlayer])[0];
    setPlayerQuality(firstPlayer, firstQuality);
  } catch (e) {
    alert('Не удалось загрузить поток: ' + e.message);
  }
}

// Обработчики кнопок
settingsBtn.onclick = () => {
  buildSettingsList();
  settingsModal.classList.remove('hidden');
};
closeSettings.onclick = () => {
  settingsModal.classList.add('hidden');
};
prevBtn.onclick = () => {
  if (currentEpisode > 1) {
    currentEpisode--;
    updateHash();
    fetchPlayerData();
  }
};
nextBtn.onclick = () => {
  currentEpisode++;
  updateHash();
  fetchPlayerData();
};
skipBtn.onclick = () => {
  const video = document.getElementById('videoPlayer');
  if (video) {
    video.currentTime += 85;
  }
};

reloadPlayerBtn.onclick = () => {
  if (!currentPlayer || !currentQuality) return;
  const video = document.getElementById('videoPlayer');
  let currentTime = 0;
  // Если текущий плеер - видео, сохраняем текущее время
  if (video && video.tagName.toLowerCase() === 'video') {
    console.log(video.currentTime);
    currentTime = video.currentTime || 0;
  }
  setPlayerQuality(currentPlayer, currentQuality, currentTime);
};

// Инициализация при загрузке страницы
function init() {
  currentEpisode = readEpisodeFromHash();
  updateHash();
  fetchPlayerData();
}

// При смене хэша URL
window.onhashchange = () => {
  const ep = readEpisodeFromHash();
  if (ep !== currentEpisode) {
    currentEpisode = ep;
    episodeNumberElem.textContent = currentEpisode;
    fetchPlayerData();
  }
};

init();