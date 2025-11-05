## Lire un PDF avec Azure Functions (Python)

Une fonction Azure Functions en Python pour lire et extraire du texte à partir de fichiers PDF, avec des tests simples et une démo visuelle.

## Fonctionnalités

- Extraction de texte depuis un PDF côté serveur (fonction HTTP Azure).
- Exemples de tests unitaires (`test_simple.py`, `test_intelligence.py`).
- Fichiers de configuration prêts pour l'exécution locale (`host.json`, `local.settings.json`).
- Guide de test manuel et démonstration visuelle (`guide_test_manuel.md`, `DEMO_VISUELLE.md`, `DEMONSTRATION_RESULTS.md`).

## Structure du projet

- `function_app.py` : point d'entrée de la fonction Azure Functions (HTTP trigger).
- `requirements.txt` : dépendances Python.
- `host.json` et `local.settings.json` : configuration locale Azure Functions.
- `test_simple.py`, `test_intelligence.py` : tests.
- `DEMO_VISUELLE.md`, `DEMONSTRATION_RESULTS.md`, `guide_test_manuel.md` : documentation de démo.

## Prérequis

- Python 3.10+ (recommandé)
- Azure Functions Core Tools
- Node.js (pour Azure Functions Core Tools) et .NET SDK si requis par votre version d'outils

## Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

## Exécution locale

1. Copier `local.settings.json` (s'il n'existe pas) et ajuster les paramètres si besoin.
2. Lancer l'émulateur Functions :

```bash
func start
```

3. Appeler la fonction HTTP (exemple) :

```bash
curl -X POST "http://localhost:7071/api/read-pdf" ^
  -H "Content-Type: application/pdf" ^
  --data-binary @votre_fichier.pdf
```

Selon l'implémentation de `function_app.py`, vous pouvez aussi envoyer une URL ou un PDF encodé en base64 (voir le code).

## Tests

```bash
pytest -q
```

## Déploiement (rapide)

1. Se connecter :

```bash
az login
```

2. Déployer :

```bash
func azure functionapp publish <NOM_DE_VOTRE_APP>
```

## Configuration

- `local.settings.json` contient les paramètres de développement local. Ne pas le committer avec des secrets.
- Les variables spécifiques (clés, connexions) doivent être ajoutées en tant que paramètres d’application dans Azure.

## Limitations et pistes d’amélioration

- Gérer les PDF scannés (OCR via Azure Cognitive Services ou Tesseract).
- Support des gros fichiers via stockage temporaire (Azure Blob Storage) au lieu d’upload direct.
- Validation des entrées et gestion d’erreurs plus détaillées.

## Licence

Ce projet est distribué sous licence MIT. Voir `LICENSE` si présent ou ajouter un fichier de licence.


