#!/usr/bin/env python
"""
Connect to Jupyter using ssh.

For each Jupyter server running on a compute node, this script creates
an ssh tunnel to the server and opens a notebook on a web browser.
This script assumes that the Jupyter servers were launched using sbatch
(IP addresses and ports of Jupyter servers are parsed from SLURM output files).

To use this script, edit the variables:
* job_name
* user
* host
* open_command

"""

import re
import subprocess

job_name = "jupyter"
user = "chatipat"
host = "midway3.rcc.uchicago.edu"

# open_command = ["open"]  # open with default web browser
# open_command = ["open", "-a", "Firefox"]
# open_command = ["open", "-a", "Google Chrome"]
open_command = ["open", "-a", "JupyterLab", "--args"]  # open with JupyterLab Desktop

ssh_command = ["ssh", f"{user}@{host}"]


def get_job_ids(user, job_name):
    proc = subprocess.run(
        ssh_command
        + ["squeue", "-h", "-u", user, "-n", job_name, "-t", "r", "-o", "%i"],
        capture_output=True,
    )
    job_ids = proc.stdout.decode().split()
    return job_ids


def get_job_info(job_id):
    proc = subprocess.run(
        ssh_command + ["scontrol", "-d", "-o", "show", "job", job_id],
        capture_output=True,
    )
    job_info = {}
    for key_val in proc.stdout.decode().split():
        key_val = key_val.split("=", 1)
        if len(key_val) == 1:
            key_val += [None]
        key, val = key_val
        job_info[key] = val
    return job_info


def parse_jupyter_output(f):
    while True:
        line = next(f)
        if "Or copy and paste one of these URLs" in line:
            break

    p = re.compile(r"http://(\d+\.\d+\.\d+\.\d+):(\d+)/")

    line = next(f)
    m = p.search(line)
    assert m is not None

    remote_ip = m.group(1)
    remote_port = m.group(2)

    line = next(f)
    m = p.search(line)
    assert m is not None

    local_port = m.group(2)

    url = line.strip()

    return (local_port, remote_ip, remote_port), url


def make_tunnel(local_port, remote_ip, remote_port):
    subprocess.run(
        ssh_command
        + ["-f", "-N", "-T", "-L", f"{local_port}:{remote_ip}:{remote_port}"]
    )


def open_jupyter(url):
    subprocess.run(open_command + [url])


def main():
    for job_id in get_job_ids(user, job_name):
        job_info = get_job_info(job_id)

        proc = subprocess.run(
            ssh_command + ["cat", job_info["StdErr"]], capture_output=True
        )
        (local_port, remote_ip, remote_port), url = parse_jupyter_output(
            iter(proc.stdout.decode().split("\n"))
        )
        make_tunnel(local_port, remote_ip, remote_port)
        open_jupyter(url)


if __name__ == "__main__":
    main()
