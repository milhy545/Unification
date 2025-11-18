#!/usr/bin/env python3
import os,subprocess,json,requests

class MyCoder:
    def __init__(self):
        self.ai='http://192.168.0.41:11434'
        print('⚡ MyCoder - Lightweight Claude Code')
        
    def r(self,f): # read file
        try: return ''.join(f'{i+1:3}: {l}' for i,l in enumerate(open(os.path.expanduser(f)).readlines()[:15]))
        except: return '❌ Error reading file'
        
    def b(self,c): # bash command  
        try: 
            r=subprocess.run(c,shell=True,capture_output=True,text=True,timeout=10)
            return r.stdout if r.returncode==0 else f'❌ {r.stderr[:100]}'
        except: return '❌ Command failed'
        
    def ai(self,p): # AI chat
        try:
            req=requests.post(f'{self.ai}/api/generate',json={'model':'ultra-fast:latest','prompt':f'Help: {p}','stream':False,'options':{'num_predict':50}},timeout=15)
            return req.json()['response'][:100] if req.status_code==200 else '❌ AI error'
        except: return '❌ AI offline'
        
    def run(self):
        print('📋 /r file, /b cmd, /l, /q  Or chat: How do I...?')
        while True:
            try:
                i=input('> ').strip()
                if i=='/q':break
                elif i=='/l':print(self.b('ls -la'))  
                elif i.startswith('/r '):print(self.r(i[3:]))
                elif i.startswith('/b '):print(self.b(i[3:]))
                else:print('🤖',self.ai(i))
            except KeyboardInterrupt:print('\n⏸️ /q to quit')

MyCoder().run()
