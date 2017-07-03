import os
import paramiko
from scp import SCPClient
from config import host

def ssh_execute(cmd, host=host):
    """
    INPUT:
    cmd = 'ls -la /home/deploy/'
    host = {
        'hostname': '172.0.0.1',  # Ensure host works in ssh
        'user': 'someone', 
        'pwd': 'secret'
    } 
    
    OUTPUT:
    ================================================================================
    [Info]
    someone@172.0.0.1

    [Execute]
    ls -la /home/

    [Output]
    total 16
    drwxr-xr-x  4 root   root   4096 May  8 17:20 .
    drwxr-xr-x 24 root   root   4096 May 17 08:59 ..
    drwxr-xr-x 11 deploy deploy 4096 May 26 13:31 deploy
    """
    def to_string(std):
        return str(std.read().decode('utf-8').strip())

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host['hostname'], username=host['user'], password=host['pwd'])

        execute_infos = ['='*80,
                         '[Info]\n{}\n'.format(host['user']+'@'+host['hostname']),
                         '[Execute]\n{}\n'.format(cmd)]
        print('\n'.join(execute_infos))

        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout = to_string(stdout)
        stderr = to_string(stderr)

        if len(stdout)>0:
            print('[Output]\n{}\n'.format(stdout))
            return stdout

        if len(stderr)>0:
            print('[Error]\n{}\n'.format(stderr))

def scp_put_file(local_path, remote_path, host=host, recursive=False):
    """
    INPUT:
    local_path = './data'
    remote_path = '/home/deploy/'
    host = {
        'hostname': '172.0.0.1',  # Ensure host works in ssh
        'user': 'someone', 
        'pwd': 'secret'
    }
    
    OUTPUT:
    ================================================================================
    [Put] (local_path)
    ./data

    [To] (remote_path)
    someone@172.0.0.1:/home/deploy/
    """
    def print_output():
        print('='*80)
        print('[Put] (local_path)')

        if isinstance(local_path, list):
            for f in local_path:
                print(f)
        else:
            print(local_path)
            
        print('\n[To] (remote_path)')
        print('{info}:{remote_path}\n'.format(info=host['user']+'@'+host['hostname'],
                                              remote_path=remote_path))
    
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host['hostname'], username=host['user'], password=host['pwd'])
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_path, remote_path, recursive=recursive)
            print_output()


def scp_get_file(remote_path, local_path, host=host, recursive=False):
    """
    INPUT:
    remote_path = '/data/'
    local_path = './'
    host = {
        'hostname': '172.0.0.1',  # Ensure host works in ssh
        'user': 'someone',
        'pwd': 'secret'
    }
    
    OUTPUT:
    ================================================================================
    [Get] (remote_path)
    someone@172.0.0.1:/data/


    [To] (local_path)
    ./
    """
    def print_output():
        print('='*80)
        print('[Get] (remote_path)')
        print('{info}:{remote_path}\n'.format(info=host['user']+'@'+host['hostname'],
                                              remote_path=remote_path))
        print('\n[To] (local_path)')
        if isinstance(local_path, list):
            for f in local_path:
                print(f)
        else:
            print(local_path)

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host['hostname'], username=host['user'], password=host['pwd'])

        with SCPClient(ssh.get_transport()) as scp:
            scp.get(remote_path, local_path, recursive=recursive)
            print_output()

