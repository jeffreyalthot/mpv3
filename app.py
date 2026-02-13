import argparse
from pathlib import Path

import requests
from moviepy.editor import AudioFileClip, VideoFileClip

from src.config import load_settings


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_script(topic: str, duration: int, settings) -> str:
    if not settings.openai_api_key:
        return (
            f"Sujet: {topic}\n\n"
            f"Script offline de secours pour {duration} secondes."
        )

    url = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.openai_model,
        "messages": [
            {
                "role": "system",
                "content": "Tu écris des scripts courts, dynamiques et viraux en français.",
            },
            {
                "role": "user",
                "content": f"Écris un script voix-off de {duration} secondes sur: {topic}",
            },
        ],
        "temperature": 0.7,
    }
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def generate_tts(script: str, settings) -> Path | None:
    if not settings.elevenlabs_api_key or not settings.elevenlabs_voice_id:
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.elevenlabs_voice_id}"
    headers = {
        "xi-api-key": settings.elevenlabs_api_key,
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
    }
    payload = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=120)
    response.raise_for_status()

    out_path = OUTPUT_DIR / "voice.mp3"
    out_path.write_bytes(response.content)
    return out_path


def download_stock_video(query: str, settings) -> Path | None:
    if not settings.pexels_api_key:
        return None

    search_url = "https://api.pexels.com/videos/search"
    params = {"query": query, "per_page": 1, "orientation": "portrait"}
    headers = {"Authorization": settings.pexels_api_key}

    response = requests.get(search_url, params=params, headers=headers, timeout=60)
    response.raise_for_status()
    data = response.json()

    videos = data.get("videos", [])
    if not videos:
        return None

    video_files = videos[0].get("video_files", [])
    if not video_files:
        return None

    video_url = sorted(video_files, key=lambda v: v.get("width", 10_000))[0]["link"]
    video_response = requests.get(video_url, timeout=120)
    video_response.raise_for_status()

    out_path = OUTPUT_DIR / "stock.mp4"
    out_path.write_bytes(video_response.content)
    return out_path


def render_video(stock_video: Path, voice_file: Path) -> Path:
    output_file = OUTPUT_DIR / "final_video.mp4"

    video = VideoFileClip(str(stock_video))
    audio = AudioFileClip(str(voice_file))

    if video.duration > audio.duration:
        video = video.subclip(0, audio.duration)

    final = video.set_audio(audio)
    final.write_videofile(str(output_file), codec="libx264", audio_codec="aac")

    video.close()
    audio.close()
    final.close()

    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MoneyPrinterV2 Android/Pydroid3 sans API IA locale"
    )
    parser.add_argument("--topic", required=True, help="Sujet de la vidéo")
    parser.add_argument("--duration", type=int, default=30, help="Durée cible en secondes")
    args = parser.parse_args()

    settings = load_settings()

    script = generate_script(args.topic, args.duration, settings)
    script_path = OUTPUT_DIR / "script.txt"
    script_path.write_text(script, encoding="utf-8")
    print(f"[OK] Script généré: {script_path}")

    voice_path = generate_tts(script, settings)
    if voice_path:
        print(f"[OK] Voix générée: {voice_path}")
    else:
        print("[INFO] TTS non configuré (ELEVENLABS_* manquants).")

    stock_path = download_stock_video(args.topic, settings)
    if stock_path:
        print(f"[OK] Vidéo stock téléchargée: {stock_path}")
    else:
        print("[INFO] Pexels non configuré (PEXELS_API_KEY manquant) ou aucun résultat.")

    if voice_path and stock_path:
        final = render_video(stock_path, voice_path)
        print(f"[OK] Vidéo finale créée: {final}")
    else:
        print("[INFO] Assemblage vidéo ignoré (audio/vidéo manquant).")


if __name__ == "__main__":
    main()
