#!/usr/bin/env python3
"""
Example script showing how to use the Image Generation Service.

This is a simple example to help you get started.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.image_generation_service import ImageGenerationService


def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    # Initialize the service
    service = ImageGenerationService(
        db_host=os.getenv('DB_HOST', 'localhost'),
        db_user=os.getenv('DB_USER', 'root'),
        db_password=os.getenv('DB_PASSWORD', 'password'),
        db_name='PMP_Backend',
        gcp_project_id=os.getenv('GCP_PROJECT_ID'),
        gcp_bucket_name='kalshi-vs-ai'
    )
    
    # Process all articles (or limit with max_articles parameter)
    service.run(max_articles=5)  # Process only 5 articles for testing


def example_fetch_only():
    """Example: Just fetch articles without processing."""
    print("\n" + "=" * 60)
    print("Example 2: Fetch Articles Only")
    print("=" * 60)
    
    service = ImageGenerationService(
        db_host=os.getenv('DB_HOST', 'localhost'),
        db_user=os.getenv('DB_USER', 'root'),
        db_password=os.getenv('DB_PASSWORD', 'password'),
        db_name='PMP_Backend',
        gcp_project_id=os.getenv('GCP_PROJECT_ID')
    )
    
    # Just fetch articles
    articles = service.fetch_articles_without_images()
    
    print(f"\nFound {len(articles)} articles without images:")
    for i, article in enumerate(articles[:5], 1):  # Show first 5
        print(f"\n{i}. {article['headline'][:80]}...")
        print(f"   Category: {article['category']}")
        print(f"   Event: {article['title'][:60]}...")


def example_process_single():
    """Example: Process a single article."""
    print("\n" + "=" * 60)
    print("Example 3: Process Single Article")
    print("=" * 60)
    
    service = ImageGenerationService(
        db_host=os.getenv('DB_HOST', 'localhost'),
        db_user=os.getenv('DB_USER', 'root'),
        db_password=os.getenv('DB_PASSWORD', 'password'),
        db_name='PMP_Backend',
        gcp_project_id=os.getenv('GCP_PROJECT_ID')
    )
    
    # Fetch articles
    articles = service.fetch_articles_without_images()
    
    if articles:
        print(f"\nProcessing first article: {articles[0]['headline'][:60]}...")
        success = service.process_article(articles[0])
        
        if success:
            print("✓ Successfully processed article!")
        else:
            print("✗ Failed to process article")
    else:
        print("No articles found without images")


def example_custom_configuration():
    """Example: Custom configuration."""
    print("\n" + "=" * 60)
    print("Example 4: Custom Configuration")
    print("=" * 60)
    
    # You can customize various parameters
    service = ImageGenerationService(
        db_host='your-db-host.com',
        db_user='your-username',
        db_password='your-password',
        db_name='PMP_Backend',
        gcp_project_id='your-gcp-project',
        gcp_bucket_name='kalshi-vs-ai',
        gcp_region='us-central1'  # or 'us-east1', 'europe-west1', etc.
    )
    
    print("Service configured with custom settings")
    print(f"Bucket: {service.bucket_name}")
    print(f"Region: {service.gcp_region}")


def check_environment():
    """Check if environment variables are set."""
    print("=" * 60)
    print("Environment Check")
    print("=" * 60)
    
    required_vars = {
        'DB_HOST': 'Database host',
        'DB_USER': 'Database username',
        'DB_PASSWORD': 'Database password',
        'GCP_PROJECT_ID': 'GCP Project ID',
        'GOOGLE_APPLICATION_CREDENTIALS': 'Path to GCP service account key'
    }
    
    missing = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'PASSWORD' in var or 'CREDENTIALS' in var:
                display_value = '***' + value[-4:] if len(value) > 4 else '***'
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: Not set ({description})")
            missing.append(var)
    
    if missing:
        print(f"\n⚠ Missing {len(missing)} required environment variable(s)")
        print("\nSet them using:")
        for var in missing:
            print(f"  export {var}=your-value")
        return False
    else:
        print("\n✓ All required environment variables are set!")
        return True


def main():
    """Run examples."""
    print("\n" + "=" * 60)
    print("Kalshi Image Generation Service - Examples")
    print("=" * 60)
    
    # Check environment first
    if not check_environment():
        print("\n⚠ Please set required environment variables before running examples")
        print("\nExample:")
        print("  export DB_HOST=localhost")
        print("  export DB_USER=root")
        print("  export DB_PASSWORD=password")
        print("  export GCP_PROJECT_ID=my-project")
        print("  export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json")
        return
    
    # Ask user which example to run
    print("\nWhich example would you like to run?")
    print("1. Basic usage (process 5 articles)")
    print("2. Fetch articles only (no processing)")
    print("3. Process single article")
    print("4. Show custom configuration")
    print("5. Run all examples")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-5): ").strip()
    
    try:
        if choice == '1':
            example_basic_usage()
        elif choice == '2':
            example_fetch_only()
        elif choice == '3':
            example_process_single()
        elif choice == '4':
            example_custom_configuration()
        elif choice == '5':
            example_fetch_only()
            example_process_single()
        elif choice == '0':
            print("Exiting...")
        else:
            print("Invalid choice")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. Database is accessible")
        print("  2. GCP credentials are valid")
        print("  3. Required APIs are enabled")
        print("  4. Bucket 'kalshi-vs-ai' exists")


if __name__ == "__main__":
    main()
