# rag.py

import os
import openai
import faiss
import numpy as np
from dotenv import load_dotenv
import json
import pdfplumber  # Pour l'extraction de texte des PDF
import textwrap    # Pour la segmentation des textes 


# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class RAG:
    def __init__(self, documents_path='documents/', index_path='faiss.index', metadata_path='metadata.json'):
        """
        Initialisation de la classe RAG.

        Args:
            documents_path (str): Chemin vers le dossier contenant les fichiers PDF.
            index_path (str): Chemin vers le fichier d'index FAISS.
            metadata_path (str): Chemin vers le fichier JSON contenant les métadonnées.
        """
        self.documents_path = documents_path
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.embedding_dim = 1536  # Dimension des embeddings OpenAI (ex. text-embedding-ada-002)
        self.index = None
        self.metadata = []

        # Vérifier si l'index et les métadonnées existent déjà
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.load_index()
        else:
            self.build_index()

    def extract_text_from_pdf(self, file_path):
        """
        Extraire le texte d'un fichier PDF en utilisant pdfplumber.

        Args:
            file_path (str): Chemin vers le fichier PDF.

        Returns:
            str: Texte extrait du PDF.
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                pages = pdf.pages
                text = ""
                for page in pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Erreur lors de l'extraction du texte du PDF {file_path}: {e}")
            return ""

    def segment_text(self, text, max_chars=3000):
        """
        Segmenter le texte en passages plus petits pour éviter de dépasser la limite de tokens.

        Args:
            text (str): Texte à segmenter.
            max_chars (int): Nombre maximum de caractères par segment.

        Returns:
            list: Liste de segments de texte.
        """
        ########## Code ###########


        ###########################


        return segments


    def embed_text(self, text):
        """
        Obtenir les embeddings pour un texte donné en utilisant l'API OpenAI.

        Args:
            text (str): Texte à encoder.

        Returns:
            numpy.ndarray or None: Vecteur d'embedding ou None en cas d'erreur.
        """

        ######## Code ##########


        #######################
        return 

    def build_index(self):
        """
        Construire l'index FAISS à partir des documents PDF.
        """
       
        ########### Code ############


        ############################

        return 
                            }


    def load_index(self):
        """
        Charger l'index FAISS et les métadonnées depuis le disque.
        """
        try:
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            print("Index FAISS et métadonnées chargés avec succès.")
        except Exception as e:
            print(f"Erreur lors du chargement de l'index ou des métadonnées: {e}")

    def search(self, query, top_k=5):
        """
        Rechercher les passages les plus pertinents pour une requête donnée.

        Args:
            query (str): Requête de l'utilisateur.
            top_k (int): Nombre de passages à récupérer.

        Returns:
            list: Liste des passages pertinents.
        """
        query_embedding = self.embed_text(query)
        if query_embedding is None:
            return []

        query_embedding = np.expand_dims(query_embedding, axis=0).astype('float32')
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx]['content'])
        return results

    def generate_response(self, query, context):
        """
        Générer une réponse basée sur la requête et le contexte fourni en utilisant GPT-4.

        Args:
            query (str): Question de l'utilisateur.
            context (str): Contexte extrait des passages pertinents.

        Returns:
            str: Réponse générée par GPT-4.
        """
        messages = [
            {"role": "system", "content": "Vous êtes un assistant utile et informatif. Ta réponse doit absolument être basé sur le document fourni. Si tu ne trouves pas de réponse dans le document fourni, réponds que tu n'as pas trouivé de réponse."},
            {"role": "user", "content": f"Contexte:\n{context}\n\nQuestion: {query}\nRéponse:"}
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-2024-08-06",  
                messages=messages,
                max_tokens=150,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse: {e}")
            return "Désolé, je ne peux pas générer de réponse pour le moment."

    def rag(self, query, top_k=5):
        """
        Processus complet RAG : recherche et génération.

        Args:
            query (str): Requête de l'utilisateur.
            top_k (int): Nombre de passages à récupérer.

        Returns:
            str: Réponse générée.
        """
        retrieved_docs = self.search(query, top_k)
        if not retrieved_docs:
            return "Désolé, je n'ai trouvé aucun document pertinent pour votre requête."
        context = "\n".join(retrieved_docs)
        answer = self.generate_response(query, context)
        return answer

if __name__ == "__main__":
    rag_system = RAG()
    réponse = rag_system.rag(user_query)
    print("Réponse générée :", réponse)
