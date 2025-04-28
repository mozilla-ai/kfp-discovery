import re
import sys
import logging
import argparse

import numpy as np
import soundfile as sf

from document_to_podcast.inference.model_loaders import load_tts_model
from document_to_podcast.inference.text_to_speech import text_to_speech


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    argparser = argparse.ArgumentParser(
        description="Convert text to speech using a pre-trained model."
    )
    argparser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input text file.",
    )
    argparser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output audio file.",
    )
    argparser.add_argument(
        "--voice-profiles",
        type=str,
        nargs=2,
        help=(
            "List containing the two voice profiles to use for the podcast speakers."
            " The first element is the voice profile for the first speaker,"
            " the main host, and the second element is the voice profile for the second speaker."
        ),
    )
    argparser.add_argument(
        "--file-type",
        type=str,
        choices=["WAV", "MP3", "OGG"],
        default="WAV",
        help="Type of the output audio file.",
    )
    argparser.add_argument(
        "--model",
        type=str,
        required=True,
        help="The model to use for generating the podcast script.",
    )

    args = argparser.parse_args()

    # Load the input text file
    with open(args.input, "r") as f:
        podcast_script = f.read()

    speakers = [
        {"id": 1, "voice_profile": args.voice_profiles[0]},
        {"id": 2, "voice_profile": args.voice_profiles[1]},
    ]

    if speakers[0]["voice_profile"][0] != speakers[1]["voice_profile"][0]:
        raise ValueError("Both speakers need to have the same language code.")

    # Get which language is used for generation from the first character of the Kokoro voice profile
    language_code = speakers[0]["voice_profile"][0]

    model = load_tts_model(args.model, **{"lang_code": language_code})

    logger.info("Generating podcast audio...")
    podcast_audio = []
    for line in podcast_script.split("\n"):
        if "Speaker" in line:
            speaker_id = re.search(r"Speaker (\d+)", line).group(1)
            voice_profile = next(
                speaker["voice_profile"]
                for speaker in speakers
                if speaker["id"] == int(speaker_id)
            )
            speech = text_to_speech(
                line.split(f'"Speaker {speaker_id}":')[-1],
                model,
                voice_profile
            )
            podcast_audio.append(speech)

    logger.info("Finalizing podcast audio...")
    sf.write(
        args.output,
        np.concatenate(podcast_audio),
        format=args.file_type,
        samplerate=model.sample_rate,
    )

    logger.info(f"Podcast audio saved to {args.output}")


if __name__ == "__main__":
    sys.exit(main())
