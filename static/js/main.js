document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("btn_recommend");
    const genre = document.getElementById("genre");
    const intensity = document.getElementById("intensity");
    const era = document.getElementById("era");
    const container = document.getElementById("recs-container");

    btn.addEventListener("click", async () => {
        const g = genre.value;
        const i = intensity.value;
        const e = era.value;

        if (!g || !i || !e) {
            alert("Responde las 3 preguntas para darte una recomendación 🎬");
            return;
        }

        // Limpiar resultados previos
        container.innerHTML = "";

        try {
            const response = await fetch("/recommend", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    genre: g,
                    intensity: i,
                    era: e
                })
            });

            if (!response.ok) throw new Error("Error al obtener recomendaciones");

            const recs = await response.json();

            if (recs.length === 0) {
                container.innerHTML = "<p>No se encontraron recomendaciones 😔</p>";
                return;
            }

            recs.forEach(rec => {
                const card = document.createElement("div");
                card.className = "movie-card";

                const img = document.createElement("img");
                img.src = `/static/images/${rec.img}`; // ✅ Usar 'rec.img'
                img.alt = rec.title;

                const info = document.createElement("div");
                info.className = "movie-info";

                const title = document.createElement("h3");
                title.textContent = rec.title;

                const score = document.createElement("p");
                score.textContent = `Recomendado 🎯`;

                info.appendChild(title);
                info.appendChild(score);
                card.appendChild(img);
                card.appendChild(info);

                container.appendChild(card);
            });

        } catch (err) {
            console.error(err);
            alert("Ocurrió un error al obtener recomendaciones");
        }
    });
});
