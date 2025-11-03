#!/bin/bash

echo "================================================"
echo "TEST: Alternative API Key (SCM-Legal)"
echo "================================================"
echo
echo "Por favor provee el key COMPLETO de 'SCM-Legal'"
echo "(Si no lo tienes guardado, crea uno nuevo desde la plataforma)"
echo
read -p "Pega el API key completo aquí: " NEW_KEY

if [ -z "$NEW_KEY" ]; then
    echo "❌ No se proveyó ningún key"
    exit 1
fi

echo
echo "Testing with provided key..."
echo

curl -s -X POST https://api.minimax.io/v1/chat/completions \
  -H "Authorization: Bearer $NEW_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M2","messages":[{"role":"user","content":"Responde OK en español"}],"max_tokens":10}' \
  | python3 -m json.tool

