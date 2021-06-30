import subprocess
import sys

def copy2clip(txt):
    if sys.platform == 'win32':
        cmd='echo '+txt.strip()+'|clip'
        return subprocess.check_call(cmd, shell=True)
    else:
        cmd='echo '+txt.strip()+'|pbcopy'
        return subprocess.check_call(cmd, shell=True)
    
copy2clip('hellonvioewjgojwe')