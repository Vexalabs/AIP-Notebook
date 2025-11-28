#!/bin/bash
# Test script for ML Model Builder backend

echo "========================================"
echo "  ML Model Builder - API Test"
echo "========================================"
echo ""

BASE_URL="http://localhost:8000"

echo "1. Testing environment status endpoint..."
curl -s "$BASE_URL/api/environment/status" | python3 -m json.tool
echo ""

echo "2. Testing config check endpoint..."
curl -s "$BASE_URL/api/config/check-setup" | python3 -m json.tool
echo ""

echo "3. Testing history submissions endpoint..."
curl -s "$BASE_URL/api/history/submissions" | python3 -m json.tool
echo ""

echo "========================================"
echo "  Test Complete"
echo "========================================"
echo ""
echo "If you see JSON responses above, the backend is working!"
echo ""
echo "To test submission:"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Start the environment"
echo "  3. Create a test file in workspace"
echo "  4. Submit with a commit message"
echo ""
echo "To test restore:"
echo "  1. View submission history in the UI"
echo "  2. Click 'Restore' on any submission"
echo ""
