# Quick Start Guide: Kalshi Image Generation Service

This guide will help you get the image generation service up and running quickly.

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `mysql-connector-python` - For database connectivity
- `google-cloud-storage` - For uploading images to GCS
- `google-cloud-aiplatform` - For Vertex AI image generation

### Step 2: Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
cp env.template .env
nano .env  # or use your favorite editor
```

Fill in your credentials:
```bash
DB_HOST=your-database-host
DB_USER=your-database-user
DB_PASSWORD=your-database-password
GCP_PROJECT_ID=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### Step 3: Test the Connection (Dry Run)

```bash
cd backend/scripts
python generate_images.py --dry-run
```

This will show you what articles would be processed without actually generating images.

### Step 4: Generate Images!

Process a few articles first to test:
```bash
python generate_images.py --max-articles 5
```

Or process all articles:
```bash
python generate_images.py
```

## 📋 Common Commands

### Using the Python CLI

```bash
# Dry run - see what would be processed
python generate_images.py --dry-run

# Process only 5 articles
python generate_images.py --max-articles 5

# Verbose logging for debugging
python generate_images.py --verbose

# Combine options
python generate_images.py --max-articles 10 --verbose
```

### Using the Shell Script (Linux/Mac)

```bash
# Make executable (first time only)
chmod +x run_image_generation.sh

# Run with default settings
./run_image_generation.sh

# Dry run
./run_image_generation.sh --dry-run

# Process limited articles
./run_image_generation.sh --max-articles 5
```

## 🔧 Troubleshooting

### "No module named 'mysql'"
```bash
pip install mysql-connector-python
```

### "No module named 'vertexai'"
```bash
pip install google-cloud-aiplatform
```

### "Access Denied" to GCS bucket
Make sure your service account has these permissions:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_SA@YOUR_PROJECT.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_SA@YOUR_PROJECT.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

### "Database connection failed"
- Check your database host and credentials
- Ensure the database is accessible from your network
- Verify the database name is correct (default: `PMP_Backend`)

### "Bucket not found"
Verify the bucket exists:
```bash
gsutil ls gs://kalshi-vs-ai
```

If it doesn't exist, create it:
```bash
gsutil mb -p YOUR_PROJECT_ID gs://kalshi-vs-ai
```

## 📊 What Happens

When you run the service:

1. **Connects to Database** - Queries for articles where `image_url IS NULL`
2. **For Each Article:**
   - Generates an image using Vertex AI Imagen
   - Uploads the image to `gs://kalshi-vs-ai/kalshi_articles/`
   - Updates the database with the public image URL
3. **Reports Results** - Shows success/failure count

## 💰 Cost Estimate

- **Vertex AI Imagen**: ~$0.020 per image
- **Cloud Storage**: ~$0.020 per GB/month
- **Example**: 100 articles ≈ $2.00

## 🎯 Best Practices

1. **Start Small**: Use `--max-articles 5` for testing
2. **Use Dry Run**: Always test with `--dry-run` first
3. **Monitor Costs**: Check GCP billing dashboard
4. **Check Logs**: Use `--verbose` for detailed information
5. **Backup Database**: Before running on production data

## 📁 File Structure

```
backend/
├── services/
│   ├── image_generation_service.py  # Main service class
│   └── IMAGE_GENERATION_README.md   # Detailed documentation
├── scripts/
│   ├── generate_images.py           # CLI tool
│   ├── run_image_generation.sh      # Shell wrapper
│   └── example_image_generation.py  # Usage examples
├── env.template                      # Environment template
└── requirements.txt                  # Python dependencies
```

## 🔄 Running Regularly

To run this service regularly (e.g., daily), you can set up a cron job:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 2 AM
0 2 * * * cd /opt/docker/4C_Predictions/model_builder_env/backend/scripts && ./run_image_generation.sh >> /var/log/kalshi-image-gen.log 2>&1
```

## 📚 Next Steps

- Read the full documentation: `backend/services/IMAGE_GENERATION_README.md`
- Check out examples: `python backend/scripts/example_image_generation.py`
- Customize image prompts in `image_generation_service.py`

## 🆘 Need Help?

1. Check the logs for detailed error messages
2. Run with `--verbose` flag
3. Verify all environment variables are set
4. Ensure GCP APIs are enabled:
   - Vertex AI API
   - Cloud Storage API

## ✅ Checklist

Before running in production:

- [ ] Database credentials are correct
- [ ] GCP service account has required permissions
- [ ] Bucket `kalshi-vs-ai` exists and is accessible
- [ ] Vertex AI API is enabled
- [ ] Tested with `--dry-run`
- [ ] Tested with `--max-articles 5`
- [ ] Verified images are uploaded correctly
- [ ] Verified database is updated with URLs

---

**Ready to go?** Run: `python generate_images.py --dry-run`
