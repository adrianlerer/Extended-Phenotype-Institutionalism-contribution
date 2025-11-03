"""
Test MiniMax API with GroupID in request body
Based on official SDK patterns
"""
import requests
import json
import os
import base64
from pathlib import Path

# Load API key
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

api_key = os.environ.get("MINIMAX_API_KEY")

# Extract GroupID from JWT
parts = api_key.split('.')
payload_bytes = parts[1] + '=' * (4 - len(parts[1]) % 4)
payload = json.loads(base64.urlsafe_b64decode(payload_bytes))
group_id = payload.get('GroupID')

print(f"✓ API Key loaded: {len(api_key)} chars")
print(f"✓ GroupID extracted from JWT: {group_id}\n")

# Test configurations with GroupID in different places
test_configs = [
    {
        "name": "GroupID in request body (OpenAI endpoint)",
        "url": "https://api.minimax.io/v1/chat/completions",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        "payload": {
            "model": "MiniMax-M2",
            "messages": [{"role": "user", "content": "Responde 'Sistema OK' en español"}],
            "group_id": group_id,
            "max_tokens": 30
        }
    },
    {
        "name": "GroupID as query parameter",
        "url": f"https://api.minimax.io/v1/chat/completions?GroupId={group_id}",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        "payload": {
            "model": "MiniMax-M2",
            "messages": [{"role": "user", "content": "Responde 'Sistema OK' en español"}],
            "max_tokens": 30
        }
    },
    {
        "name": "GroupID in header",
        "url": "https://api.minimax.io/v1/chat/completions",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "GroupId": group_id
        },
        "payload": {
            "model": "MiniMax-M2",
            "messages": [{"role": "user", "content": "Responde 'Sistema OK' en español"}],
            "max_tokens": 30
        }
    },
    {
        "name": "MiniMax native endpoint with group_id in body",
        "url": "https://api.minimax.io/v1/text/chatcompletion_v2",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        "payload": {
            "model": "MiniMax-M2",
            "messages": [{"role": "user", "content": "Responde 'Sistema OK' en español"}],
            "group_id": group_id,
            "max_tokens": 30
        }
    },
]

print("="*70)
print("TESTING GROUPID AUTHENTICATION APPROACHES")
print("="*70)

for i, config in enumerate(test_configs, 1):
    print(f"\n[Test {i}] {config['name']}")
    print(f"  URL: {config['url'][:80]}")
    
    try:
        response = requests.post(
            config["url"],
            headers=config["headers"],
            json=config["payload"],
            timeout=30
        )
        print(f"  Status: {response.status_code}")
        
        try:
            resp_json = response.json()
            
            # Check for success
            if 'choices' in resp_json and resp_json.get('choices'):
                print(f"\n  ✅✅✅ SUCCESS! ✅✅✅")
                print(f"  Response: {resp_json['choices'][0].get('message', {}).get('content', 'N/A')}")
                print(f"\n  🎉 WORKING CONFIGURATION FOUND! 🎉")
                print(f"\n  Endpoint: {config['url']}")
                print(f"  Headers: {json.dumps(config['headers'], indent=4)}")
                print(f"  Payload structure: {json.dumps({k: '...' if k != 'group_id' else v for k, v in config['payload'].items()}, indent=4)}")
                break
            elif 'base_resp' in resp_json:
                status_code = resp_json['base_resp'].get('status_code')
                status_msg = resp_json['base_resp'].get('status_msg')
                print(f"  ❌ Error: status_code={status_code}")
                print(f"     Message: {status_msg}")
            else:
                print(f"  Response: {json.dumps(resp_json, indent=2)[:400]}")
                
        except Exception as e:
            print(f"  ❌ JSON error: {e}")
            print(f"  Raw: {response.text[:200]}")
            
    except Exception as e:
        print(f"  ❌ Request error: {e}")

print("\n" + "="*70)
