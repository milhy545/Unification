#!/usr/bin/env python3
"""
MyCoder Ultimate - Smart AI + Multiple LLM Providers + MCP Tools
Claude Code alternative with internet LLMs, local Ollama, and HAS MCP
"""

import os, subprocess, json, requests
from datetime import datetime

class MyCoderUltimate:
    def __init__(self):
        self.ollama_url = "http://192.168.0.41:11434"
        self.has_zen = "http://192.168.0.58:8020"
        self.cwd = os.getcwd()
        self.conversation = []
        
        print(f"🧠 MyCoder Ultimate - Multi-LLM + MCP")
        print(f"📁 {self.cwd}")
        print(f"🌐 Providers: Ollama (local) + HAS ZEN + Internet APIs")

    def read_file(self, path, lines=20):
        """Read file like Claude Code Read tool"""
        try:
            with open(os.path.expanduser(path), 'r') as f:
                content = f.readlines()[:lines]
            return ''.join(f"{i+1:4}: {line}" for i, line in enumerate(content))
        except Exception as e:
            return f"❌ Read failed: {e}"

    def bash(self, cmd, timeout=15):
        """Execute bash like Claude Code Bash tool"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=self.cwd)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"❌ Exit {result.returncode}: {result.stderr[:200]}"
        except subprocess.TimeoutExpired:
            return f"❌ Timeout after {timeout}s"
        except Exception as e:
            return f"❌ Command failed: {e}"

    def mcp_call(self, tool, args):
        """Call HAS MCP services via ZEN"""
        try:
            payload = {"tool": tool, "arguments": args}
            response = requests.post(f"{self.has_zen}/mcp", json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"MCP {tool} failed: {response.status_code}"}
        except Exception as e:
            return {"error": f"HAS unreachable: {e}"}

    def chat_ollama(self, prompt, model="ultra-fast:latest"):
        """Chat with local Ollama"""
        try:
            # Add file system context
            context = f"You are MyCoder, like Claude Code with file system access.\nCurrent dir: {self.cwd}\nTools: /r file, /b cmd, /mcp tool\nQuery: {prompt}"
            
            payload = {
                "model": model,
                "prompt": context,
                "stream": False,
                "options": {"temperature": 0.6, "num_predict": 200}
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"❌ Ollama error: {response.status_code}"
        except Exception as e:
            return f"❌ Ollama offline: {e}"

    def chat_zen_ai(self, prompt):
        """Chat via HAS ZEN coordinator (if it has AI proxy)"""
        try:
            # Try ZEN AI endpoint
            payload = {"query": prompt, "provider": "auto"}
            response = requests.post(f"{self.has_zen}/ai/chat", json=payload, timeout=45)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response from ZEN AI")
            else:
                return f"❌ ZEN AI error: {response.status_code}"
        except Exception as e:
            return f"❌ ZEN AI unavailable: {e}"

    def chat_internet_fallback(self, prompt):
        """Fallback to free internet LLM APIs"""
        # Try HuggingFace Inference API (free tier)
        try:
            hf_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            headers = {"Content-Type": "application/json"}
            payload = {"inputs": f"Human: {prompt}\nAssistant:"}
            
            response = requests.post(hf_url, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "No response").replace(f"Human: {prompt}\nAssistant:", "").strip()
            
            return "❌ Internet LLM unavailable"
        except Exception as e:
            return f"❌ Internet LLM failed: {e}"

    def smart_chat(self, prompt, provider="auto"):
        """Intelligent multi-provider chat with fallback"""
        providers = {
            "ollama": self.chat_ollama,
            "zen": self.chat_zen_ai, 
            "internet": self.chat_internet_fallback
        }
        
        if provider == "auto":
            # Try providers in order of preference
            for name, func in providers.items():
                print(f"🤖 Trying {name}...", end="", flush=True)
                response = func(prompt)
                if not response.startswith("❌"):
                    print(f"\r🤖 {name.title()}: {response[:100]}{'...' if len(response) > 100 else ''}")
                    return response
                print(f"\r❌ {name} failed, trying next...")
            
            return "❌ All AI providers failed"
        else:
            return providers.get(provider, self.chat_ollama)(prompt)

    def show_help(self):
        return """🧠 MyCoder Ultimate Commands:

📁 FILE OPERATIONS:
  /r <file>              - Read file (like Claude Code)
  /w <file> <content>    - Write file (interactive)
  
⚡ SYSTEM OPERATIONS:  
  /b <command>           - Bash command
  /cd <path>             - Change directory
  /l                     - List files (ls -la)
  
🌐 MCP TOOLS (via HAS ZEN):
  /mcp memory <text>     - Store in HAS memory
  /mcp search <query>    - Search HAS memories
  /mcp exec <command>    - Execute on HAS server
  /mcp git <command>     - Git operations on HAS
  
🤖 AI CHAT (Multi-provider):
  <message>              - Auto-select best AI provider
  /ai ollama <message>   - Force Ollama (local)
  /ai zen <message>      - Force ZEN coordinator AI
  /ai net <message>      - Force internet LLM
  
