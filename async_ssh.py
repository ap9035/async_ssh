"""
author: chien-de li
"""

import asyncio
import os

HOME = os.environ['HOME']
SSH_KEY = f"{HOME}/.ssh/id_rsa"


async def ssh_run(hostname, username, command, ssh_key=SSH_KEY):
    """
    ssh login and run command
    """
    shell_command = f"ssh -i {ssh_key} -X {username}@{hostname} '{command}'"
    print(f"start {shell_command}")
    proc = await asyncio.create_subprocess_shell(
        shell_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return stdout.decode()


async def main():
    """
    main function
    """
    task_list = []
    for i in range(5):
        task_list.append(
            ssh_run("asgc-ui03.grid.sinica.edu.tw", "cdli", f"echo HELLO {i}"))
    data_return = await asyncio.gather(*task_list)
    print(data_return)


if __name__ == "__main__":
    asyncio.run(main())
