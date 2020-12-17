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


async def run_on_host(hostname_list, account, command, ssh_key, timeout=10):
    """
    run a command on multiple hosts
    """

    # create event loop
    task_dict = {}
    for hostname in hostname_list:
        task = asyncio.create_task(ssh_run(hostname, account, command,
                                           ssh_key))
        task_dict[hostname] = task

    # run concurrently and get result
    result_dict = {}
    for hostname in hostname_list:
        try:
            result = await asyncio.wait_for(task_dict[hostname], 10)
            result_dict[hostname] = result.strip()
        except asyncio.TimeoutError:
            print(f"{account}@{hostname} cmd:{command} timeout")

    return result_dict


async def ssh_copy(hostname, username, src, dest="/tmp/", ssh_key=SSH_KEY):
    """
    copy srcs to hosts /tmp/
    """
    shell_command = f"scp -i {ssh_key} {src} {username}@{hostname}:{dest}"
    proc = await asyncio.create_subprocess_shell(
        shell_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return stdout.decode()


async def copy_to_host(hostname_list, account, files, ssh_key):
    """
    run a command on multiple hosts
    """
    # create event loop
    task_dict = {}
    for hostname in hostname_list:
        for file in files:
            task = asyncio.create_task(
                ssh_copy(hostname, account, file, ssh_key=ssh_key))
            task_dict[f"{hostname}-{file}"] = task

    # run concurrently and get result
    result_dict = {}
    for hostname in hostname_list:
        for file in files:
            try:
                result = await asyncio.wait_for(
                    task_dict[f"{hostname}-{file}"], 10)
                result_dict[hostname] = result.strip()
            except asyncio.TimeoutError:
                print(f"copy {file} from local to {hostname}")

    return result_dict
