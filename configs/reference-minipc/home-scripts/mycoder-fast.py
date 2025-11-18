#!/usr/bin/env python3
"""
MyCoder AI - Fast Edition for 32bit systems
Optimized for quick responses on vacation notebook
"""

import json
import requests
import sys
import readline
from datetime import datetime

class MyCoderFast:
    def __init__(self):
        self.has_zen = "http://192.168.0.58:8020"  
        self.llms_ollama = "http://192.168.0.41:11434"
        self.conversation_history = []
        self.session_id = f"vacation-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        print(f"⚡ MyCoder Fast - 32bit Optimized")
        print(f"📱 Session: {self.session_id}")
        print()

    def chat_with_ollama(self, prompt: str, model: str = "qwen2:0.5b"):
        """Chat with fastest Ollama models"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "top_p": 0.8, "num_predict": 100}  # Shorter responses
            }
            
            response = requests.post(f"{self.llms_ollama}/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"❌ Error: {response.status_code}"
                
        except Exception as e:
            return f"❌ Connection failed: {e}"

    def send_mcp_request(self, tool: str, arguments: dict):
        """Send request to HAS MCP"""
        try:
            payload = {"tool": tool, "arguments": arguments}
            response = requests.post(f"{self.has_zen}/mcp", json=payload, timeout=15)
            return response.json() if response.status_code == 200 else {"error": "MCP failed"}
        except:
            return {"error": "HAS unreachable"}

    def fast_models(self):
        """Show ultra-fast models"""
        return ["qwen2:0.5b", "ultra-fast:latest", "ultra-fast-agent:latest", "text-processor:latest"]

    def chat_loop(self):
        """Fast chat loop"""
        models = self.fast_models()
        current_model = "qwen2:0.5b"
        
        print(f"⚡ Ready! Using: {current_model}")
        print("Commands: /help /fast /model /status /quit")
        print("-" * 40)
        
        while True:
            try:
                user_input = input(f"\n🧑 ").strip()
                
                if not user_input:
                    continue
                    
                if user_input == '/quit':
                    print(f"👋 Bye! {len(self.conversation_history)} chats.")
                    break
                    
                elif user_input == '/help':
                    print("""
⚡ MyCoder Fast Commands:
========================
💬 <message>     - Chat with AI
🔄 /model <name> - Switch model  
⚡ /fast         - Show fast models
📊 /status       - System status
❓ /help         - This help
👋 /quit         - Exit

Fast models: qwen2:0.5b (default), ultra-fast:latest
                    """)
                    
                elif user_input == '/fast':
                    print(f"""
⚡ Ultra-fast models for 32bit:
==============================
🟢 qwen2:0.5b         (352MB, <1s)
🟢 ultra-fast:latest  (776MB, 1-2s)  
🟡 ultra-fast-agent   (352MB, 1-2s)
🟡 text-processor     (352MB, 1-3s)

Current: {current_model}
                    """)
                    
                elif user_input.startswith('/model '):
                    new_model = user_input[7:]
                    if new_model in models:
                        current_model = new_model
                        print(f"🔄 Switched to: {current_model}")
                    else:
                        print(f"❌ Unknown model. Use /fast to see available models.")
                        
                elif user_input == '/status':
                    print("📊 Quick status check...")
                    try:
                        result = requests.get(f"{self.has_zen}/health", timeout=5)
                        if result.status_code == 200:
                            print("✅ HAS: Online")
                        else:
                            print("❌ HAS: Offline")
                    except:
                        print("❌ HAS: Unreachable")
                        
                    try:
                        result = requests.get(f"{self.llms_ollama}/api/tags", timeout=3)
                        if result.status_code == 200:
                            count = len(result.json()["models"])
                            print(f"✅ LLMS: {count} models")
                        else:
                            print("❌ LLMS: Offline")
                    except:
                        print("❌ LLMS: Unreachable")
                        
                else:
                    # Chat
                    print(f"⚡ Thinking...", end="", flush=True)
                    response = self.chat_with_ollama(user_input, current_model)
                    print(f"\r🤖 {response}")
                    self.conversation_history.append({"user": user_input, "ai": response})
                    
            except KeyboardInterrupt:
                print("\n⏸️  Ctrl+C - Type /quit to exit")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    fast_ai = MyCoderFast()
    fast_ai.chat_loop()
