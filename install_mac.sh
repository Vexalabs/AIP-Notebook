#!/bin/bash
# ML Model Builder - Mac/Linux Installer

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  ML Model Builder - Mac Installer${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# 1. Check Prerequisites
echo -e "${CYAN}[1/5] Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    echo "Please install it from https://python.org or run: brew install python"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed.${NC}"
    echo "Please install it from https://nodejs.org or run: brew install node"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites found${NC}"

# 2. Setup Directory
INSTALL_DIR="$HOME/MLModelBuilder"
echo -e "${CYAN}[2/5] Creating installation directory at $INSTALL_DIR...${NC}"

if [ -d "$INSTALL_DIR" ]; then
    echo "Removing existing installation..."
    rm -rf "$INSTALL_DIR"
fi
mkdir -p "$INSTALL_DIR"

# 3. Copy Files
echo -e "${CYAN}[3/5] Copying files...${NC}"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy all files except installer scripts and dist
rsync -av --progress "$SOURCE_DIR/" "$INSTALL_DIR/" \
    --exclude ".git" \
    --exclude "node_modules" \
    --exclude "venv" \
    --exclude "__pycache__" \
    --exclude "dist" \
    --exclude "*.bat" \
    --exclude "*.ps1" \
    --exclude "*.exe" > /dev/null

echo -e "${GREEN}✓ Files copied${NC}"

# 4. Install Dependencies
echo -e "${CYAN}[4/5] Installing dependencies...${NC}"
cd "$INSTALL_DIR"

# Setup Python venv
echo "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip > /dev/null
pip install -r backend/requirements.txt > /dev/null

# Setup Frontend
echo "Setting up Frontend..."
cd frontend
npm install > /dev/null
cd ..

# 5. Create Launcher
echo -e "${CYAN}[5/5] Creating launcher...${NC}"

# Create start.command (double-clickable on Mac)
cat > "$INSTALL_DIR/start.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

echo "Starting ML Model Builder..."
source venv/bin/activate

# Start Backend
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Start Frontend
cd frontend
npm run dev -- --port 3000 &
FRONTEND_PID=$!
cd ..

echo "Services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

# Wait a moment then open browser
sleep 3
open "http://localhost:3000"

# Handle shutdown
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM

echo "Press CTRL+C to stop..."
wait
EOF

chmod +x "$INSTALL_DIR/start.command"

# Create Desktop Shortcut (Symbolic Link)
ln -sf "$INSTALL_DIR/start.command" "$HOME/Desktop/ML Model Builder.command"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "You can now launch the app from your Desktop:"
echo "Double-click 'ML Model Builder.command'"
echo ""
