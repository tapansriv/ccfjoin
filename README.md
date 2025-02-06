# ccfjoin
instructions/scripts to install and run CCF and launch a javascript app to run a simple join/distinct query. 



Install CCF:
- Install ruby
- Install open enclave from wget otherwise it’ll install version that’s too old 0.19.4 instead of >=0.19.7
- Update javascript runtime in consortium.py  in bin/infra
    - Find where actions are being created, add one for the javascript runtime
        - Document the values
- Update idle_connection_timeout in config.jinja template used to extend the timeout beyond 60s

