#--------------CODE BIOPYTHON -------------------------------------------------------------------------------------------------------------------------------------------#



import json
from Bio import SeqIO
from Bio.Align import PairwiseAligner

# Charger le fichier JSON
with open('card.json', 'r') as database:
    data = json.load(database)

# Lire le fichier FASTA et stocker toutes les séquences de celui-ci dans une liste vide.
fasta_sequences = []
for record in SeqIO.parse('genome.fasta', 'fasta'):
    fasta_sequences.append(str(record.seq).lower())

# Initialiser l'aligneur
aligner = PairwiseAligner()

# Comparer chaque séquence du fichier JSON avec toutes les séquences du fichier FASTA
for protein_id, protein_data in data.items():
    if 'model_sequences' in protein_data and 'identifiant' in protein_data['model_sequences']['sequence']:
        # Accéder à la séquence d'acides aminés
        sequence_resistome = (protein_data['model_sequences']['sequence']['identifiant']['dna_sequence']['sequence']).lower()
        nom_resistome = protein_data['model_name']
        # Rechercher les séquences du fichier FASTA qui ont une similarité d'au moins 75%
        for sequence in fasta_sequences:
            # Selection du meilleur alignement obtenu 
            alignment = aligner.align(sequence_resistome, sequence)[0]
            # Calcul du pourcentage d'identité
            similarite = (alignment.score / len(sequence_resistome))*100
            if similarite >= 75:
                print(f"La séquence {sequence_resistome} du resistome {nom_resistome} a une similitude de {similarite:.2f}% avec une séquence dans le fichier FASTA.")
                break
        else:
            print(f"La séquence {sequence_resistome} n'a pas été trouvée dans le fichier FASTA.")
