"""
Image Generation Service for Kalshi Articles

This service:
1. Queries the database for articles without images
2. Generates images using Google's Vertex AI Imagen
3. Uploads images to GCP Storage bucket 'kalshi-vs-ai'
4. Updates the database with the image URLs
"""

import os
import io
from typing import List, Dict, Optional
from pathlib import Path
from google.cloud import storage
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from datetime import datetime
import logging

# Import database service
try:
    from .database import DatabaseService
except ImportError:
    from database import DatabaseService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageGenerationService:
    """Service for generating and storing images for Kalshi articles."""
    
    def __init__(
        self,
        db_host: Optional[str] = None,
        db_user: Optional[str] = None,
        db_password: Optional[str] = None,
        db_name: str = "PMP_Backend",
        gcp_project_id: Optional[str] = None,
        gcp_bucket_name: str = "kalshi-vs-ai",
        gcp_region: str = "us-central1",
        use_config: bool = True
    ):
        """
        Initialize the Image Generation Service.
        
        Args:
            db_host: Database host address (optional if using config)
            db_user: Database username (optional if using config)
            db_password: Database password (optional if using config)
            db_name: Database name (default: PMP_Backend)
            gcp_project_id: GCP Project ID for Vertex AI
            gcp_bucket_name: GCS bucket name (default: kalshi-vs-ai)
            gcp_region: GCP region (default: us-central1)
            use_config: Whether to use config system for credentials (default: True)
        """
        # Initialize database service
        self.db_service = DatabaseService(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            use_config=use_config
        )
        
        self.bucket_name = gcp_bucket_name
        self.gcp_project_id = gcp_project_id
        self.gcp_region = gcp_region
        
        # Initialize GCP clients
        self._init_gcp_clients()
        
    def _init_gcp_clients(self):
        """Initialize Google Cloud Platform clients."""
        try:
            # Initialize Vertex AI
            if self.gcp_project_id:
                vertexai.init(project=self.gcp_project_id, location=self.gcp_region)
                logger.info(f"Initialized Vertex AI for project {self.gcp_project_id}")
            else:
                logger.warning("GCP Project ID not provided, using default credentials")
                vertexai.init(location=self.gcp_region)
            
            # Initialize Storage client
            self.storage_client = storage.Client(project=self.gcp_project_id)
            self.bucket = self.storage_client.bucket(self.bucket_name)
            logger.info(f"Initialized GCS client for bucket {self.bucket_name}")
            
            # Initialize Image Generation Model
            self.image_model = ImageGenerationModel.from_pretrained("imagegeneration@006")
            logger.info("Initialized Vertex AI Image Generation Model")
            
        except Exception as e:
            logger.error(f"Failed to initialize GCP clients: {e}")
            raise
    
    def fetch_articles_without_images(self) -> List[Dict]:
        """
        Fetch articles that don't have images from the database.
        
        Returns:
            List of dictionaries containing article data
        """
        query = """
        SELECT 
            eve.title, 
            eve.category, 
            art.headline, 
            art.article_content,
            art.event_ticker,
            art.id as article_id
        FROM PMP_Backend.kalshi_events as eve
        LEFT JOIN PMP_Backend.kalshi_markets as mar
            ON eve.event_ticker = mar.ticker
        LEFT JOIN PMP_Backend.kalshi_series as ser
            ON eve.event_ticker = ser.ticker
        INNER JOIN PMP_Backend.kalshi_articles as art
            ON eve.event_ticker = art.event_ticker
        WHERE art.image_url IS NULL
        """
        
        try:
            with self.db_service.get_cursor(dictionary=True) as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                logger.info(f"Found {len(results)} articles without images")
                return results
        except Exception as e:
            logger.error(f"Error fetching articles: {e}")
            raise
    
    def generate_image(self, headline: str, title: str, category: str) -> bytes:
        """
        Generate an image using Vertex AI Imagen based on article content.
        
        Args:
            headline: Article headline
            title: Event title
            category: Event category
            
        Returns:
            Image bytes
        """
        try:
            # Create a detailed prompt for image generation
            prompt = f"""
            Create a professional, visually appealing image for a news article about:
            Category: {category}
            Title: {title}
            Headline: {headline}
            
            Style: Modern, clean, professional news illustration. 
            No text in the image. High quality, suitable for article header.
            """
            
            logger.info(f"Generating image for: {headline[:50]}...")
            
            # Generate image using Vertex AI
            response = self.image_model.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="16:9",  # Good for article headers
                safety_filter_level="block_some",
                person_generation="allow_adult"
            )
            
            # Get the first generated image
            if response.images:
                image = response.images[0]
                # Convert to bytes
                image_bytes = image._pil_image.tobytes()
                
                # Save as PNG format
                img_byte_arr = io.BytesIO()
                image._pil_image.save(img_byte_arr, format='PNG')
                image_bytes = img_byte_arr.getvalue()
                
                logger.info("Image generated successfully")
                return image_bytes
            else:
                raise Exception("No images generated")
                
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise
    
    def upload_to_gcs(self, image_bytes: bytes, filename: str) -> str:
        """
        Upload image to Google Cloud Storage.
        
        Args:
            image_bytes: Image data as bytes
            filename: Filename for the image
            
        Returns:
            Public URL of the uploaded image
        """
        try:
            # Create blob with timestamp to ensure uniqueness
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            blob_name = f"kalshi_articles/{timestamp}_{filename}.png"
            blob = self.bucket.blob(blob_name)
            
            # Upload with content type
            blob.upload_from_string(
                image_bytes,
                content_type='image/png'
            )
            
            # Make the blob publicly accessible
            blob.make_public()
            
            # Get public URL
            public_url = blob.public_url
            logger.info(f"Image uploaded to: {public_url}")
            
            return public_url
            
        except Exception as e:
            logger.error(f"Error uploading to GCS: {e}")
            raise
    
    def update_article_image_url(self, article_id: int, image_url: str):
        """
        Update the article's image_url in the database.
        
        Args:
            article_id: ID of the article to update
            image_url: URL of the uploaded image
        """
        query = """
        UPDATE PMP_Backend.kalshi_articles
        SET image_url = %s
        WHERE id = %s
        """
        
        try:
            with self.db_service.get_cursor() as cursor:
                cursor.execute(query, (image_url, article_id))
                logger.info(f"Updated article {article_id} with image URL")
        except Exception as e:
            logger.error(f"Error updating article: {e}")
            raise
    
    def process_article(self, article: Dict) -> bool:
        """
        Process a single article: generate image, upload, and update DB.
        
        Args:
            article: Dictionary containing article data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Processing article: {article['headline']}")
            
            # Generate image
            image_bytes = self.generate_image(
                headline=article['headline'],
                title=article['title'],
                category=article['category']
            )
            
            # Create filename from headline (sanitized)
            filename = "".join(c if c.isalnum() else "_" for c in article['headline'][:50])
            
            # Upload to GCS
            image_url = self.upload_to_gcs(image_bytes, filename)
            
            # Update database
            self.update_article_image_url(article['article_id'], image_url)
            
            logger.info(f"Successfully processed article {article['article_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process article {article.get('article_id')}: {e}")
            return False
    
    def run(self, max_articles: Optional[int] = None):
        """
        Main execution method: process all articles without images.
        
        Args:
            max_articles: Maximum number of articles to process (None = all)
        """
        logger.info("Starting image generation service...")
        
        # Fetch articles
        articles = self.fetch_articles_without_images()
        
        if not articles:
            logger.info("No articles found without images")
            return
        
        # Limit if specified
        if max_articles:
            articles = articles[:max_articles]
            logger.info(f"Processing {len(articles)} articles (limited to {max_articles})")
        else:
            logger.info(f"Processing {len(articles)} articles")
        
        # Process each article
        success_count = 0
        failure_count = 0
        
        for i, article in enumerate(articles, 1):
            logger.info(f"Processing article {i}/{len(articles)}")
            
            if self.process_article(article):
                success_count += 1
            else:
                failure_count += 1
        
        # Summary
        logger.info("=" * 60)
        logger.info(f"Image generation complete!")
        logger.info(f"Successfully processed: {success_count}")
        logger.info(f"Failed: {failure_count}")
        logger.info(f"Total: {len(articles)}")
        logger.info("=" * 60)


def main():
    """
    Main entry point for running the service as a standalone script.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate images for Kalshi articles')
    parser.add_argument('--db-host', required=True, help='Database host')
    parser.add_argument('--db-user', required=True, help='Database user')
    parser.add_argument('--db-password', required=True, help='Database password')
    parser.add_argument('--db-name', default='PMP_Backend', help='Database name')
    parser.add_argument('--gcp-project', help='GCP Project ID')
    parser.add_argument('--bucket', default='kalshi-vs-ai', help='GCS bucket name')
    parser.add_argument('--max-articles', type=int, help='Maximum articles to process')
    
    args = parser.parse_args()
    
    # Create service instance
    service = ImageGenerationService(
        db_host=args.db_host,
        db_user=args.db_user,
        db_password=args.db_password,
        db_name=args.db_name,
        gcp_project_id=args.gcp_project,
        gcp_bucket_name=args.bucket
    )
    
    # Run the service
    service.run(max_articles=args.max_articles)


if __name__ == "__main__":
    main()
