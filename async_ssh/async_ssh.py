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
    proc = await asyncio.create_subprocess_shell(
        shell_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return stdout.decode()


async def run_on_host(hostname_list, account, command):
    """
    run a command on multiple hosts
    """

    # create event loop
    task_dict = {}
    for hostname in hostname_list:
        task = asyncio.create_task(ssh_run(hostname, account, command))
        task_dict[hostname] = task

    # run concurrently and get result
    result_dict = {}
    for hostname in hostname_list:
        try:
            result = await asyncio.wait_for(task_dict[hostname], 10)
            result_dict[hostname] = result.strip()
        except asyncio.TimeoutError:
            print("timeout")

    return result_dict
