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
