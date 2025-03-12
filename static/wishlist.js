document.addEventListener("DOMContentLoaded", function () {
    fetch("/get_wishlist")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("wishlist");
            tableBody.innerHTML = "";

            data.forEach(entry => {
                const row = document.createElement("tr");

                const titleCell = document.createElement("td");
                titleCell.textContent = entry.title;

                const yearCell = document.createElement("td");
                yearCell.textContent = entry.year;

                const categoryCell = document.createElement("td");
                categoryCell.textContent = entry.category;

                const notesCell = document.createElement("td");
                notesCell.textContent = entry.notes || "";

                const actionCell = document.createElement("td");
                
                const editButton = document.createElement("button");
                editButton.textContent = "📝";
                editButton.classList.add("edit-btn");
                editButton.dataset.id = entry.id;
                editButton.dataset.notes = entry.notes || "";
                actionCell.appendChild(editButton);
                
                const deleteBtn = document.createElement("button");
                deleteBtn.textContent = "🗑️";
                deleteBtn.classList.add("delete-btn");
                deleteBtn.dataset.id = entry.id;
                actionCell.appendChild(deleteBtn);

                row.appendChild(titleCell);
                row.appendChild(yearCell);
                row.appendChild(categoryCell);
                row.appendChild(notesCell);
                row.appendChild(actionCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Fehler beim Laden der Wunschliste:", error));
});

// Event Delegation für das Editieren von Bemerkungen
document.getElementById("wishlist").addEventListener("click", function (event) {
    if (event.target.classList.contains("edit-btn")) {
        const entryId = event.target.dataset.id;
        const currentNotes = event.target.dataset.notes;
        openEditModal(entryId, currentNotes);
    }
    if (event.target.classList.contains("delete-btn")) {
        const entryId = event.target.dataset.id;
        removeFromWishlist(entryId, event.target);
    }
});

function openEditModal(entryId, currentNotes) {
    const modal = document.getElementById("editModal");
    const modalInput = document.getElementById("modalNotes");
    const saveButton = document.getElementById("saveNotes");

    modal.style.display = "flex";
    modalInput.value = currentNotes;
    
    saveButton.onclick = function () {
        const newNotes = modalInput.value;
        fetch("/update_notes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: entryId, notes: newNotes })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                console.error("Fehler beim Speichern der Bemerkung");
            }
        })
        .catch(error => console.error("Netzwerkfehler:", error));
    };
}

// Modal schließen
document.getElementById("cancelNotes").addEventListener("click", function () {
    document.getElementById("editModal").style.display = "none";
});

// Funktion zum Entfernen eines Eintrags aus der Wunschliste
function removeFromWishlist(id, button) {
    console.log(`Removing entry with ID: ${id}`);
    fetch(`/remove_entry/${id}`, {
        method: "DELETE",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Netzwerkantwort war nicht ok");
        }
        const row = button.closest("tr");
        row.remove(); // Entferne die gesamte Tabellenzeile
    })
    .catch(error => {
        console.error("Es gab ein Problem mit der Fetch-Operation:", error);
    });
}