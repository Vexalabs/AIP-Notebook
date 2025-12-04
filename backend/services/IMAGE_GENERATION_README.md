# Kalshi Article Image Generation Service

This service automatically generates images for Kalshi articles that don't have images yet. It uses Google's Vertex AI Imagen model to create professional, visually appealing images based on article content.

## Features

- ✅ Queries database for articles without images
- ✅ Generates high-quality images using Vertex AI Imagen
- ✅ Uploads images to Google Cloud Storage (bucket: `kalshi-vs-ai`)
- ✅ Updates database with image URLs
- ✅ Supports batch processing with configurable limits
- ✅ Comprehensive error handling and logging
- ✅ Dry-run mode for testing

## Prerequisites

### 1. Database Access
You need access to the MySQL database with the following tables:
- `PMP_Backend.kalshi_events`
- `PMP_Backend.kalshi_markets`
- `PMP_Backend.kalshi_series`
- `PMP_Backend.kalshi_articles`

### 2. Google Cloud Platform Setup

#### GCP Project
- A GCP project with billing enabled
- Vertex AI API enabled
- Cloud Storage API enabled

#### GCS Bucket
- Bucket name: `kalshi-vs-ai` (already exists according to requirements)
- Bucket should allow public read access for uploaded images

#### Authentication
Set up authentication using one of these methods:

**Option 1: Service Account (Recommended for production)**
```bash
# Create a service account
gcloud iam service-accounts create kalshi-image-generator \
    --display-name="Kalshi Image Generator"

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:kalshi-image-generator@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:kalshi-image-generator@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

# Create and download key
gcloud iam service-accounts keys create ~/kalshi-sa-key.json \
    --iam-account=kalshi-image-generator@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=~/kalshi-sa-key.json
```

**Option 2: Application Default Credentials (for development)**
```bash
gcloud auth application-default login
```

### 3. Python Dependencies

Install required packages:
```bash
cd backend
pip install -r requirements.txt
```

## Installation

1. **Clone/Navigate to the repository:**
```bash
cd /opt/docker/4C_Predictions/model_builder_env
```

2. **Install dependencies:**
```bash
pip install -r backend/requirements.txt
```

3. **Set up environment variables:**
```bash
# Database credentials
export DB_HOST=your-database-host
export DB_USER=your-database-user
export DB_PASSWORD=your-database-password
export DB_NAME=PMP_Backend

# GCP configuration
export GCP_PROJECT_ID=your-gcp-project-id
export GCS_BUCKET=kalshi-vs-ai
export GCP_REGION=us-central1

# GCP authentication
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

## Usage

### Command Line Interface

The service can be run using the CLI script:

```bash
cd backend/scripts
python generate_images.py
```

### CLI Options

```
usage: generate_images.py [-h] [--db-host DB_HOST] [--db-user DB_USER]
                          [--db-password DB_PASSWORD] [--db-name DB_NAME]
                          [--gcp-project GCP_PROJECT] [--bucket BUCKET]
                          [--region REGION] [--max-articles MAX_ARTICLES]
                          [--dry-run] [--verbose]

options:
  -h, --help            show this help message and exit
  --db-host DB_HOST     Database host (or set DB_HOST env var)
  --db-user DB_USER     Database user (or set DB_USER env var)
  --db-password DB_PASSWORD
                        Database password (or set DB_PASSWORD env var)
  --db-name DB_NAME     Database name (default: PMP_Backend)
  --gcp-project GCP_PROJECT
                        GCP Project ID (or set GCP_PROJECT_ID env var)
  --bucket BUCKET       GCS bucket name (default: kalshi-vs-ai)
  --region REGION       GCP region (default: us-central1)
  --max-articles MAX_ARTICLES
                        Maximum number of articles to process
  --dry-run             Show what would be processed without actually processing
  --verbose             Enable verbose logging
```

### Examples

**1. Dry run to see what would be processed:**
```bash
python generate_images.py --dry-run
```

**2. Process only 5 articles:**
```bash
python generate_images.py --max-articles 5
```

**3. Using command-line arguments instead of environment variables:**
```bash
python generate_images.py \
  --db-host localhost \
  --db-user root \
  --db-password mypassword \
  --gcp-project my-gcp-project \
  --max-articles 10
