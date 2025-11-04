from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import os

# --- Inicializar Flask ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# --- Cargar datos ---
movies = pd.read_csv(os.path.join(BASE_DIR, "data", "movies.csv"))

# --- Extraer año del título si no existe columna 'year' ---
if "year" not in movies.columns:
    movies["year"] = movies["title"].str.extract(r"\((\d{4})\)").astype(float)

# --- RUTA PRINCIPAL ---
@app.route("/")
def index():
    return render_template("index.html")

# --- API DE RECOMENDACIONES ---
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    genre = data.get("genre")
    era = data.get("era")

    recs = movies.copy()

    # --- Filtrar por género ---
    if genre:
        recs = recs[recs["genres"].str.contains(genre, case=False, na=False)]

    # --- Filtrar por época ---
    if era == "Reciente":
        recs = recs[recs["year"] >= 2010]
    elif era == "Clásica":
        recs = recs[recs["year"] < 2010]

    # --- Seleccionamos hasta 6 películas aleatorias ---
    if len(recs) > 0:
        recs = recs.sample(min(6, len(recs)))
    else:
        return jsonify([])  # No hay recomendaciones

    # --- Preparar resultados ---
    resultados = []
    for _, row in recs.iterrows():
        img_file = row["img"] if pd.notna(row["img"]) and row["img"] != "" else "default.jpg"
        img_url = url_for("static", filename=f"images/{img_file}")

        resultados.append({
            "title": row["title"],
            "img": img_url
        })

    return jsonify(resultados)

# --- Ejecutar ---
if __name__ == "__main__":
    app.run(debug=True)
