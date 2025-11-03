"""
Direct HTTP test for MiniMax API authentication
Testing different Authorization header formats
"""
import requests
import json
import os
from pathlib import Path

# Load API key from .env
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

api_key = os.environ.get("MINIMAX_API_KEY")
print(f"✓ API Key loaded: {len(api_key)} chars")
print(f"  Starts with: {api_key[:50]}...")

# Test different header formats
test_formats = [
    {"Authorization": f"Bearer {api_key}"},
    {"Authorization": api_key},
    {"authorization": f"Bearer {api_key}"},
    {"authorization": api_key},
]

url = "https://api.minimax.io/v1/text/chatcompletion_v2"

payload = {
    "model": "MiniMax-M2",
    "messages": [
        {
            "role": "user",
            "content": "Di 'Sistema funcionando' en español"
        }
    ],
    "max_tokens": 50,
    "temperature": 0.1
}

print("\n" + "="*70)
print("TESTING DIFFERENT AUTHORIZATION HEADER FORMATS")
print("="*70)

for i, headers in enumerate(test_formats, 1):
    print(f"\n[Test {i}] Headers: {list(headers.keys())[0]} = {list(headers.values())[0][:60]}...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"  Status Code: {response.status_code}")
        
        try:
            resp_json = response.json()
            print(f"  Response: {json.dumps(resp_json, indent=2)[:500]}")
            
            # Check if successful
            if response.status_code == 200 and 'choices' in resp_json:
                print("\n✅ SUCCESS! This header format works!")
                print(f"   Working format: {list(headers.keys())[0]}: {list(headers.values())[0][:60]}...")
                if resp_json.get('choices'):
                    print(f"   Response text: {resp_json['choices'][0].get('message', {}).get('content', 'N/A')}")
                break
        except:
            print(f"  Raw response: {response.text[:500]}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "="*70)
