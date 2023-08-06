import paramiko
from scp import SCPClient
import io
import shutil
import os

pkey = paramiko.RSAKey.from_private_key(io.StringIO(open('.key', 'r').read()))
server = 'vergil.u.washington.edu'
username = 'arjunsn'
directory = '~/cherryblossom/module'
place_in = './.cherryblossom'

def get_file1(filenames):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, pkey=pkey)
    scp = SCPClient(ssh.get_transport())
    scp.get(directory, place_in, True)
    l = {}
    for filename in filenames:
        with open(os.path.join(place_in, filename), 'r') as f:
            l[filename] = f.read().strip()
    shutil.rmtree(place_in)
    scp.close()
    ssh.close()
    return l

files = ['Analyzer.py',     'Blossom.py',      'Channels.py',     'Chat.py',         'DB.py',           'Data.py',         'Functions.py',    'GPTModel.py',     'Index.py',        'Plots.py',        'Timezone.py',     'imports.py', 'TOS']
f = get_file1(files)

TOS = f['TOS']

def get_file(filename):
    return f[filename]

    