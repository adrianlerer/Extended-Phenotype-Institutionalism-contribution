"""
Test MiniMax with official Python SDK
"""
import os
import base64
import json
from pathlib import Path

# Load environment
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

print(f"✓ API Key: {len(api_key)} chars")
print(f"✓ GroupID: {group_id}\n")

try:
    from minimax import Minimax
    
    print("Testing official Minimax SDK...")
    client = Minimax(
        api_key=api_key,
        group_id=group_id
    )
    
    print("✓ Client initialized successfully\n")
    print("SDK uses its own authentication - checking internals...")
    
    # The SDK might handle video only, but let's see what attributes it has
    print(f"Client attributes: {[attr for attr in dir(client) if not attr.startswith('_')]}")
    
except ImportError as e:
    print(f"❌ SDK not installed properly: {e}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
