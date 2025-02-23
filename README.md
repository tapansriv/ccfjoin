# ccfjoin
instructions/scripts to install and run CCF and launch a javascript app to run a simple join/distinct query. 



Install CCF:
- Make ssh key CHMOD 600
- Install ruby: `sudo apt-get install ruby-full`
- Install open enclave from wget otherwise it’ll install version that’s too old 0.19.4 instead of >=0.19.7
    - WGET the .deb file and then use `sudo dpkg -i <PATH>` 
- run just `./run.sh app-dev.yml --extra-vars "platform=sgx"` from
  `getting_started/setup_vm` which is from the root of the CCF git repo that you
  have to clone
- Update javascript runtime in consortium.py  in bin/infra
    - Find where actions are being created, add one for the javascript runtime
        - Document the values
- Update idle_connection_timeout in config.jinja template used to extend the timeout beyond 60s (I set 3000 seconds and deleted template)
- Gotta set the javascript runtime timeout. The way to do this most quickly is
  to add another proposal around line 195 on consortium.py under /opt/ccf_sgx/bin/infra with the right dict and 
  then adding it to the list of actions that will be proposed
    - https://learn.microsoft.com/en-us/azure/managed-ccf/how-to-update-javascript-runtime-options
    - need to have the max heap size and stack size too (i set these to 5GB each
      on a 30GB RAM machine with 30GB disk via 5 * 1024 * 1024 * 1024 in the
      python file, to make it compute bytes for me and keep it interpretable)
