"""
Test different MiniMax models and endpoints
"""
import requests
import json
import os

api_key = os.environ.get("MINIMAX_API_KEY")

# Different model names to try
models = [
    "MiniMax-M2",
    "abab6.5s-chat",
    "abab6.5-chat", 
    "abab5.5-chat",
    "abab5.5s-chat",
]

# Different endpoints to try
endpoints = [
    "https://api.minimax.io/v1/chat/completions",
    "https://api.minimax.io/v1/text/chatcompletion_v2",
    "https://api.minimax.io/v1/text/chatcompletion",
]

print("="*70)
print("TESTING DIFFERENT MODELS AND ENDPOINTS")
print("="*70)

for endpoint in endpoints:
    print(f"\n{'='*70}")
    print(f"Endpoint: {endpoint}")
    print('='*70)
    
    for model in models:
        print(f"\n  [Testing] Model: {model}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 10
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
            resp_json = response.json()
            
            # Check for success
            if 'choices' in resp_json and resp_json.get('choices'):
                print(f"    ✅✅✅ SUCCESS!")
                print(f"    Model: {model}")
                print(f"    Endpoint: {endpoint}")
                print(f"    Response: {resp_json['choices'][0].get('message', {}).get('content', '')}")
                print(f"\n{'='*70}")
                print("🎉 WORKING CONFIGURATION FOUND!")
                print(f"Model: {model}")
                print(f"Endpoint: {endpoint}")
                print('='*70)
                exit(0)
            elif 'base_resp' in resp_json:
                status_code = resp_json['base_resp'].get('status_code')
                status_msg = resp_json['base_resp'].get('status_msg', '')
                print(f"    ❌ Error {status_code}: {status_msg[:60]}")
            else:
                print(f"    ❓ Unexpected: {str(resp_json)[:80]}")
                
        except Exception as e:
            print(f"    ❌ Exception: {str(e)[:60]}")

print(f"\n{'='*70}")
print("❌ No working configuration found")
print('='*70)
