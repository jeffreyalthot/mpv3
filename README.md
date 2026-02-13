# MoneyPrinterV2 (édition Pydroid 3, sans IA locale)

Cette version est une adaptation minimale orientée **Android + Pydroid 3** :
- aucun serveur IA local,
- aucune API locale de type `http://127.0.0.1:xxxx`,
- uniquement des API cloud (OpenAI-compatible, ElevenLabs, Pexels, etc.).

## Objectif
Créer automatiquement une vidéo courte à partir d'un sujet :
1. génération du script via API LLM cloud,
2. synthèse vocale via API TTS cloud,
3. récupération d'une vidéo stock,
4. assemblage final via MoviePy.

## Installation (Pydroid 3)

Dans le terminal Pydroid 3 :

```bash
pip install -r requirements-pydroid3.txt
```

> Astuce Pydroid: installer le plugin "Pydroid repository plugin" pour faciliter l'installation des dépendances natives (notamment `numpy`).

## Variables d'environnement

Définir les variables suivantes dans Pydroid (ou dans un fichier `.env` chargé manuellement):

- `OPENAI_API_KEY` (obligatoire)
- `OPENAI_BASE_URL` (optionnel, défaut: `https://api.openai.com/v1`)
- `OPENAI_MODEL` (optionnel, défaut: `gpt-4o-mini`)
- `ELEVENLABS_API_KEY` (optionnel)
- `ELEVENLABS_VOICE_ID` (optionnel)
- `PEXELS_API_KEY` (optionnel)

## Utilisation

```bash
python app.py --topic "5 astuces productivité" --duration 30
```

Le script crée:
- `output/script.txt`
- `output/voice.mp3` (si TTS configuré)
- `output/stock.mp4` (si Pexels configuré)
- `output/final_video.mp4` (si assets disponibles)

## Notes importantes

- Si une API n'est pas configurée, le pipeline passe en mode dégradé (ex: script uniquement).
- Cette base est volontairement simple pour être robuste sur smartphone.
- **Aucune dépendance à une API IA locale** n'est utilisée.
