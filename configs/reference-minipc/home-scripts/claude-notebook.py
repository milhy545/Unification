#!/usr/bin/env python3
import os, sys, subprocess, json, requests, asyncio
from pathlib import Path

# Add claude-cli-auth to path
sys.path.insert(0, '/home/milhy777/claude-cli-authentication/src')

try:
    from claude_cli_auth import ClaudeAuthManager
    CLAUDE_AVAILABLE = True
    print('✅ Claude CLI Authentication available')
except ImportError:
    CLAUDE_AVAILABLE = False
    print('❌ Claude CLI Authentication not available')

class ClaudeNotebook:
    def __init__(self):
        self.ollama = 'http://192.168.0.41:11434'
        self.cwd = Path.cwd()
        self.claude = None
        
        print(f'🤖 Claude Notebook for 32bit')
        print(f'📁 {self.cwd}')
        
        if CLAUDE_AVAILABLE:
            try:
                self.claude = ClaudeAuthManager()
                print('🧠 Real Claude: Ready')
            except Exception as e:
                print(f'⚠️  Real Claude: Error - {e}')

    def r(self, path):  # read file
        try: 
            return ''.join(f'{i+1:3}: {l}' for i,l in enumerate(open(Path(path).expanduser()).readlines()[:20]))
        except Exception as e: 
            return f'❌ {e}'

    def b(self, cmd):  # bash
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10, cwd=self.cwd)
            return result.stdout if result.returncode == 0 else f'❌ {result.stderr[:100]}'
        except Exception as e: 
            return f'❌ {e}'

    async def claude_chat(self, prompt):
        if not self.claude:
            return '❌ Real Claude not available'
        try:
            context = f'Working in {self.cwd}. Available: /r file, /b cmd. Query: {prompt}'
            response = await self.claude.query(context, working_directory=self.cwd)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f'❌ Claude error: {e}'

    def ollama_chat(self, prompt):
        try:
            payload = {'model': 'qwen2:1.5b', 'prompt': f'Help with: {prompt}', 'stream': False, 'options': {'num_predict': 150}}
            r = requests.post(f'{self.ollama}/api/generate', json=payload, timeout=20)
            return r.json()['response'] if r.status_code == 200 else '❌ Ollama error'
        except Exception as e:
            return f'❌ Ollama offline: {e}'

    async def smart_chat(self, prompt):
        if self.claude:
            print('🧠 Asking real Claude...', end='', flush=True)
            claude_resp = await self.claude_chat(prompt)
            if not claude_resp.startswith('❌'):
                print(f'\r🧠 Claude: {claude_resp[:80]}...')
                return claude_resp
            print(f'\r❌ Claude failed, using Ollama...')
        
        ollama_resp = self.ollama_chat(prompt)
        print(f'🤖 Ollama: {ollama_resp[:80]}...')
        return ollama_resp

    async def run(self):
        print('Commands: /r file, /b cmd, /q   Or chat: How do I...?')
        print('-' * 40)
        while True:
            try:
                inp = input('> ').strip()
                if not inp: continue
                if inp == '/q': break
                elif inp.startswith('/r '): print(self.r(inp[3:]))
                elif inp.startswith('/b '): print(self.b(inp[3:]))
                elif inp == '/l': print(self.b('ls -la'))
                elif inp.startswith('/cd '):
                    try: 
                        os.chdir(Path(inp[4:]).expanduser())
                        self.cwd = Path.cwd()
                        print(f'📁 {self.cwd}')
                    except: print('❌ Bad path')
                else: 
                    response = await self.smart_chat(inp)
                    print(response[:300] + '...' if len(response) > 300 else response)
            except KeyboardInterrupt:
                print('\n⏸️ /q to quit')
            except Exception as e:
                print(f'❌ {e}')

if __name__ == '__main__':
    asyncio.run(ClaudeNotebook().run())
