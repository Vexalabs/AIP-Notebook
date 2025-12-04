#!/bin/bash
# Test script for auto-update endpoints

echo "========================================="
echo "  Auto-Update System - Test Script"
echo "========================================="
echo ""

BASE_URL="http://localhost:8000"

echo "1. Testing current version endpoint..."
echo "   GET /api/updates/current-version"
curl -s "$BASE_URL/api/updates/current-version" | python3 -m json.tool
echo ""

echo "2. Testing update check endpoint..."
echo "   GET /api/updates/check"
curl -s "$BASE_URL/api/updates/check" | python3 -m json.tool
echo ""

echo "3. Testing validation endpoint..."
echo "   GET /api/updates/validate"
curl -s "$BASE_URL/api/updates/validate" | python3 -m json.tool
echo ""

echo "4. Testing status endpoint..."
echo "   GET /api/updates/status"
curl -s "$BASE_URL/api/updates/status" | python3 -m json.tool
echo ""

echo "========================================="
echo "  Test Complete!"
echo "========================================="
echo ""
echo "If all endpoints returned JSON responses, the backend is working correctly."
echo ""
echo "To test the full update flow:"
echo "  1. Create a test release on GitHub (v1.0.1)"
echo "  2. Open http://localhost:3000 in your browser"
echo "  3. Click 'Update Now' when the banner appears"
echo "  4. Watch the progress messages"
echo ""
