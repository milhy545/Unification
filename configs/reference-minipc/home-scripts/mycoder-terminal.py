#!/usr/bin/env python3
"""
MyCoder Terminal - AI s přímým shell přístupem
Může spouštět lokální i vzdálené příkazy
"""

import json
import requests
import subprocess
import os
import sys
import readline
from datetime import datetime

class MyCoderTerminal:
    def __init__(self):
        self.llms_ollama = "http://192.168.0.41:11434"
        self.has_zen = "http://192.168.0.58:8020"  
        self.conversation_history = []
        self.session_id = f"terminal-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        print(f"💻 MyCoder Terminal - AI + Shell Access")
        print(f"📱 Session: {self.session_id}")
        print(f"🏠 Local: {os.getcwd()}")
        print(f"👤 User: {os.getenv('USER', 'unknown')}")
        print()

    def run_local_command(self, command: str, timeout: int = 30):
        """Execute command locally on notebook"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.path.expanduser('~')
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "location": "local"
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {timeout}s", "location": "local"}
        except Exception as e:
            return {"success": False, "error": str(e), "location": "local"}

    def run_has_command(self, command: str):
        """Execute command on HAS via MCP"""
        try:
            payload = {"tool": "execute_command", "arguments": {"command": command}}
            response = requests.post(f"{self.has_zen}/mcp", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                result["location"] = "HAS"
                return result
            else:
                return {"success": False, "error": f"HAS MCP error: {response.status_code}", "location": "HAS"}
        except Exception as e:
            return {"success": False, "error": f"HAS connection failed: {e}", "location": "HAS"}

    def chat_with_ai(self, prompt: str, model: str = "qwen2:1.5b"):
        """Chat with AI with shell context"""
        # Add shell capabilities to context
        enhanced_prompt = f"""You are MyCoder Terminal, an AI assistant with direct shell access to both local (32bit antiX notebook) and remote (HAS server) systems.

Available capabilities:
LOCAL SHELL (notebook):
- Full bash/zsh access on antiX Linux
- File operations, system monitoring, package management
- Python, Node.js, git, network tools
- Current directory: /home/milhy777

REMOTE SHELL (HAS server):
- Execute commands via MCP on 192.168.0.58
- Access to orchestration services and databases
- Docker containers, system administration

When user asks about:
- System info, files, processes → suggest /local <command>
- HAS server, orchestration, databases → suggest /has <command>  
- Both systems → provide commands for both

User question: {prompt}

Provide helpful suggestions and explain what commands would be useful.
"""

        try:
            payload = {
                "model": model,
                "prompt": enhanced_prompt,
                "stream": False,
                "options": {"temperature": 0.6, "num_predict": 250}
            }
            
            response = requests.post(f"{self.llms_ollama}/api/generate", json=payload, timeout=45)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"❌ AI Error: {response.status_code}"
                
        except Exception as e:
            return f"❌ AI Connection failed: {e}"

    def format_command_output(self, result: dict, command: str):
        """Format command execution results"""
        location = result.get("location", "unknown")
        
        if result.get("success", False):
            stdout = result.get("stdout", "").strip()
            if stdout:
                return f"✅ {location}: {stdout[:500]}{'...' if len(stdout) > 500 else ''}"
            else:
                return f"✅ {location}: Command executed successfully (no output)"
        else:
            error = result.get("error", result.get("stderr", "Unknown error"))
            return f"❌ {location}: {error[:300]}{'...' if len(str(error)) > 300 else ''}"

    def show_capabilities(self):
        """Show system capabilities"""
        print("""
💻 MyCoder Terminal Capabilities:
===============================

🏠 LOCAL SYSTEM (antiX notebook):
  • System: 32bit antiX Linux, user milhy777
  • Shell: bash/zsh with full access
  • Tools: Python, Node.js, git, curl, ssh
  • Network: Tailscale VPN connected
  
🏢 REMOTE SYSTEM (HAS server):
  • System: Alpine Linux orchestration server  
  • Access: Via MCP protocol (secure)
  • Services: 7 MCP services, PostgreSQL, Redis
  • Tools: Docker, system administration

📋 COMMANDS:
  💬 <message>         - Chat with AI (knows both systems)
  🏠 /local <command>  - Execute on local notebook
  🏢 /has <command>    - Execute on HAS server
  📊 /status           - Check both systems
  💻 /info             - Show this info
  👋 /quit             - Exit

Examples:
  How can I check disk space on both systems?
  /local df -h
  /has docker ps
  /status
        """)

    def check_systems_status(self):
        """Check status of both systems"""
        print("📊 System Status Check:")
        print("=" * 30)
        
        # Local system
        print("🏠 LOCAL SYSTEM:")
        local_status = self.run_local_command("uname -a && uptime && df -h / | tail -1")
        if local_status["success"]:
            lines = local_status["stdout"].strip().split('\n')
            for line in lines:
                print(f"   {line}")
        else:
            print(f"   ❌ Error: {local_status.get('error', 'Unknown')}")
        
        print()
        
        # HAS system  
        print("🏢 HAS SYSTEM:")
        try:
            response = requests.get(f"{self.has_zen}/health", timeout=10)
            if response.status_code == 200:
                status = response.json()
                print(f"   ✅ Status: {status.get('status')}")
                print(f"   📊 Services: {status.get('services_running')}/{status.get('services_total')}")
                print(f"   💾 Database: {'✅' if status.get('database_healthy') else '❌'}")
                print(f"   🔴 Redis: {'✅' if status.get('redis_healthy') else '❌'}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
        
        print()

    def chat_loop(self):
        """Main terminal chat loop"""
        current_model = "qwen2:1.5b"
        
        print(f"💻 Ready! AI Model: {current_model}")
        print("Type /info for capabilities, /quit to exit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input(f"\n🧑 ").strip()
                
                if not user_input:
                    continue
                    
                if user_input in ['/quit', '/exit']:
                    print(f"👋 Terminal session ended. Commands executed: {len(self.conversation_history)}")
                    break
                    
                elif user_input == '/info':
                    self.show_capabilities()
                    
                elif user_input == '/status':
                    self.check_systems_status()
                    
                elif user_input.startswith('/local '):
                    command = user_input[7:]
                    print(f"🏠 Executing locally: {command}")
                    result = self.run_local_command(command)
                    output = self.format_command_output(result, command)
                    print(f"📤 {output}")
                    
                elif user_input.startswith('/has '):
                    command = user_input[5:]
                    print(f"🏢 Executing on HAS: {command}")
                    result = self.run_has_command(command)
                    output = self.format_command_output(result, command)
                    print(f"📤 {output}")
                    
                elif user_input.startswith('/model '):
                    new_model = user_input[7:]
                    current_model = new_model
                    print(f"🔄 Switched AI model to: {current_model}")
                    
                else:
                    # AI Chat
                    print(f"💭 AI thinking...", end="", flush=True)
                    response = self.chat_with_ai(user_input, current_model)
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
    terminal_ai = MyCoderTerminal()
    terminal_ai.chat_loop()
