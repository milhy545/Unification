#!/usr/bin/env python3
"""
FEI Bridge for 32bit Notebook → HAS MCP
Lightweight FEI-style interface for HAS services
"""

import json
import requests
import sys
from typing import Dict, Any

class FEIBridge:
    def __init__(self):
        self.has_endpoint = "http://100.79.142.112:8020"
        self.context = []
        
    def ask(self, query: str) -> str:
        """FEI-style ask interface"""
        print(f"🧠 Processing: {query}")
        
        # Determine action based on query
        if "remember" in query.lower() or "store" in query.lower():
            return self._store_memory(query)
        elif "recall" in query.lower() or "search" in query.lower() or "find" in query.lower():
            return self._search_memory(query)
        elif "execute" in query.lower() or "run" in query.lower():
            return self._execute_command(query)
        elif "status" in query.lower() or "health" in query.lower():
            return self._system_status()
        else:
            return self._general_query(query)
    
    def _mcp_call(self, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Internal MCP call to HAS"""
        try:
            payload = {"tool": tool, "arguments": args}
            response = requests.post(f"{self.has_endpoint}/mcp", json=payload, timeout=20)
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def _store_memory(self, query: str) -> str:
        """Store information in HAS memory"""
        content = query.replace("remember", "").replace("store", "").strip()
        result = self._mcp_call("store_memory", {"content": content, "category": "notebook"})
        
        if "error" in result:
            return f"❌ Failed to store: {result['error']}"
        else:
            return f"✅ Stored in HAS memory: {content[:50]}..."
    
    def _search_memory(self, query: str) -> str:
        """Search HAS memories"""
        search_term = query.replace("recall", "").replace("search", "").replace("find", "").strip()
        result = self._mcp_call("search_memories", {"query": search_term})
        
        if "error" in result:
            return f"❌ Search failed: {result['error']}"
        else:
            memories = result if isinstance(result, list) else result.get("memories", [])
            if memories:
                return f"🔍 Found {len(memories)} memories:\n" + "\n".join([f"- {m.get('content', 'N/A')[:100]}" for m in memories[:3]])
            else:
                return "🔍 No memories found for: " + search_term
    
    def _execute_command(self, query: str) -> str:
        """Execute command on HAS"""
        command = query.replace("execute", "").replace("run", "").strip()
        result = self._mcp_call("execute_command", {"command": command})
        
        if "error" in result:
            return f"❌ Command failed: {result['error']}"
        else:
            return f"⚡ Command result:\n{result.get('stdout', 'No output')}"
    
    def _system_status(self) -> str:
        """Get HAS system status"""
        try:
            response = requests.get(f"{self.has_endpoint}/health", timeout=10)
            if response.status_code == 200:
                status = response.json()
                return f"✅ HAS Status: {status.get('status', 'unknown')}, Services: {status.get('services_running', 0)}/{status.get('services_total', 0)}"
            else:
                return f"❌ HAS not responding: {response.status_code}"
        except Exception as e:
            return f"❌ Connection failed: {e}"
    
    def _general_query(self, query: str) -> str:
        """Handle general queries via research MCP"""
        result = self._mcp_call("research_query", {"query": query, "model": "gemini-flash"})
        
        if "error" in result:
            return f"❌ Research failed: {result['error']}"
        else:
            return f"🤖 Research result:\n{result.get('response', 'No response')}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fei-32bit-bridge.py 'your question'")
        print("Example: python3 fei-32bit-bridge.py 'remember that I am testing from 32bit notebook'")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    fei = FEIBridge()
    result = fei.ask(query)
    print(result)

if __name__ == "__main__":
    main()
