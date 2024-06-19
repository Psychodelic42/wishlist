document.addEventListener("DOMContentLoaded", function() {
    const categories = document.querySelectorAll('.category');
    const overlay = document.getElementById('overlay');
    const categoryOptions = document.getElementById('category-options');
    const formContainer = document.getElementById('form-container');
    const entryForm = document.getElementById('entry-form');
    const cancelBtn = document.getElementById('cancel');
    let selectedCategory = '';

    categories.forEach(category => {
        category.addEventListener('click', function() {
            selectedCategory = this.id;
            showCategoryOptions(this.id);
        });
    });

    function showCategoryOptions(category) {
        overlay.style.display = 'flex';
        categoryOptions.innerHTML = '';
        let options = '';
        switch (category) {
            case 'film':
                options = `
                    <button class="option-btn" onclick="selectOption('Anime')">Anime</button>
                    <button class="option-btn" onclick="selectOption('Nicht-Anime')">Nicht-Anime</button>
                `;
                break;
            case 'serie':
                options = `
                    <button class="option-btn" onclick="selectOption('Anime-Serie')">Anime-Serie</button>
                    <button class="option-btn" onclick="selectOption('Nicht-Anime-Serie')">Nicht-Anime-Serie</button>
                `;
                break;
            case 'hoerbuch':
                selectOption('');
                return;
            case 'ebook':
                options = `
                    <button class="option-btn" onclick="selectOption('Literatur/Fachbuch')">Literatur/Fachbuch</button>
                    <button class="option-btn" onclick="selectOption('Comic')">Comic</button>
                    <button class="option-btn" onclick="selectOption('Manga')">Manga</button>
                    <button class="option-btn" onclick="selectOption('Roman')">Roman</button>
                    <button class="option-btn" onclick="selectOption('Sonstiges')">Sonstiges</button>
                `;
                break;
        }
        categoryOptions.innerHTML = options;
    }

    window.selectOption = function(option) {
        overlay.style.display = 'none';
        formContainer.style.display = 'flex';
    }

    entryForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const title = entryForm.title.value;
        const year = entryForm.year.value;
        const link = entryForm.link.value;
        addToWishlist({ title, year, link, category: selectedCategory });
        formContainer.style.display = 'none';
        entryForm.reset();
    });

    cancelBtn.addEventListener('click', function() {
        formContainer.style.display = 'none';
        entryForm.reset();
    });

    function addToWishlist(entry) {
        fetch('http://localhost:5000/add_entry', {  // Update to the correct URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(entry),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Eintrag hinzugefügt!");
            } else {
                alert("Fehler beim Hinzufügen des Eintrags!");
            }
        });
    }
});
