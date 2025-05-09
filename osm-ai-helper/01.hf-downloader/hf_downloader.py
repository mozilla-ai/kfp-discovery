import sys
import logging
import argparse
from huggingface_hub import hf_hub_download


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    argparser = argparse.ArgumentParser(description="Download an artifact from Hugging Face Hub.")
    argparser.add_argument(
        "--repo-id",
        type=str,
        required=True,
        help="Repository ID on Hugging Face Hub (e.g., 'username/model_name').",
    )
    argparser.add_argument(
        "--repo-type",
        type=str,
        default="model",
        help="Type of the repository (e.g., 'model', 'dataset').",
    )
    argparser.add_argument(
        "--filename",
        type=str,
        default="model.pt",
        help="Name of the model file to download.",
    )
    argparser.add_argument(
        "--output-dir",
        type=str,
        default="models",
        help="Directory to save the downloaded model.",
    )

    args = argparser.parse_args()
    repo_id = args.repo_id
    repo_type = args.repo_type
    filename = args.filename
    output_dir = args.output_dir

    logger.info(f"Downloading {filename} from Hugging Face Hub. Repo ID: {repo_id}...")

    hf_hub_download(
        "mozilla-ai/swimming-pool-detector",
        filename=filename,
        repo_type=repo_type,
        local_dir=output_dir,
    )

    logger.info("Artifact downloaded successfully.")


if __name__ == "__main__":
    sys.exit(main())
