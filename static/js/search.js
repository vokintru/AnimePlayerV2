let debounceTimeout;
let currentRequestId = 0;
let infoQueue = [];
let infoTimerActive = false;

const searchInput = document.getElementById('searchInput');
const container = document.getElementById('resultContainer');

function redirectIfReauth(response, json = null) {
	if (response.status === 403 || json === 'reauth') {
		window.location.href = '/shiki_auth_link';
		return true;
	}
	return false;
}

searchInput.addEventListener('input', () => handleSearch(searchInput.value.trim()));
window.addEventListener('DOMContentLoaded', () => {
	const initialQuery = searchInput.value.trim();
	if (initialQuery) handleSearch(initialQuery); // автозапуск, если есть текст
});

function handleSearch(query) {
	clearTimeout(debounceTimeout);

	debounceTimeout = setTimeout(async () => {
		container.innerHTML = '';
		if (!query) return;

		const thisRequestId = ++currentRequestId;
		infoQueue = [];

		try {
			const searchResponse = await fetch(/api/v1/search/${encodeURIComponent(query)});
			if (!searchResponse.ok) throw new Error('Ошибка запроса поиска');

			const searchResults = await searchResponse.json();
			if (thisRequestId !== currentRequestId) return;

			if (!Array.isArray(searchResults) || searchResults.length === 0) {
				container.innerHTML = '<p class="text-white">Ничего не найдено</p>';
				return;
			}

			searchResults.forEach((item, index) => {
				const link = document.createElement('a');
				link.href = /release?id=${item.id};
				link.className = 'block';

				const placeholder = document.createElement('div');
				placeholder.className = 'flex items-start gap-6 text-white p-2 rounded-lg max-w-2xl';
				placeholder.dataset.id = item.id;

				placeholder.innerHTML =
					<img
						src="/resources/no_poster.jpg"
						alt="Постер"
						class="w-full max-w-[120px] h-auto rounded-md object-cover"
					/>
					<div class="space-y-2 text-md leading-relaxed">
						<h2 class="text-lg font-bold">Загрузка...</h2>
						<p><span class="font-semibold">Тип:</span> <span class="text-gray-300">—</span></p>
						<p><span class="font-semibold">Статус:</span> <span class="text-gray-300">—</span></p>
						<p><span class="font-semibold">Эпизодов:</span> <span class="text-gray-300">—</span></p>
					</div>
				;

				link.appendChild(placeholder);
				container.appendChild(link);

				if (index < searchResults.length - 1) {
					container.appendChild(document.createElement('hr'));
				}

				infoQueue.push(() => loadTitleInfo(item.id, placeholder, thisRequestId));
			});

			startInfoQueue();
		} catch (error) {
			if (thisRequestId === currentRequestId) {
				console.error('Ошибка при поиске:', error);
			}
		}
	}, 300);
}

function startInfoQueue() {
	if (infoTimerActive) return;

	infoTimerActive = true;
	const interval = setInterval(() => {
		if (infoQueue.length === 0) {
			clearInterval(interval);
			infoTimerActive = false;
			return;
		}
		const task = infoQueue.shift();
		task();
	}, 200);
}

async function loadTitleInfo(id, placeholder, requestId) {
	try {
		const infoResponse = await fetch(`/api/v1/title/${id}/info`);
		if (!infoResponse.ok) {
			if (infoResponse.status === 403) {
				window.location.href = '/shiki_auth_link';
				return;
			}
			throw new Error('Ошибка запроса info');
		}
		if (requestId !== currentRequestId) return;

		const info = await infoResponse.json();
		if (redirectIfReauth(infoResponse, info)) return;

		placeholder.innerHTML = `
			<img
				src="${info.poster}"
				alt="Постер"
				class="w-full max-w-[120px] h-auto rounded-md object-cover"
			/>
			<div class="space-y-2 text-md leading-relaxed">
				<h2 class="text-lg font-bold">${info.name}</h2>
				<p><span class="font-semibold">Тип:</span> <span class="text-gray-300">${info.type}</span></p>
				<p><span class="font-semibold">Статус:</span> <span class="text-gray-300">${info.status}</span></p>
				<p><span class="font-semibold">Эпизодов:</span> <span class="text-gray-300">${info.released_episodes}/${info.total_episodes}</span></p>
			</div>
		`;
	} catch (err) {
		console.error(`Ошибка info для id=${id}:`, err);
	}
}
