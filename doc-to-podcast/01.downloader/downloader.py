import sys
import logging
import argparse
import requests
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    argparser = argparse.ArgumentParser(description="Download a document given a URL.")
    argparser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL of the document to download.",
    )
    argparser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to save the downloaded document.",
    )
    argparser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the output file if it exists.",
    )

    args = argparser.parse_args()
    url = args.url
    output_path = args.output
    overwrite = args.overwrite

    if Path(output_path).exists() and not overwrite:
        logger.info(f"Output file {output_path} already exists. Use --overwrite to overwrite.")
        raise RuntimeError("Output file already exists.")
    
    if not url.startswith("http://") and not url.startswith("https://"):
        logger.error("Invalid URL. Please provide a valid HTTP or HTTPS URL.")
        return ValueError("Invalid URL.")

    logger.info(f"Downloading document from {url} to {output_path}...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    logger.info("Download complete. Saving to file...")
    with open(f"{output_path}", "wb") as file:
        file.write(response.content)

    logger.info(f"Document downloaded successfully and saved to {output_path}.")


if __name__ == "__main__":
    sys.exit(main())
