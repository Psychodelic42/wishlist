document.addEventListener("DOMContentLoaded", function () {
    fetch("/get_history")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("history-list");
            tableBody.innerHTML = ""; // Sicherstellen, dass die Tabelle leer startet

            data.forEach(entry => {
                const row = document.createElement("tr");

                // Korrekte Zeichenkettenerstellung mit innerText statt innerHTML für sicheres Einfügen
                const titleCell = document.createElement("td");
                titleCell.textContent = entry.title;

                const yearCell = document.createElement("td");
                yearCell.textContent = entry.year;

                const categoryCell = document.createElement("td");
                categoryCell.textContent = entry.category;

                const notesCell = document.createElement("td");
                notesCell.textContent = entry.notes || ""; // Falls notes leer ist, nichts anzeigen

                row.appendChild(titleCell);
                row.appendChild(yearCell);
                row.appendChild(categoryCell);
                row.appendChild(notesCell);
                
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Fehler beim Laden des Verlaufs:", error));
});
