document.addEventListener("DOMContentLoaded", async () => {
	await loadTitle();
});

async function loadTitle() {
	const res = await fetch(`/api/v1/title/${release_id}/info`);
	if (!res.ok) return;

	const data = await res.json();
	document.title = data.name;
}
