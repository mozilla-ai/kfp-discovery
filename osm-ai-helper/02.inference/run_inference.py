import os
import sys
import logging
import argparse
from osm_ai_helper.run_inference import run_inference
from osm_ai_helper.export_osm import export_osm


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    argparser = argparse.ArgumentParser(description="Download an artifact from Hugging Face Hub.")
    argparser.add_argument(
        "--model-dir",
        type=str,
        default="models",
        help="Directory to save the downloaded model.",
    )
    argparser.add_argument(
        "--model-name",
        type=str,
        default="model.pt",
        help="Name of the model file to download.",
    )
    argparser.add_argument(
        "--latitude",
        type=float,
        required=True,
        help="Latitude of the location to analyze.",
    )
    argparser.add_argument(
        "--longitude",
        type=float,
        required=True,
        help="Longitude of the location to analyze.",
    )
    argparser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Batch size for inference.",
    )
    argparser.add_argument(
        "--mapbox-token",
        type=str,
        required=True,
        help="Mapbox token for accessing Mapbox services.",
    )
    argparser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save the output results.",
    )

    args = argparser.parse_args()
    model_dir = args.model_dir
    model_name = args.model_name
    latitude = args.latitude
    longitude = args.longitude
    batch_size = args.batch_size
    output_dir = args.output_dir

    os.environ["MAPBOX_TOKEN"] = args.mapbox_token

    logger.info(f"Analyzing location: ({latitude}, {longitude})")

    output_path, _, _, _ = run_inference(
        f"{model_dir}/{model_name}",
        output_dir="results",
        lat_lon=(latitude, longitude),
        margin=2,
        batch_size=batch_size,
    )

    logger.info("Inference completed successfully.")

    logger.info("Exporting results to OSM format...")

    export_osm(
        results_dir=output_path,
        output_dir=output_dir,
        tags={"leisure": "swimming_pool", "access": "private", "location": "outdoor"},
    )

    logger.info("Results exported successfully.")


if __name__ == "__main__":
    sys.exit(main())
