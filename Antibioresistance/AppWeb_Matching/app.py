from flask import Flask, render_template, request
import json
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('accueil.html')

@app.route('/recherche')
def recherche():
    return render_template('recherche.html')

@app.route('/result', methods=['POST'])     
def result():
    # Charger le fichier JSON
    with open('card.json', 'r') as f:
        data = json.load(f)
    
    if 'file' in request.files:
        # Si un fichier est téléchargé, lire son contenu et nettoyer la séquence
        file = request.files['file']
        text = file.read().decode('utf-8').split('\n', 1)[1].replace('\n', '')
        text = re.sub(r'[^ATCG]', '', text)  # supprimer tous les caractères non ATCG
    elif 'text' in request.form:
        # Si un texte est soumis, récupérer la séquence à partir du texte
        text = request.form.get('text')
    else:
        # Si ni un fichier ni un texte ne sont soumis, retourner une erreur
        return 'Error: no file or text submitted'

    # Stocker les données à afficher dans la variable result
    result = []
    for protein_id, protein_data in data.items():
        if 'model_sequences' in protein_data:
            name = protein_data['model_name']
            ARO_description = protein_data['ARO_description']
            sequence_lines = protein_data['model_sequences']['sequence']['test']['dna_sequence']['sequence'].split('\n')
            # Concaténer toutes les lignes de la séquence en une seule chaîne
            sequence = ''.join(sequence_lines)
            NCBI_taxonomy_name = protein_data['model_sequences']['sequence']['test']['NCBI_taxonomy']['NCBI_taxonomy_name']
            identity = 0
            for i in range(min(len(text), len(sequence))):
                if text[i] == sequence[i]:
                    identity += 1
            percent_identity = round(100 * identity / len(text), 2)
            
            result.append((name, NCBI_taxonomy_name, percent_identity, ARO_description, sequence))

    # trier les résultats par ordre décroissant de pourcentage d'identité
    result.sort(key=lambda x: x[2], reverse=True)
    
    # Passer les données à afficher à render_template()
    return render_template('result.html', result=result)



if __name__ == "__main__":
    app.run(debug=True)
