document.getElementById('searchInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        const query = encodeURIComponent(this.value.trim());
        if (query) {
            window.location.href = `/search?query=${query}`;
        }
    }
});

document.getElementById('shikiInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        const id = this.value.trim();
        if (/^\d+$/.test(id)) {
            window.location.href = `/release?id=${id}`;
        } else {
            alert('ID должен содержать только цифры');
        }
    }
});