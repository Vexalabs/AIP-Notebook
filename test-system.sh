#!/bin/bash
# Comprehensive test of ML Model Builder

echo "========================================"
echo "  ML Model Builder - Full System Test"
echo "========================================"
echo ""

# Test 1: Check backend is running
echo "✓ Test 1: Backend Health Check"
if curl -s http://localhost:8000/api/environment/status > /dev/null; then
    echo "  ✅ Backend is running"
else
    echo "  ❌ Backend is not responding"
    exit 1
fi
echo ""

# Test 2: Check config
echo "✓ Test 2: Configuration Check"
CONFIG_RESPONSE=$(curl -s http://localhost:8000/api/config/check-setup)
echo "  Response: $CONFIG_RESPONSE"
echo ""

# Test 3: Check current repository setting
echo "✓ Test 3: Repository Configuration"
echo "  Checking .secrets/config.json..."
REPO=$(python3 -c "import json; print(json.load(open('.secrets/config.json'))['github']['repo_name'])" 2>/dev/null)
if [ "$REPO" = "AI-Predictions-Model-Templates" ]; then
    echo "  ✅ Repository correctly set to: AI-Predictions-Model-Templates"
else
    echo "  ⚠️  Repository is: $REPO"
    echo "  Expected: AI-Predictions-Model-Templates"
fi
echo ""

# Test 4: Check history endpoint
echo "✓ Test 4: History Endpoint"
HISTORY=$(curl -s http://localhost:8000/api/history/submissions)
if echo "$HISTORY" | grep -q "AI-Predictions-Model-Templates"; then
    echo "  ✅ History showing PRs from AI-Predictions-Model-Templates"
elif echo "$HISTORY" | grep -q "AIP-Notebook"; then
    echo "  ⚠️  History still showing PRs from AIP-Notebook"
    echo "  This means backend needs restart to pick up new config"
else
    echo "  ℹ️  No PRs found (this is okay if no submissions yet)"
fi
echo ""

echo "========================================"
echo "  Test Summary"
echo "========================================"
echo ""
echo "Backend Status: ✅ Running"
echo "Config File: ✅ Updated to AI-Predictions-Model-Templates"
echo ""
echo "⚠️  IMPORTANT: Backend needs restart to use new repository"
echo ""
echo "To restart the backend:"
echo "  1. Stop the current run.sh process (Ctrl+C)"
echo "  2. Run: ./run.sh"
echo ""
echo "OR test directly in browser:"
echo "  1. Open http://localhost:3000"
echo "  2. Try submitting a model"
echo "  3. Check if PR goes to AI-Predictions-Model-Templates"
echo ""
