# app.py

from flask import Flask, request, jsonify, render_template
from rag import RAG
import os

app = Flask(__name__)

# Initialiser le système RAG une seule fois au démarrage de l'application
rag_system = RAG()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('query')
        top_k = request.form.get('top_k', 5)
        
        # Validation des entrées
        if not query:
            return render_template('index.html', error="Aucune requête fournie.", answer=None)
        
        try:
            top_k = int(top_k)
            if top_k < 1 or top_k > 20:
                raise ValueError
        except ValueError:
            return render_template('index.html', error="Le nombre de documents à récupérer doit être un entier entre 1 et 20.", answer=None)
        
        try:
            answer = rag_system.rag(query, top_k)
            return render_template('index.html', answer=answer, error=None)
        except Exception as e:
            return render_template('index.html', error=str(e), answer=None)
    
    # Si méthode GET, afficher le formulaire sans réponse
    return render_template('index.html', answer=None, error=None)

@app.route('/api/query', methods=['POST'])
def handle_query_api():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Aucune requête fournie.'}), 400

    query = data['query']
    top_k = data.get('top_k', 5)  # Nombre de documents à récupérer, par défaut 5

    try:
        top_k = int(top_k)
        if top_k < 1 or top_k > 20:
            raise ValueError
    except ValueError:
        return jsonify({'error': 'Le nombre de documents à récupérer doit être un entier entre 1 et 20.'}), 400

    try:
        answer = rag_system.rag(query, top_k)
        return jsonify({'answer': answer}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5010))
    app.run(host='0.0.0.0', port=port, debug=True)
