document.addEventListener("DOMContentLoaded", async () => {
	await loadTitleInfo();
	await loadTranslations();
	await loadRelated();
});

async function loadTitleInfo() {
	const res = await fetch(`/api/v1/title/${release_id}/info`);
	if (!res.ok) return;

	const data = await res.json();
	document.getElementById("title").textContent = data.name;

	const posterImg = document.getElementById("banner");
	if (posterImg && data.poster) {
		posterImg.src = data.poster;
	}

	document.title = data.name;

	const metaContainer = document.getElementById("info-container");

	// Если статус "Анонс", отображаем только название и статус
	if (data.status === "Анонс") {
		metaContainer.innerHTML = `
			<h1 class="text-2xl font-bold">${data.name}</h1>
			<p><span class="font-semibold">Статус:</span> ${data.status}</p>
		`;
		return;
	}

	// Иначе — вся остальная информация
	metaContainer.innerHTML = `
		<h1 class="text-2xl font-bold">${data.name}</h1>
		<p><span class="font-semibold">Тип:</span> ${data.type}</p>
		<p><span class="font-semibold">Статус:</span> ${data.status}</p>
		<p><span class="font-semibold">Оценка:</span> ${data.score}</p>
		<p><span class="font-semibold">Возрастной рейтинг:</span> ${data.rating}</p>
	`;
	if (data.is_ongoing) {
		metaContainer.innerHTML += `
			<p><span class="font-semibold">Кол-во серий:</span> ${data.released_episodes}/${data.total_episodes}</p>
			<p><span class="font-semibold">Даты:</span> с ${data.started}</p>
			<p><span class="font-semibold">Следующая серия:</span> ${data.next_episode_at}</p>
		`;
	} else {
		metaContainer.innerHTML += `
			<p><span class="font-semibold">Кол-во серий:</span> ${data.total_episodes}</p>
			<p><span class="font-semibold">Даты:</span> с ${data.started} по ${data.released}</p>
		`;
	}
}


async function loadTranslations() {
	const res = await fetch(`/api/v1/title/${release_id}/translations`);
	if (!res.ok) return;

	const data = await res.json();
	const container = document.getElementById("translations-container");
	const title = document.getElementById("translations");
    if (data.length > 0 && title.classList.contains("hidden")) {
		title.classList.remove("hidden");
	}

	for (const t of data.translations) {
		const btn = document.createElement("a");
		btn.href = `/watch/${release_id}/${t.id}`;
		btn.textContent = t.name;
		btn.className = "bg-zinc-800 hover:bg-zinc-700 px-4 py-2 rounded shadow";
		container.appendChild(btn);
	}
}

async function loadRelated() {
	const res = await fetch(`/api/v1/title/${release_id}/related`);
	if (!res.ok) return;

	const data = await res.json();
	const container = document.getElementById("related-container");

    const title = document.getElementById("related-titles");
    if (data.length > 0 && title.classList.contains("hidden")) {
		title.classList.remove("hidden");
	}

	container.innerHTML = "";

	for (const item of data) {
		const content = item.anime || item.manga;
		const type = item.anime ? "Аниме" : "Манга";

		const block = document.createElement("div");
		block.className = "bg-zinc-900 p-3 rounded shadow flex items-start gap-4 w-full max-w-md";

		block.innerHTML = `
			<img src="${content.image ? 'https://shikimori.one' + content.image.preview : '/resources/no_poster.jpg'}"
				alt="${type}" class="w-20 h-auto rounded object-cover" />
			<div class="flex-1">
				<h3 class="font-semibold text-sm leading-snug">${content.name}</h3>
				<p class="text-sm text-gray-400">${type} – ${item.type}<br>${content.aired_on}</p>
			</div>
		`;

		container.appendChild(block);
	}
}
