document.addEventListener("DOMContentLoaded", function() {
    const wishlist = document.getElementById('wishlist');

    fetch('http://localhost:5000/get_wishlist')
        .then(response => {
            if (!response.ok) {
                throw new Error('Netzwerkantwort war nicht ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.length === 0) {
                const li = document.createElement('li');
                li.textContent = 'Ganz schön leer hier...';
                li.style.textAlign = 'center';
                li.style.color = '#E0E0E0';
                wishlist.appendChild(li);
            } else {
                data.forEach(entry => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <span>${entry.title} (${entry.year})</span>
                        <span>${entry.category}</span>
                        <button onclick="removeFromWishlist(${entry.id}, this)">🗑</button>
                    `;
                    wishlist.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error('Es gab ein Problem mit der Fetch-Operation:', error);
        });

    window.removeFromWishlist = function(id, button) {
        fetch(`http://localhost:5000/remove_entry/${id}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Netzwerkantwort war nicht ok');
            }
            const li = button.parentElement;
            wishlist.removeChild(li);
            if (wishlist.children.length === 0) {
                const emptyLi = document.createElement('li');
                emptyLi.textContent = 'Ganz schön leer hier...';
                emptyLi.style.textAlign = 'center';
                emptyLi.style.color = '#E0E0E0';
                wishlist.appendChild(emptyLi);
            }
        })
        .catch(error => {
            console.error('Es gab ein Problem mit der Fetch-Operation:', error);
        });
    }
});