🔧 UTILITY:
  /models                - Show available Ollama models
  /status                - System status
  /help                  - This help
  /quit                  - Exit

Examples:
  /r ~/.zshrc
  /b df -h
  /mcp memory "Important vacation note"
  /ai ollama How do I check disk space?
  Can you help me with Python?"""

    def run(self):
        """Main MyCoder Ultimate loop"""
        print("Type /help for commands, or just chat!")
        print("-" * 50)
        
        while True:
            try:
                inp = input(f"\n📁 {os.path.basename(self.cwd)} > ").strip()
                
                if not inp:
                    continue
                    
                if inp in ['/quit', '/q', '/exit']:
                    print(f"👋 MyCoder session ended. Chats: {len(self.conversation)}")
                    break
                    
                elif inp == '/help':
                    print(self.show_help())
                    
                elif inp == '/l':
                    print(self.bash("ls -la"))
                    
                elif inp.startswith('/cd '):
                    path = inp[4:]
                    try:
                        os.chdir(os.path.expanduser(path))
                        self.cwd = os.getcwd()
                        print(f"📁 Changed to: {self.cwd}")
                    except Exception as e:
                        print(f"❌ cd failed: {e}")
                        
                elif inp.startswith('/r '):
                    file_path = inp[3:]
                    print(self.read_file(file_path))
                    
                elif inp.startswith('/w '):
                    file_path = inp[3:]
                    print(f"Writing to {file_path}. Enter content, end with '###':")
                    content = []
                    while True:
                        line = input()
                        if line == '###':
                            break
                        content.append(line)
                    
                    try:
                        with open(os.path.expanduser(file_path), 'w') as f:
                            f.write('\n'.join(content))
                        print(f"✅ Written: {file_path}")
                    except Exception as e:
                        print(f"❌ Write failed: {e}")
                        
                elif inp.startswith('/b '):
                    command = inp[3:]
                    print(self.bash(command))
                    
                elif inp.startswith('/mcp '):
                    mcp_parts = inp[5:].split(' ', 1)
                    if len(mcp_parts) < 2:
                        print("❓ Usage: /mcp <tool> <args>")
                        continue
                        
                    tool_name = mcp_parts[0]
                    args = mcp_parts[1]
                    
                    if tool_name == 'memory':
                        result = self.mcp_call("store_memory", {"content": args, "category": "ultimate-session"})
                    elif tool_name == 'search':
                        result = self.mcp_call("search_memories", {"query": args})
                    elif tool_name == 'exec':
                        result = self.mcp_call("execute_command", {"command": args})
                    elif tool_name == 'git':
                        result = self.mcp_call("git_execute", {"command": args})
                    else:
                        result = {"error": f"Unknown MCP tool: {tool_name}"}
                    
                    if "error" in result:
                        print(f"❌ {result['error']}")
                    else:
                        print(f"✅ MCP {tool_name}: {json.dumps(result, indent=2)[:300]}...")
                        
                elif inp.startswith('/ai '):
                    ai_parts = inp[4:].split(' ', 1)
                    if len(ai_parts) < 2:
                        print("❓ Usage: /ai <provider> <message>")
                        continue
                        
                    provider = ai_parts[0]
                    message = ai_parts[1]
                    response = self.smart_chat(message, provider)
                    print(response)
                    
                elif inp == '/models':
                    try:
                        response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
                        if response.status_code == 200:
                            models = response.json()["models"]
                            print(f"🧠 Available Ollama models ({len(models)}):")
                            for model in models[:10]:
                                name = model["name"]
                                size = model.get("size", 0) // (1024*1024)  # MB
                                print(f"  • {name} ({size}MB)")
                            if len(models) > 10:
                                print(f"  ... and {len(models)-10} more")
                        else:
                            print("❌ Cannot fetch models")
                    except Exception as e:
                        print(f"❌ Models unavailable: {e}")
                        
                elif inp == '/status':
                    print("📊 MyCoder Ultimate Status:")
                    print(f"  📁 Directory: {self.cwd}")
                    print(f"  💬 Conversations: {len(self.conversation)}")
                    
                    # Test providers
                    providers = [
                        ("Ollama", self.ollama_url + "/api/tags"),
                        ("HAS ZEN", self.has_zen + "/health")
                    ]
                    
                    for name, url in providers:
                        try:
                            r = requests.get(url, timeout=5)
                            status = "✅ Online" if r.status_code == 200 else f"❌ Error {r.status_code}"
                        except:
                            status = "❌ Offline"
                        print(f"  🌐 {name}: {status}")
                        
                else:
                    # Regular AI chat with auto-provider selection
                    response = self.smart_chat(inp)
                    print(response)
                    
                    # Store conversation
                    self.conversation.append({
                        "user": inp,
                        "ai": response,
                        "timestamp": datetime.now().isoformat(),
                        "cwd": self.cwd
                    })
                    
            except KeyboardInterrupt:
                print("\n⏸️  Interrupted. Type /quit to exit.")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    mycoder = MyCoderUltimate()
    mycoder.run()
