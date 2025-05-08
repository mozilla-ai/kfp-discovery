import sys
import logging
import argparse

from document_to_podcast.preprocessing import DATA_CLEANERS, DATA_LOADERS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    argparser = argparse.ArgumentParser(description="Load and process documents.")
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
        "--file-type",
        type=str,
        choices=[".txt", ".pdf", ".docx", ".html", ".markdown"],
        required=True,
        help="Type of the input document file.",
    )

    args = argparser.parse_args()

    input_path = args.input
    output_path = args.output

    suffix = args.file_type
    data_loader = DATA_LOADERS.get(suffix, None)
    if data_loader is None:
        raise ValueError(f"No data loader available for file type: {suffix}")
    
    data_cleaner = DATA_CLEANERS.get(suffix, None)
    if data_cleaner is None:
        raise ValueError(f"No data cleaner available for file type: {suffix}")
    
    logger.info(f"Loading document from {input_path} using loader...")
    document = data_loader(input_path)
    logger.info(f"Loaded document from {input_path}")
    logger.info(f"Document content: {document[:100]}...")
    logger.info(f"Number of characters in document: {len(document)}")

    logger.info("Extracting raw text from the documnt...")
    cleaned_document = data_cleaner(document)
    logger.info(f"Cleaned document content: {cleaned_document[:100]}...")
    logger.info(f"Number of characters in cleaned document: {len(cleaned_document)}")

    logger.info(f"Saving cleaned document to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_document)

    logger.info(f"Saved cleaned document to {output_path}")


if __name__ == "__main__":
    sys.exit(main())
