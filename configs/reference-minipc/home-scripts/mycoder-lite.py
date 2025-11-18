#!/usr/bin/env python3
"""
MyCoder Lite Setup for 32bit Notebooks
Lightweight alternative to Claude Code with HAS MCP access
"""

import json
import requests
import sys
import readline  # For better input handling

class MyCoderLite:
    def __init__(self):
        self.has_zen = "http://192.168.0.58:8020"  # HAS IP
        self.session_memory = []
        
    def send_mcp_request(self, tool: str, arguments: dict):
        """Send request to HAS MCP services"""
        try:
            payload = {"tool": tool, "arguments": arguments}
            response = requests.post(f"{self.has_zen}/mcp", json=payload, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"MCP error: {response.status_code}", "details": response.text[:200]}
        except Exception as e:
            return {"error": f"Connection failed: {e}"}

    def store_memory(self, content: str, category: str = "general"):
        """Store in HAS memory"""
        result = self.send_mcp_request("store_memory", {"content": content, "category": category})
        self.session_memory.append({"action": "store", "content": content, "result": result})
        return result

    def search_memories(self, query: str):
        """Search HAS memories"""
        result = self.send_mcp_request("search_memories", {"query": query})
        self.session_memory.append({"action": "search", "query": query, "result": result})
        return result

    def execute_on_has(self, command: str):
        """Execute command on HAS"""
        result = self.send_mcp_request("execute_command", {"command": command})
        self.session_memory.append({"action": "execute", "command": command, "result": result})
        return result

    def read_has_file(self, path: str):
        """Read file from HAS"""
        result = self.send_mcp_request("file_read", {"path": path})
        return result

    def has_git(self, command: str, repo_path: str = "/home/orchestration"):
        """Git operations on HAS"""
        result = self.send_mcp_request("git_execute", {"command": command, "repo_path": repo_path})
        return result

    def chat_loop(self):
        """Main interactive loop"""
        print("🚀 MyCoder Lite - 32bit Compatible HAS MCP Client")
        print("Connected to HAS ZEN Coordinator:", self.has_zen)
        print("Commands: memory <text>, search <query>, exec <command>, git <cmd>, file <path>, help, quit")
        print("-" * 80)
        
        while True:
            try:
                user_input = input("\n📱 MyCoder> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                    
                elif user_input.lower() == 'help':
                    self.show_help()
                    
                elif user_input.startswith('memory '):
                    content = user_input[7:]
                    result = self.store_memory(content)
                    print(f"💾 Stored: {result}")
                    
                elif user_input.startswith('search '):
                    query = user_input[7:]
                    result = self.search_memories(query)
                    print(f"🔍 Found: {json.dumps(result, indent=2)}")
                    
                elif user_input.startswith('exec '):
                    command = user_input[5:]
                    result = self.execute_on_has(command)
                    print(f"⚡ Result: {json.dumps(result, indent=2)}")
                    
                elif user_input.startswith('git '):
                    command = user_input[4:]
                    result = self.has_git(command)
                    print(f"🔀 Git: {json.dumps(result, indent=2)}")
                    
                elif user_input.startswith('file '):
                    path = user_input[5:]
                    result = self.read_has_file(path)
                    print(f"📄 File: {json.dumps(result, indent=2)}")
                    
                else:
                    print("❓ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Interrupted. Type 'quit' to exit.")
            except Exception as e:
                print(f"❌ Error: {e}")

    def show_help(self):
        """Show help information"""
        print("""
📚 MyCoder Lite Commands:

💾 memory <text>     - Store text in HAS memory
🔍 search <query>    - Search HAS memories  
⚡ exec <command>    - Execute command on HAS server
🔀 git <command>     - Git operations on HAS
📄 file <path>       - Read file from HAS
❓ help             - Show this help
👋 quit             - Exit MyCoder

Examples:
  memory "Testing from 32bit notebook"
  search "notebook test"  
  exec "uptime"
  git "status"
  file "/home/orchestration/README.md"
        """)

if __name__ == "__main__":
    mycoder = MyCoderLite()
    mycoder.chat_loop()
