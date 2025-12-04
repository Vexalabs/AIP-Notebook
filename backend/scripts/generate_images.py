#!/usr/bin/env python3
"""
CLI tool for generating images for Kalshi articles.

This script provides a command-line interface to the Image Generation Service.
It can read configuration from environment variables or command-line arguments.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.image_generation_service import ImageGenerationService
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_env_or_arg(env_var: str, arg_value: str = None, required: bool = True) -> str:
    """
    Get value from environment variable or command-line argument.
    
    Args:
        env_var: Environment variable name
        arg_value: Command-line argument value
        required: Whether the value is required
        
    Returns:
        The value from arg or env
        
    Raises:
        ValueError if required and not found
    """
    value = arg_value or os.getenv(env_var)
    
    if required and not value:
        raise ValueError(f"Missing required parameter: {env_var}")
    
    return value


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate images for Kalshi articles without images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  DB_HOST          Database host address
  DB_USER          Database username
  DB_PASSWORD      Database password
  DB_NAME          Database name (default: PMP_Backend)
  GCP_PROJECT_ID   Google Cloud Project ID
  GCS_BUCKET       GCS bucket name (default: kalshi-vs-ai)
  GCP_REGION       GCP region (default: us-central1)

Examples:
  # Using environment variables
  export DB_HOST=localhost
  export DB_USER=root
  export DB_PASSWORD=password
  export GCP_PROJECT_ID=my-project
  python generate_images.py

  # Using command-line arguments
  python generate_images.py --db-host localhost --db-user root --db-password password

  # Process only 5 articles
  python generate_images.py --max-articles 5

  # Dry run (show what would be processed)
  python generate_images.py --dry-run
        """
    )
    
    # Database arguments
    parser.add_argument(
        '--db-host',
        help='Database host (or set DB_HOST env var)'
    )
    parser.add_argument(
        '--db-user',
        help='Database user (or set DB_USER env var)'
    )
    parser.add_argument(
        '--db-password',
        help='Database password (or set DB_PASSWORD env var)'
    )
    parser.add_argument(
        '--db-name',
        default=None,
        help='Database name (default: PMP_Backend, or set DB_NAME env var)'
    )
    
    # GCP arguments
    parser.add_argument(
        '--gcp-project',
        help='GCP Project ID (or set GCP_PROJECT_ID env var)'
    )
    parser.add_argument(
        '--bucket',
        default=None,
        help='GCS bucket name (default: kalshi-vs-ai, or set GCS_BUCKET env var)'
    )
    parser.add_argument(
        '--region',
        default=None,
        help='GCP region (default: us-central1, or set GCP_REGION env var)'
    )
    
    # Processing arguments
    parser.add_argument(
        '--max-articles',
        type=int,
        help='Maximum number of articles to process'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be processed without actually processing'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Get configuration from args or environment
        db_host = get_env_or_arg('DB_HOST', args.db_host)
        db_user = get_env_or_arg('DB_USER', args.db_user)
        db_password = get_env_or_arg('DB_PASSWORD', args.db_password)
        db_name = get_env_or_arg('DB_NAME', args.db_name, required=False) or 'PMP_Backend'
        gcp_project = get_env_or_arg('GCP_PROJECT_ID', args.gcp_project, required=False)
        bucket = get_env_or_arg('GCS_BUCKET', args.bucket, required=False) or 'kalshi-vs-ai'
        region = get_env_or_arg('GCP_REGION', args.region, required=False) or 'us-central1'
        
        logger.info("=" * 60)
        logger.info("Kalshi Article Image Generation Service")
        logger.info("=" * 60)
        logger.info(f"Database: {db_name} @ {db_host}")
        logger.info(f"GCP Project: {gcp_project or 'Using default credentials'}")
        logger.info(f"GCS Bucket: {bucket}")
        logger.info(f"Region: {region}")
        if args.max_articles:
            logger.info(f"Max Articles: {args.max_articles}")
        if args.dry_run:
            logger.info("DRY RUN MODE - No changes will be made")
        logger.info("=" * 60)
        
        # Create service instance
        service = ImageGenerationService(
            db_host=db_host,
            db_user=db_user,
            db_password=db_password,
            db_name=db_name,
            gcp_project_id=gcp_project,
            gcp_bucket_name=bucket,
            gcp_region=region
        )
        
        # Dry run mode - just fetch and display
        if args.dry_run:
            articles = service.fetch_articles_without_images()
            if args.max_articles:
                articles = articles[:args.max_articles]
            
            logger.info(f"\nFound {len(articles)} articles without images:")
            for i, article in enumerate(articles, 1):
                logger.info(f"\n{i}. Article ID: {article['article_id']}")
                logger.info(f"   Title: {article['title']}")
                logger.info(f"   Category: {article['category']}")
                logger.info(f"   Headline: {article['headline'][:80]}...")
            
            logger.info(f"\nDry run complete. Run without --dry-run to process these articles.")
            return 0
        
        # Run the service
        service.run(max_articles=args.max_articles)
        
        logger.info("\n✓ Image generation completed successfully!")
        return 0
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("\nPlease provide required parameters via command-line or environment variables.")
        logger.error("Run with --help for more information.")
        return 1
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())