```

**4. Verbose logging for debugging:**
```bash
python generate_images.py --verbose
```

### Programmatic Usage

You can also use the service programmatically in your Python code:

```python
from services.image_generation_service import ImageGenerationService

# Initialize the service
service = ImageGenerationService(
    db_host='localhost',
    db_user='root',
    db_password='password',
    db_name='PMP_Backend',
    gcp_project_id='my-gcp-project',
    gcp_bucket_name='kalshi-vs-ai',
    gcp_region='us-central1'
)

# Process all articles without images
service.run()

# Or process a limited number
service.run(max_articles=10)

# Or process individual articles
articles = service.fetch_articles_without_images()
for article in articles[:5]:
    service.process_article(article)
```

## How It Works

1. **Query Database**: Fetches articles from the database where `image_url IS NULL`
2. **Generate Image**: For each article, creates a prompt based on:
   - Event title
   - Event category
   - Article headline
3. **Upload to GCS**: Saves the generated image to the `kalshi-vs-ai` bucket
4. **Update Database**: Updates the `kalshi_articles` table with the public image URL

## Database Schema

The service expects the following table structure:

```sql
-- kalshi_articles table
CREATE TABLE kalshi_articles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_ticker VARCHAR(255),
    headline TEXT,
    article_content TEXT,
    image_url VARCHAR(512),  -- This field is updated by the service
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Image Generation Details

- **Model**: Vertex AI Imagen (`imagegeneration@006`)
- **Aspect Ratio**: 16:9 (optimal for article headers)
- **Format**: PNG
- **Style**: Professional, modern news illustration
- **Safety**: Moderate content filtering enabled

## Error Handling

The service includes comprehensive error handling:
- Database connection errors
- Image generation failures
- GCS upload errors
- Individual article failures don't stop the entire batch

Failed articles are logged but don't prevent processing of other articles.

## Logging

The service provides detailed logging:
- INFO: Progress updates and successful operations
- ERROR: Failures and exceptions
- DEBUG: Detailed information (use `--verbose` flag)

## Costs

**Vertex AI Imagen Pricing** (as of 2024):
- ~$0.020 per image generated
- Processing 100 articles ≈ $2.00

**Cloud Storage Pricing**:
- Storage: ~$0.020 per GB/month
- Network egress: Varies by region

## Troubleshooting

### "No module named 'vertexai'"
```bash
pip install google-cloud-aiplatform
```

### "Access Denied" errors
Ensure your service account has the following roles:
- `roles/aiplatform.user`
- `roles/storage.objectAdmin`

### "Bucket not found"
Verify the bucket exists:
```bash
gsutil ls gs://kalshi-vs-ai
```

### Database connection errors
- Check database credentials
- Verify network connectivity
- Ensure database allows connections from your IP

## Maintenance

### Monitoring
Monitor the service execution:
```bash
# Check logs
tail -f /var/log/kalshi-image-gen.log

# Check GCS bucket
gsutil ls gs://kalshi-vs-ai/kalshi_articles/
```

### Cleanup
To remove old images:
```bash
# List images older than 30 days
gsutil ls -l gs://kalshi-vs-ai/kalshi_articles/ | grep "2024-01"

# Delete old images
gsutil -m rm gs://kalshi-vs-ai/kalshi_articles/old_image.png
```

## Future Enhancements

Potential improvements:
- [ ] Support for different image styles/themes
- [ ] Image quality validation
- [ ] Retry logic for failed generations
- [ ] Parallel processing for faster execution
- [ ] Web UI for monitoring and manual triggering
- [ ] Webhook notifications on completion
- [ ] A/B testing different prompts

## Support

For issues or questions:
1. Check the logs for detailed error messages
2. Verify all prerequisites are met
3. Try running with `--dry-run` and `--verbose` flags
4. Check GCP quotas and billing

## License

[Your License Here]
