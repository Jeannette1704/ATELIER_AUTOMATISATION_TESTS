import time
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

# URL de l'API choisie (ZenQuotes pour des citations aléatoires)
API_URL = "https://zenquotes.io/api/random"

@app.route('/')
def home():
    # 1. On commence le chronomètre
    start_time = time.time()
    
    error_message = None
    status_code = None
    response_time = 0
    api_status = "🔴 ÉCHEC"
    quote_text = ""
    quote_author = ""

    try:
        # 2. On lance la requête vers l'API publique
        response = requests.get(API_URL, timeout=5)
        status_code = response.status_code
        
        # 3. On calcule le temps de réponse (en millisecondes)
        response_time = round((time.time() - start_time) * 1000, 2)
        
        # 4. On vérifie les critères de qualité (Le Test)
        if status_code == 200:
            data = response.json()
            # ZenQuotes renvoie une liste avec un dictionnaire [{ "q": "citation", "a": "auteur" }]
            if isinstance(data, list) and len(data) > 0:
                quote_text = data[0].get("q", "")
                quote_author = data[0].get("a", "")
                api_status = "🟢 SUCCÈS"
        else:
            error_message = f"L'API a répondu avec un code {status_code}"

    except requests.exceptions.RequestException as e:
        response_time = round((time.time() - start_time) * 1000, 2)
        error_message = str(e)

    # 5. Interface HTML simple pour exposer les indicateurs de qualité
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Suivi API - QA Engineering</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 600px; margin: auto; }
            h1 { color: #2c3e50; text-align: center; }
            .status { font-size: 1.2em; font-weight: bold; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
            .success { background-color: #d4edda; color: #155724; }
            .danger { background-color: #f8d7da; color: #721c24; }
            .metric { margin: 10px 0; font-size: 1.1em; }
            .quote-box { background: #eef2f7; padding: 15px; border-left: 5px solid #3498db; font-style: italic; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>📊 Tableau de bord API Monitoring</h1>
            
            <div class="status {{ 'success' if api_status == '🟢 SUCCÈS' else 'danger' }}">
                Statut du Test : {{ api_status }}
            </div>
            
            <div class="metric"><strong>🔗 API Testée :</strong> <code>{{ url }}</code></div>
            <div class="metric"><strong>⏱️ Temps de réponse :</strong> {{ response_time }} ms</div>
            <div class="metric"><strong>🗂️ Code HTTP reçu :</strong> {{ status_code if status_code else 'Aucun' }}</div>
            
            {% if error_message %}
                <div class="metric" style="color: red;"><strong>❌ Erreur :</strong> {{ error_message }}</div>
            {% endif %}

            {% if quote_text %}
                <div class="quote-box">
                    <p>"{{ quote_text }}"</p>
                    <small>- {{ quote_author }}</small>
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    """
    
    return render_template_string(
        html_template, 
        url=API_URL, 
        api_status=api_status, 
        response_time=response_time, 
        status_code=status_code, 
        error_message=error_message,
        quote_text=quote_text,
        quote_author=quote_author
    )

if __name__ == '__main__':
    app.run(debug=True)
