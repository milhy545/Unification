#!/usr/bin/env python3
"""
MyCoder Claude - Real Claude API Integration for 32bit systems
Uses claude-cli-authentication for genuine Claude AI access
"""

import os, sys, subprocess, json, requests, asyncio
from pathlib import Path

# Add claude-cli-authentication to path
sys.path.insert(0, '/home/milhy777/claude-cli-authentication/src')

try:
    from claude_cli_auth import ClaudeAuthManager, ClaudeAuthError
    CLAUDE_AUTH_AVAILABLE = True
    print("✅ Claude CLI Authentication loaded")
except ImportError as e:
    CLAUDE_AUTH_AVAILABLE = False
    print(f"❌ Claude CLI Auth not available: {e}")

class MyCoderClaude:
    def __init__(self):
        self.ollama_url = "http://192.168.0.41:11434"
        self.has_zen = "http://192.168.0.58:8020"
        self.cwd = Path.cwd()
        self.claude_manager = None
        
        print(f"🤖 MyCoder Claude - Real Claude + Ollama + MCP")
        print(f"📁 {self.cwd}")
        
        # Initialize Claude if available
        if CLAUDE_AUTH_AVAILABLE:
            try:
                self.claude_manager = ClaudeAuthManager()
                print("🧠 Claude AI: Ready (via claude-cli-auth)")
            except Exception as e:
                print(f"⚠️  Claude AI: Error initializing - {e}")
                self.claude_manager = None
        else:
            print("⚠️  Claude AI: Not available (using Ollama fallback)")

    def read_file(self, path, lines=25):
        """Read file like Claude Code"""
        try:
            with open(Path(path).expanduser(), 'r') as f:
                content = f.readlines()[:lines]
            return ''.join(f"{i+1:4}: {line}" for i, line in enumerate(content))
        except Exception as e:
            return f"❌ Read failed: {e}"

    def bash(self, cmd, timeout=15):
        """Execute bash command"""
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

    async def chat_claude_real(self, prompt, session_id="mycoder-session"):
        """Chat with real Claude AI via claude-cli-authentication"""
        if not self.claude_manager:
            return "❌ Claude AI not available"
            
        try:
            # Add file system context like Claude Code
            context = f"""You are Claude, working in directory {self.cwd}.
Available tools: /r <file> (read), /b <cmd> (bash), /mcp <tool> (MCP commands).

Current working directory contents:
{self.bash('ls -la')[:300]}

User request: {prompt}"""

            response = await self.claude_manager.query(
                context,
                working_directory=self.cwd,
                session_id=session_id,
                continue_session=True
            )
            
            return response.content if hasattr(response, 'content') else str(response)
            
        except ClaudeAuthError as e:
            return f"❌ Claude auth error: {e}"
        except Exception as e:
            return f"❌ Claude error: {e}"

    def chat_ollama_fallback(self, prompt, model="qwen2:1.5b"):
        """Fallback to Ollama if Claude unavailable"""
        try:
            context = f"You are Claude assistant. Directory: {self.cwd}\nQuery: {prompt}"
            payload = {
                "model": model,
                "prompt": context,
                "stream": False,
                "options": {"temperature": 0.6, "num_predict": 250}
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"❌ Ollama error: {response.status_code}"
        except Exception as e:
            return f"❌ Ollama unavailable: {e}"

    def mcp_call(self, tool, args):
        """Call HAS MCP services"""
        try:
            payload = {"tool": tool, "arguments": args}
            response = requests.post(f"{self.has_zen}/mcp", json=payload, timeout=20)
            return response.json() if response.status_code == 200 else {"error": f"MCP failed: {response.status_code}"}
        except Exception as e:
            return {"error": f"HAS unreachable: {e}"}

    async def smart_chat(self, prompt):
        """Smart chat with Claude-first, Ollama fallback"""
        if self.claude_manager:
            print("🧠 Asking real Claude...", end="", flush=True)
            claude_response = await self.chat_claude_real(prompt)
            if not claude_response.startswith("❌"):
                print(f"\r🧠 Claude: {claude_response[:100]}{'...' if len(claude_response) > 100 else ''}")
                return claude_response
            else:
                print(f"\r❌ Claude failed: {claude_response[:50]}...")
        
        print("🤖 Using Ollama fallback...", end="", flush=True)
        ollama_response = self.chat_ollama_fallback(prompt)
        print(f"\r🤖 Ollama: {ollama_response[:100]}{'...' if len(ollama_response) > 100 else ''}")
        return ollama_response

    def show_help(self):
        return """🤖 MyCoder Claude - Real Claude + Tools:

📁 FILE OPERATIONS:
  /r <file>              - Read file
  /b <command>           - Bash command
  /cd <path>             - Change directory
  /l                     - List files

🧠 AI CHAT:
  <message>              - Chat with real Claude (fallback to Ollama)
  /ollama <message>      - Force Ollama local
  /claude <message>      - Force real Claude only

🌐 MCP TOOLS:
  /mcp memory <text>     - Store in HAS memory
  /mcp search <query>    - Search memories
  /mcp exec <cmd>        - Execute on HAS

🔧 UTILITY:
  /status                - System status
  /help                  - This help
  /quit                  - Exit

Examples:
  /r ~/.zshrc
  /b ps aux | grep python
  Can you help me write a Python script?
  /claude Explain this error message
  /mcp memory "Claude works on 32bit!""

    def run(self):
        """Main async loop"""
        print("Type /help for commands, or just chat!")
        print("-" * 50)
        
        async def main_loop():
            while True:
                try:
                    inp = input(f"\n📁 {self.cwd.name} > ").strip()
                    
                    if not inp:
                        continue
                        
                    if inp in ['/quit', '/q', '/exit']:
                        print("👋 MyCoder Claude session ended")
                        break
                        
                    elif inp == '/help':
                        print(self.show_help())
                        
                    elif inp == '/l':
                        print(self.bash("ls -la"))
                        
                    elif inp.startswith('/cd '):
                        path = inp[4:]
                        try:
                            new_path = Path(path).expanduser().resolve()
                            os.chdir(new_path)
                            self.cwd = Path.cwd()
                            print(f"📁 Changed to: {self.cwd}")
                        except Exception as e:
                            print(f"❌ cd failed: {e}")
                            
                    elif inp.startswith('/r '):
                        file_path = inp[3:]
                        print(self.read_file(file_path))
                        
                    elif inp.startswith('/b '):
                        command = inp[3:]
                        print(self.bash(command))
                        
                    elif inp.startswith('/mcp '):
                        mcp_parts = inp[5:].split(' ', 1)
                        if len(mcp_parts) < 2:
                            print("❓ Usage: /mcp <tool> <args>")
                            continue
                            
                        tool, args = mcp_parts
                        if tool == 'memory':
                            result = self.mcp_call("store_memory", {"content": args})
                        elif tool == 'search':
                            result = self.mcp_call("search_memories", {"query": args})
                        elif tool == 'exec':
                            result = self.mcp_call("execute_command", {"command": args})
                        else:
                            result = {"error": f"Unknown tool: {tool}"}
                        
                        if "error" in result:
                            print(f"❌ {result['error']}")
                        else:
                            print(f"✅ MCP result: {json.dumps(result, indent=2)[:200]}...")
                            
                    elif inp.startswith('/claude '):
                        if not self.claude_manager:
                            print("❌ Claude not available")
                        else:
                            prompt = inp[8:]
                            response = await self.chat_claude_real(prompt)
                            print(f"🧠 Claude: {response}")
                            
                    elif inp.startswith('/ollama '):
                        prompt = inp[8:]
                        response = self.chat_ollama_fallback(prompt)
                        print(f"🤖 Ollama: {response}")
                        
                    elif inp == '/status':
                        print(f"📊 MyCoder Claude Status:")
                        print(f"  📁 Directory: {self.cwd}")
                        print(f"  🧠 Real Claude: {'✅ Available' if self.claude_manager else '❌ Not available'}")
                        
                        # Test connections
                        try:
                            ollama_test = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
                            ollama_status = "✅ Online" if ollama_test.status_code == 200 else "❌ Error"
                        except:
                            ollama_status = "❌ Offline"
                        print(f"  🤖 Ollama: {ollama_status}")
                        
                        try:
                            has_test = requests.get(f"{self.has_zen}/health", timeout=3)
                            has_status = "✅ Online" if has_test.status_code == 200 else "❌ Error"
                        except:
                            has_status = "❌ Offline"
                        print(f"  🏠 HAS: {has_status}")
                        
                    else:
                        # Smart chat
                        response = await self.smart_chat(inp)
                        print(response)
                        
                except KeyboardInterrupt:
                    print("\n⏸️  Interrupted. Type /quit to exit.")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        # Run async main loop
        try:
            asyncio.run(main_loop())
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")

if __name__ == "__main__":
    mycoder = MyCoderClaude()
    mycoder.run()
