document.getElementById('searchInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        const title = encodeURIComponent(this.value.trim());
        if (title) {
            window.location.href = `/search?title=${title}`;
        }
    }
});

document.getElementById('shikiInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        const id = this.value.trim();
        if (/^\d+$/.test(id)) {
            window.location.href = `/title?id=${id}`;
        } else {
            alert('ID должен содержать только цифры');
        }
    }
});