# async_ssh
Async login to server and run command

## Features
- key login
- run commands
- asyncio

## TODO
- [x] ssh_run tool
    - [x] run same command on mutiple machine
    - [x] argparse
        - [x] --nodes
        - [x] --cmd
        - [x] --user
        - [x] --key -k
    - [x] input files(--files -f)
- [ ] add logging package to show debug info
- [ ] add silence mode(-q)
- [ ] password login
- [ ] scp tool and function
- [ ] error handling
    - [ ] timeout
    - [ ] known-host
    - [ ] wrong password?
    - [ ] dns resolve error
- [ ] configure file
    - [ ] default key
    - [ ] default username
- [x] timeout handling
- [x] Add duration time
- [ ] csv mode
- [x] bug, key error when timeout
    - [ ] error handling
