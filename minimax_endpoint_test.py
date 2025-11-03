"""
Test different MiniMax API endpoints and header combinations
"""
import requests
import json
import os
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
print(f"✓ API Key loaded: {len(api_key)} chars\n")

# Test different endpoint URLs and header combinations
test_configs = [
    {
        "name": "OpenAI-compatible endpoint with Bearer",
        "url": "https://api.minimax.io/v1/chat/completions",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    },
    {
        "name": "OpenAI-compatible endpoint without Bearer",
        "url": "https://api.minimax.io/v1/chat/completions",
        "headers": {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
    },
    {
        "name": "ChatCompletion v2 endpoint with Bearer",
        "url": "https://api.minimax.io/v1/text/chatcompletion_v2",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    },
    {
        "name": "ChatCompletion v2 endpoint without Bearer",
        "url": "https://api.minimax.io/v1/text/chatcompletion_v2",
        "headers": {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
    },
    {
        "name": "GroupID in payload (v2 endpoint)",
        "url": "https://api.minimax.io/v1/text/chatcompletion_v2",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        "extra_payload": {
            "group_id": "1931759578777654182"  # From JWT payload
        }
    }
]

base_payload = {
    "model": "MiniMax-M2",
    "messages": [
        {
            "role": "user",
            "content": "Responde 'Sistema OK' en español"
        }
    ],
    "max_tokens": 30,
    "temperature": 0.1
}

print("="*70)
print("TESTING DIFFERENT ENDPOINT AND HEADER COMBINATIONS")
print("="*70)

for i, config in enumerate(test_configs, 1):
    print(f"\n[Test {i}] {config['name']}")
    print(f"  URL: {config['url']}")
    print(f"  Authorization: {list(config['headers'].values())[0][:70]}...")
    
    payload = {**base_payload}
    if "extra_payload" in config:
        payload.update(config["extra_payload"])
    
    try:
        response = requests.post(
            config["url"],
            headers=config["headers"],
            json=payload,
            timeout=30
        )
        print(f"  Status: {response.status_code}")
        
        try:
            resp_json = response.json()
            
            # Check for success indicators
            if response.status_code == 200:
                if 'choices' in resp_json and resp_json['choices']:
                    print(f"\n  ✅ SUCCESS!")
                    print(f"  Response: {resp_json['choices'][0].get('message', {}).get('content', 'N/A')}")
                    print(f"\n  🎉 WORKING CONFIG FOUND!")
                    print(f"  Endpoint: {config['url']}")
                    print(f"  Headers: {json.dumps(config['headers'], indent=4)}")
                    break
                elif 'base_resp' in resp_json:
                    status_code = resp_json['base_resp'].get('status_code')
                    status_msg = resp_json['base_resp'].get('status_msg')
                    print(f"  ❌ Error: status_code={status_code}, msg={status_msg}")
                else:
                    print(f"  Response preview: {json.dumps(resp_json, indent=2)[:300]}")
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
                print(f"  Response: {response.text[:300]}")
                
        except Exception as e:
            print(f"  ❌ JSON parse error: {e}")
            print(f"  Raw response: {response.text[:300]}")
            
    except Exception as e:
        print(f"  ❌ Request error: {e}")

print("\n" + "="*70)
