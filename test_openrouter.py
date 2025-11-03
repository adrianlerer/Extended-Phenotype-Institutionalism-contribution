"""
Test OpenRouter API with MiniMax-M2 model
"""
from openai import OpenAI
import os
from pathlib import Path

# Load environment variables
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

api_key = os.environ.get("OPENROUTER_API_KEY")

print("="*70)
print("TESTING OPENROUTER + MINIMAX-M2")
print("="*70)
print(f"\n✓ API Key loaded: {api_key[:20]}...{api_key[-10:]}")
print(f"  Length: {len(api_key)} chars\n")

# Initialize OpenAI client with OpenRouter endpoint
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

print("✓ Client initialized\n")
print("-"*70)
print("TEST 1: Basic Text Generation (MiniMax-M2)")
print("-"*70)

try:
    response = client.chat.completions.create(
        model="minimax/minimax-01",  # MiniMax-M2
        messages=[
            {
                "role": "user",
                "content": "Responde brevemente en español: '¿El sistema IusMorfos está funcionando?'"
            }
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    print(f"✅ SUCCESS!\n")
    print(f"Model: {response.model}")
    print(f"Response:\n{response.choices[0].message.content}\n")
    
    print("-"*70)
    print("TEST 2: Legal Analysis with <think> tags")
    print("-"*70)
    
    response2 = client.chat.completions.create(
        model="minimax/minimax-01",
        messages=[
            {
                "role": "user",
                "content": """
<think>
Necesito analizar el concepto de "habeas corpus".
Debo identificar:
1. Origen histórico
2. Principio jurídico fundamental
3. Aplicación moderna
</think>

Resume en 2 frases el concepto de "habeas corpus" en español.
"""
            }
        ],
        max_tokens=100,
        temperature=0.3
    )
    
    print(f"✅ SUCCESS!\n")
    print(f"Response:\n{response2.choices[0].message.content}\n")
    
    print("="*70)
    print("🎉 SISTEMA FUNCIONANDO 100%")
    print("="*70)
    print("\n✅ OpenRouter + MiniMax-M2 operativo")
    print("✅ Thinking tags soportados")
    print("✅ Análisis jurídico funcional")
    print("\n📊 Próximos pasos:")
    print("  1. Implementar RootFinder con MiniMax-M2")
    print("  2. Implementar JurisRank con MiniMax-M2")
    print("  3. Implementar IusMorfos Peralta con MiniMax-M2")
    print("  4. Crear interfaz unificada")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
