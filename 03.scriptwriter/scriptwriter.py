import sys
import logging
import argparse

from document_to_podcast.inference.model_loaders import load_llama_cpp_model
from document_to_podcast.inference.text_to_text import text_to_text_stream


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

PROMPT = """
You are a podcast scriptwriter generating engaging and natural-sounding conversations in JSON format.
The script features the following speakers:
{SPEAKERS}
Instructions:
- Write dynamic, easy-to-follow dialogue.
- Include natural interruptions and interjections.
- Avoid repetitive phrasing between speakers.
- Format output as a JSON conversation.
Example:
{
  "Speaker 1": "Welcome to our podcast! Today, we're exploring...",
  "Speaker 2": "Hi! I'm excited to hear about this. Can you explain...",
  "Speaker 1": "Sure! Imagine it like this...",
  "Speaker 2": "Oh, that's cool! But how does..."
}
Important: Make sure that the output is in valid JSON format,
with double quotes around keys and values, no trailing commas, and opening and closing brackets.
"""


def main():
    argparser = argparse.ArgumentParser(description="Turn documents into podcast scripts.")
    argparser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to the input document file.",
    )
    argparser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to the output document file.",
    )
    argparser.add_argument(
        "--hosts",
        type=str,
        nargs=2,
        default=["Sarah", "Michael"],
        help=(
            "List of two host names. The first element is the name of the main host,"
            " and the second element is the name of the second host."
            " The default is ['Sarah', 'Michael']."
        ),
    )
    argparser.add_argument(
        "--model",
        type=str,
        required=True,
        help="The model to use for generating the podcast script.",
    )

    args = argparser.parse_args()
    input_path = args.input
    output_path = args.output
    hosts = args.hosts
    model = args.model

    logger.info(f"Loading input document from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        document = f.read()

    speakers = [
        {
            "id": 1,
            "name": hosts[0],
            "description": "The main host. She explains topics clearly using anecdotes and analogies, teaching in an engaging and captivating way.",
        },
        {
            "id": 2,
            "name": hosts[1],
            "description": "The co-host. He keeps the conversation on track, asks curious follow-up questions, and reacts with excitement or confusion, often using interjections like hmm or umm.",
        },
    ]
    speakers_str = "\n".join(
        f"Speaker {speaker['id']}. Named {speaker['name']}. {speaker['description']}"
        for speaker in speakers
    )
    logger.info(f"Speakers config: {speakers_str}")

    system_prompt = PROMPT.replace("{SPEAKERS}", speakers_str)
    logger.info(f"System prompt: {system_prompt}")
    model = load_llama_cpp_model(model)

    max_characters = model.n_ctx() * 4
    if len(document) > max_characters:
        logger.warning(
            f"Input text is too big ({len(document)})."
            f" Using only a subset of it ({max_characters})."
        )
        document = document[:max_characters]

    logger.info("Generating podcast script...")
    text = ""
    podcast_script = ""
    for chunk in text_to_text_stream(
        document, model, system_prompt=system_prompt.strip()
    ):
        text += chunk
        if text.endswith("\n") and "Speaker" in text:
            podcast_script += text
            logger.info(f"Generated podcast script chunk: {text[:100]}...")
            text = ""

    logger.info("Finalizing podcast script...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(podcast_script)

    logger.info(f"Saved podcast script to {output_path}")
    logger.info(f"Podcast script content: {podcast_script[:100]}...")


if __name__ == "__main__":
    sys.exit(main())
