> A scp tool based on paramiko

## To install paramiko dependencies on ubuntu 16.04

```shell=
sudo apt-get install -y libssl-dev
sudo apt-get install -y python3-dev
```

## Start

1. set `config.py`
```python=
host = {
    'hostname': '172.0.0.1',
    'user': 'someone',
    'pwd': 'secret'
}
```

2. ssh exectue cmd
```python=
from scptool import ssh_execute

cmd = 'pwd; ls -l'
ssh_execute(cmd)
```

3. scp put file
```
from scptool import scp_put_file

local_file_path = './data'
remote_dir_path = '/home/deploy/'
scp_put_file(local_file_path, remote_dir_path)
```
