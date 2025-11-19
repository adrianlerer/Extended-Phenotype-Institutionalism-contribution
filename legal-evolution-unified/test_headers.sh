#!/bin/bash

echo "Testing different header combinations..."
echo "========================================"
echo

# Test 1: X-API-Key header
echo "[1] X-API-Key header:"
curl -s -X POST https://api.minimax.io/v1/chat/completions \
  -H "X-API-Key: ${MINIMAX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}' | jq -r '.base_resp.status_msg // .choices[0].message.content // "ERROR"'

echo

# Test 2: api-key header (lowercase)
echo "[2] api-key header:"
curl -s -X POST https://api.minimax.io/v1/chat/completions \
  -H "api-key: ${MINIMAX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}' | jq -r '.base_resp.status_msg // .choices[0].message.content // "ERROR"'

echo

# Test 3: MiniMax-API-Key header
echo "[3] MiniMax-API-Key header:"
curl -s -X POST https://api.minimax.io/v1/chat/completions \
  -H "MiniMax-API-Key: ${MINIMAX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}' | jq -r '.base_resp.status_msg // .choices[0].message.content // "ERROR"'

