#!/bin/bash
curl -X POST http://localhost:8000/api/submission/submit \
  -H 'Content-Type: application/json' \
  -d '{"commit_message": "Add test model", "description": "Test submission"}'
