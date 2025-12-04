#!/usr/bin/env python3
"""
Test script for database service integration.

This script tests the database service and its integration with the image generation service.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database import DatabaseService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database_service():
    """Test the DatabaseService class."""
    print("=" * 60)
    print("Testing Database Service")
    print("=" * 60)
    
    # Test 1: Initialize from environment variables
    print("\nTest 1: Initialize from environment variables")
    try:
        db_service = DatabaseService(use_config=True)
        print(f"✓ Database service created: {db_service}")
    except Exception as e:
        print(f"✗ Failed to create database service: {e}")
        return False
    
    # Test 2: Test connection
    print("\nTest 2: Test database connection")
    if db_service.test_connection():
        print("✓ Database connection successful")
    else:
        print("✗ Database connection failed")
        return False
    
    # Test 3: Fetch articles (read-only test)
    print("\nTest 3: Fetch articles without images")
    try:
        query = """
        SELECT 
            eve.title, 
            eve.category, 
            art.headline, 
            art.event_ticker,
            art.id as article_id
        FROM PMP_Backend.kalshi_events as eve
        INNER JOIN PMP_Backend.kalshi_articles as art
            ON eve.event_ticker = art.event_ticker
        WHERE art.image_url IS NULL
        LIMIT 5
        """
        
        with db_service.get_cursor(dictionary=True) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            
            print(f"✓ Found {len(results)} articles")
            for i, article in enumerate(results, 1):
                print(f"\n  {i}. {article['headline'][:60]}...")
                print(f"     Category: {article['category']}")
                print(f"     Article ID: {article['article_id']}")
    except Exception as e:
        print(f"✗ Failed to fetch articles: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All database service tests passed!")
    print("=" * 60)
    return True


def test_image_generation_service_integration():
    """Test ImageGenerationService with DatabaseService."""
    print("\n" + "=" * 60)
    print("Testing Image Generation Service Integration")
    print("=" * 60)
    
    try:
        from services.image_generation_service import ImageGenerationService
        
        # Test: Initialize without explicit credentials (should use config/env)
        print("\nInitializing ImageGenerationService...")
        service = ImageGenerationService(use_config=True)
        print("✓ Service initialized successfully")
        
        # Test: Fetch articles
        print("\nFetching articles...")
        articles = service.fetch_articles_without_images()
        print(f"✓ Found {len(articles)} articles without images")
        
        if articles:
            print(f"\nFirst article: {articles[0]['headline'][:60]}...")
        
        print("\n" + "=" * 60)
        print("✓ Integration test passed!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Database Service Test Suite")
    print("=" * 60)
    
    # Check environment
    import os
    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD']
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"\n⚠ Missing environment variables: {', '.join(missing)}")
        print("\nPlease set:")
        for var in missing:
            print(f"  export {var}=your-value")
        print("\nOr create backend/.env file")
        return 1
    
    # Run tests
    success = True
    
    if not test_database_service():
        success = False
    
    if not test_image_generation_service_integration():
        success = False
    
    if success:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
