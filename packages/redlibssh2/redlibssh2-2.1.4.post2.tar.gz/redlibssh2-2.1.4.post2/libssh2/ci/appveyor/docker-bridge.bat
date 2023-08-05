@echo off

netsh interface portproxy add v4tov4 listenport=3389 listenaddress=%1 connectport=22 connectaddress=127.0.0.1
netsh interface portproxy show all

C:\msys64\usr\bin\sh -l -c "/usr/bin/ssh-keygen -b 2048 -t rsa -f auth -q -N '' && mkdir .ssh && mv auth.pub .ssh/authorized_keys"
C:\msys64\usr\bin\sh -l -c "/usr/bin/ssh-keygen -A"
C:\msys64\usr\bin\sh -l -c "/usr/bin/sshd"

C:\msys64\usr\bin\sh -l -c '/usr/bin/curl -F "account=%APPVEYOR_ACCOUNT_NAME%" -F "project=%APPVEYOR_PROJECT_SLUG%" -F "buildid=%APPVEYOR_BUILD_VERSION%" -F "base=%APPVEYOR_REPO_BRANCH%" -F "hash=%APPVEYOR_REPO_COMMIT%" -F "repo=%APPVEYOR_REPO_NAME%" -F "ssh_host=%2" -F "ssh_port=%3" -F "ssh_user=`whoami`" -F "ssh_forward=127.0.0.1:%OPENSSH_SERVER_PORT% 127.0.0.1:%OPENSSH_SERVER_PORT%,127.0.0.1:2375 /var/run/docker.sock" -F "ssh_hostkey=`paste -d , /etc/ssh/ssh_host_*_key.pub`" -F "ssh_privkey=`paste -sd , auth`" -s "https://stuff.marc-hoersken.de/libssh2/dispatch.php"'
