#!/bin/bash
# Lightweight HAS MCP Client for 32bit systems
# Pure bash + curl solution

HAS_ZEN="http://192.168.0.58:8020"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

show_help() {
    cat << 'HELP'
🚀 HAS Client - 32bit Compatible

Usage: ./has-client-32bit.sh <command> [args...]

Commands:
  memory <text>     - Store in HAS memory
  search <query>    - Search HAS memories  
  exec <command>    - Execute on HAS server
  git <command>     - Git operations on HAS
  file <path>       - Read file from HAS
  status           - Check HAS status
  help             - Show this help

Examples:
  ./has-client-32bit.sh memory "Testing from 32bit notebook"
  ./has-client-32bit.sh search "notebook"
  ./has-client-32bit.sh exec "uptime"
  ./has-client-32bit.sh git "status"
  ./has-client-32bit.sh file "/home/orchestration/README.md"
HELP
}

mcp_call() {
    local tool="$1"
    local args="$2"
    
    local payload="{\"tool\":\"$tool\",\"arguments\":$args}"
    
    curl -s -X POST "$HAS_ZEN/mcp" \
         -H "Content-Type: application/json" \
         -d "$payload" 2>/dev/null || echo '{"error":"Connection failed"}'
}

case "$1" in
    "memory")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: No content provided${NC}"
            exit 1
        fi
        content="$2"
        args="{\"content\":\"$content\",\"category\":\"notebook\"}"
        result=$(mcp_call "store_memory" "$args")
        echo -e "${GREEN}💾 Stored:${NC} $result"
        ;;
        
    "search")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: No query provided${NC}"
            exit 1
        fi
        query="$2"
        args="{\"query\":\"$query\"}"
        result=$(mcp_call "search_memories" "$args")
        echo -e "${BLUE}🔍 Search results:${NC}"
        echo "$result" | jq . 2>/dev/null || echo "$result"
        ;;
        
    "exec")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: No command provided${NC}"
            exit 1
        fi
        command="$2"
        args="{\"command\":\"$command\"}"
        result=$(mcp_call "execute_command" "$args")
        echo -e "${YELLOW}⚡ Command result:${NC}"
        echo "$result" | jq . 2>/dev/null || echo "$result"
        ;;
        
    "git")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: No git command provided${NC}"
            exit 1
        fi
        git_cmd="$2"
        args="{\"command\":\"$git_cmd\",\"repo_path\":\"/home/orchestration\"}"
        result=$(mcp_call "git_execute" "$args")
        echo -e "${BLUE}🔀 Git result:${NC}"
        echo "$result" | jq . 2>/dev/null || echo "$result"
        ;;
        
    "file")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Error: No file path provided${NC}"
            exit 1
        fi
        file_path="$2"
        args="{\"path\":\"$file_path\"}"
        result=$(mcp_call "file_read" "$args")
        echo -e "${GREEN}📄 File content:${NC}"
        echo "$result" | jq . 2>/dev/null || echo "$result"
        ;;
        
    "status")
        echo -e "${BLUE}🔍 Checking HAS status...${NC}"
        curl -s "$HAS_ZEN/health" | jq . 2>/dev/null || curl -s "$HAS_ZEN/health"
        ;;
        
    "help"|""|*)
        show_help
        ;;
esac
