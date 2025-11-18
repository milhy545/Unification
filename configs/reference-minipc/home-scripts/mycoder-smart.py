#!/usr/bin/env python3
"""
MyCoder Smart - AI + MCP Integration
Combines fast AI with HAS MCP tool access
"""

import json
import requests
import sys
import readline
from datetime import datetime

class MyCoderSmart:
    def __init__(self):
        self.has_zen = "http://192.168.0.58:8020"  
        self.llms_ollama = "http://192.168.0.41:11434"
        self.conversation_history = []
        self.session_id = f"smart-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        print(f"🧠 MyCoder Smart - AI + MCP Tools")
        print(f"📱 Session: {self.session_id}")
        print()

    def chat_with_ollama(self, prompt: str, model: str = "qwen2:1.5b"):
        """Chat with Ollama with context"""
        # Add MCP context to prompt
        enhanced_prompt = f"""You are MyCoder, an AI assistant with access to remote tools via MCP (Model Context Protocol).

Available tools via HAS server:
- store_memory/search_memories: Save and recall information
- execute_command: Run shell commands on HAS server  
- file_read/file_write: Read/write files on HAS
- git operations: Git commands on repositories
- database queries: PostgreSQL and Redis access

User question: {prompt}

If the user asks about system monitoring, file operations, or needs to store/recall information, suggest using the MCP tools with /exec, /memory, or /search commands.
"""

        try:
            payload = {
                "model": model,
                "prompt": enhanced_prompt,
                "stream": False,
                "options": {"temperature": 0.5, "top_p": 0.9, "num_predict": 200}
            }
            
            response = requests.post(f"{self.llms_ollama}/api/generate", json=payload, timeout=45)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"❌ Error: {response.status_code}"
                
        except Exception as e:
            return f"❌ Connection failed: {e}"

    def send_mcp_request(self, tool: str, arguments: dict):
        """Send request to HAS MCP services"""
        try:
            payload = {"tool": tool, "arguments": arguments}
            response = requests.post(f"{self.has_zen}/mcp", json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"MCP error: {response.status_code}"}
        except Exception as e:
            return {"error": f"HAS connection failed: {e}"}

    def store_memory(self, content: str, category: str = "smart-session"):
        """Store in HAS memory"""
        result = self.send_mcp_request("store_memory", {
            "content": content, 
            "category": category,
            "metadata": {"session": self.session_id}
        })
        return result

    def search_memories(self, query: str):
        """Search HAS memories"""
        result = self.send_mcp_request("search_memories", {"query": query})
        return result.get("memories", []) if "memories" in result else []

    def execute_on_has(self, command: str):
        """Execute command on HAS"""
        result = self.send_mcp_request("execute_command", {"command": command})
        return result

    def smart_models(self):
        """Models good for reasoning and tool use"""
        return ["qwen2:1.5b", "qwen2-thinking:latest", "system-monitor:latest", "working-planner:latest"]

    def chat_loop(self):
        """Smart chat loop with MCP integration"""
        current_model = "qwen2:1.5b"
        
        print(f"🧠 Ready! Using: {current_model} (balanced speed/intelligence)")
        print("Available: AI chat + MCP tools (memory, exec, search)")
        print("-" * 50)
        
        while True:
            try:
                user_input = input(f"\n🧑 ").strip()
                
                if not user_input:
                    continue
                    
                if user_input == '/quit' or user_input == '/exit':
                    print(f"👋 Goodbye! Session: {self.session_id}")
                    break
                    
                elif user_input == '/help':
                    print("""
🧠 MyCoder Smart Commands:
=========================
💬 <message>         - Chat with AI (has MCP context)
💾 /memory <text>    - Store important information  
🔍 /search <query>   - Search stored memories
⚡ /exec <command>   - Execute command on HAS server
🔄 /model <name>     - Switch AI model
📊 /status           - Check systems status
🧠 /models           - Show smart models
❓ /help             - This help
👋 /quit             - Exit

Examples:
  How can I monitor disk space on HAS?
  /memory "Vacation started Sept 1st"
  /search "vacation"  
  /exec "df -h"
                    """)
                    
                elif user_input.startswith('/memory '):
                    content = user_input[8:]
                    result = self.store_memory(content)
                    if "error" not in result:
                        print(f"💾 Stored: {content[:50]}{'...' if len(content) > 50 else ''}")
                    else:
                        print(f"❌ Memory error: {result['error']}")
                        
                elif user_input.startswith('/search '):
                    query = user_input[8:]
                    memories = self.search_memories(query)
                    print(f"🔍 Found {len(memories)} results for '{query}':")
                    for i, memory in enumerate(memories[:3], 1):
                        content = memory.get('content', '')[:80]
                        print(f"  {i}. {content}{'...' if len(memory.get('content', '')) > 80 else ''}")
                        
                elif user_input.startswith('/exec '):
                    command = user_input[6:]
                    print(f"⚡ Executing: {command}")
                    result = self.execute_on_has(command)
                    if "stdout" in result:
                        stdout = result["stdout"][:500]
                        print(f"📤 Output: {stdout}{'...' if len(result.get('stdout', '')) > 500 else ''}")
                    elif "error" in result:
                        print(f"❌ Error: {result['error']}")
                    else:
                        print(f"📤 Result: {result}")
                        
                elif user_input.startswith('/model '):
                    new_model = user_input[7:]
                    current_model = new_model
                    print(f"🔄 Switched to: {current_model}")
                    
                elif user_input == '/models':
                    models = self.smart_models()
                    print(f"🧠 Smart models for reasoning + MCP:")
                    for model in models:
                        marker = "👑" if model == current_model else "🤖"
                        print(f"  {marker} {model}")
                        
                elif user_input == '/status':
                    print("📊 System status check...")
                    # HAS check
                    try:
                        result = requests.get(f"{self.has_zen}/health", timeout=5)
                        if result.status_code == 200:
                            status = result.json()
                            print(f"✅ HAS: {status.get('status')} ({status.get('services_running')}/{status.get('services_total')} services)")
                        else:
                            print("❌ HAS: Offline")
                    except:
                        print("❌ HAS: Unreachable")
                        
                    # LLMS check
                    try:
                        result = requests.get(f"{self.llms_ollama}/api/tags", timeout=5)
                        if result.status_code == 200:
                            models = result.json()["models"]
                            print(f"✅ LLMS: {len(models)} models available")
                        else:
                            print("❌ LLMS: Offline")  
                    except:
                        print("❌ LLMS: Unreachable")
                        
                else:
                    # AI Chat with MCP context
                    print(f"🧠 Thinking with {current_model}...", end="", flush=True)
                    response = self.chat_with_ollama(user_input, current_model)
                    print(f"\r🤖 AI: {response}")
                    
                    # Store conversation
                    self.conversation_history.append({
                        "user": user_input, 
                        "ai": response,
                        "model": current_model,
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except KeyboardInterrupt:
                print("\n⏸️  Interrupted. Type /quit to exit.")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    smart_ai = MyCoderSmart()
    smart_ai.chat_loop()
