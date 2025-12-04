#!/bin/bash
# Kalshi Image Generation Service Runner
# This script makes it easy to run the image generation service

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "Kalshi Image Generation Service"
echo "=========================================="

# Check if .env file exists
ENV_FILE="$BACKEND_DIR/.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}✓${NC} Loading environment from $ENV_FILE"
    set -a
    source "$ENV_FILE"
    set +a
else
    echo -e "${YELLOW}⚠${NC} No .env file found at $ENV_FILE"
    echo "  You can create one with your database and GCP credentials"
fi

# Check required environment variables
check_env_var() {
    if [ -z "${!1}" ]; then
        echo -e "${RED}✗${NC} Missing required environment variable: $1"
        return 1
    else
        echo -e "${GREEN}✓${NC} $1 is set"
        return 0
    fi
}

echo ""
echo "Checking environment variables..."
all_set=true

check_env_var "DB_HOST" || all_set=false
check_env_var "DB_USER" || all_set=false
check_env_var "DB_PASSWORD" || all_set=false
check_env_var "GCP_PROJECT_ID" || all_set=false

if [ "$all_set" = false ]; then
    echo ""
    echo -e "${RED}✗${NC} Missing required environment variables"
    echo ""
    echo "Please set them in $ENV_FILE or export them:"
    echo "  export DB_HOST=your-database-host"
    echo "  export DB_USER=your-database-user"
    echo "  export DB_PASSWORD=your-database-password"
    echo "  export GCP_PROJECT_ID=your-gcp-project"
    echo "  export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo ""
echo "Checking Python dependencies..."
python3 -c "import mysql.connector" 2>/dev/null || {
    echo -e "${YELLOW}⚠${NC} mysql-connector-python not installed"
    echo "  Installing dependencies..."
    pip install -r "$BACKEND_DIR/requirements.txt"
}

# Parse command line arguments
DRY_RUN=""
MAX_ARTICLES=""
VERBOSE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --max-articles)
            MAX_ARTICLES="--max-articles $2"
            shift 2
            ;;
        --verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -h|--help)
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run              Show what would be processed without processing"
            echo "  --max-articles N       Process at most N articles"
            echo "  --verbose              Enable verbose logging"
            echo "  -h, --help             Show this help message"
            echo ""
            echo "Environment variables (set in .env or export):"
            echo "  DB_HOST                Database host"
            echo "  DB_USER                Database user"
            echo "  DB_PASSWORD            Database password"
            echo "  DB_NAME                Database name (default: PMP_Backend)"
            echo "  GCP_PROJECT_ID         GCP Project ID"
            echo "  GCS_BUCKET             GCS bucket (default: kalshi-vs-ai)"
            echo "  GOOGLE_APPLICATION_CREDENTIALS  Path to GCP service account key"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}✗${NC} Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run the service
echo ""
echo "=========================================="
echo "Starting Image Generation Service..."
echo "=========================================="
echo ""

cd "$SCRIPT_DIR"
python3 generate_images.py $DRY_RUN $MAX_ARTICLES $VERBOSE

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓${NC} Image generation completed successfully!"
else
    echo ""
    echo -e "${RED}✗${NC} Image generation failed with exit code $exit_code"
fi

exit $exit_code
