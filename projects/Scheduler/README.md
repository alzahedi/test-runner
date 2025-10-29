# Scheduler

<!-- TOC depthfrom:2 -->

- [Context](#context)
- [Poetry](#poetry)
  - [How I was created](#how-i-was-created)
  - [How to configure me](#how-to-configure-me)
- [Call script](#call-script)
- [Download me](#download-and-use-me)
- [Scheduler Modes](#scheduler-modes)
- [Troubleshooting](#troubleshooting)
  - [Connection issue from devcontainer](#connection-issue-from-devcontainer)

<!-- /TOC -->

## Context

 I am a python package for running, scheduling and monitoring multiple tasks. The tasks could be configured with `task group`, `task driver`, `task scheduler` and `failure mode`.

For more details on these modes [click here](#scheduler-modes)

## Poetry

I use [`Poetry`](https://python-poetry.org/), a package management system for Python.

### How I was created

```bash
poetry new Scheduler
```

### How to configure me

```bash
poetry config virtualenvs.in-project true
poetry install
```

So our python interpreter for VSCode is: `/workspaces/DevOps/Scheduler/.venv/bin/python`

To launch Poetry venv from an existing project:

```bash
poetry shell
```

#### NOTE: After making any changes to the source code, please upgrade the version of the package using poetry version commands.
For reference - [poetry-versioning](https://python-poetry.org/docs/cli/#version)

## Call script

To simulate how I'll be invoked and used:

```bash
cd /workspaces/DevOps

# Clean slate
pip uninstall poetry -y

cd Scheduler/scheduler

#Call app.py which is the entry point for the project
python app.py --config "<yaml-file defining task ordering>"

```

One sample YAML file structure that can be used as a reference
```yaml

#   1) waitcurrent: If a task fails, wait for all the running tasks to finish, but don't schedule new tasks.
#   2) failfast: Immediately exit when a task fails.
#   3) waitall: Schedules all tasks, ignoring failures. At the end will exit with error code if any tasks failed.
#   4) runalways : Execute all tasks in a group regardless of any failues from other groups
#

## YAML Level mode, modes define in group override this mode
mode: waitall


groups:
    - Group: GroupOne
      Strategy: sequential
    - Group: GroupTwo
      Strategy: sequential
      Mode: runalways

# tasks specifies the task to run
# - Command: <task command>
#   Name: <task name>
#   Group: <group name>
#   TimeoutInMinutes: <Timeout for the task, defaults to 5 minutes if not given>
#   RunCommandOnTimeout: <Command to run on timeout>
#   
tasks:
     - Command: pwsh script-one.ps1
       Name: Script One
       Group: GroupOne
       TimeoutInMinutes: 5
       RunCommandOnTimeout: python hello-world.py

     - Command: bash script-two.sh
       Name: Script Two
       Group: GroupTwo
       TimeoutInMinutes: 5
       RunCommandOnTimeout: python hello-world.py
 
```

## Download and use me

I am published to the azure feed [scheduler](https://msdata.visualstudio.com/Tina/_artifacts/feed/scheduler) by the pipeline Build scheduler which runs on main branch merge when code inside me changes

One can go the [feed](https://msdata.visualstudio.com/Tina/_artifacts/feed/scheduler) and follow the instructions there to download and use me 

## Scheduler Modes

The scheduler has two built-in scheduling types:

### 1). Sequential

The `sequential` type schedules the grouped tasks in sequence and supports the two `failure mode` types:

- `failfast`: If a task fails, the scheduler will exit with error code immediately.
- `waitall`: If a task fails, the scheduler will still start the rest tasks and exit with error code.

### 2). Parallel

The `parallel` type schedules the grouped tasks in parallel. The maximum parallel degree should be less than the half number of the CPU cores. Also, it supports the three `failure mode` types:

- `waitall`: If a task fails, the scheduler will still start the rest tasks and exit with error.
- `waitcurrent`: If a tasks fails, the scheduler will wait for all running tasks to finish but won't schedule any new tasks.
- `failfast`: If a task fails, the scheduler will exit with error immediately.

Each of the groups can also have a mode defined which will override the root level yaml file mode.
The modes are

- `waitall`: If a task in the group fails, the scheduler will still start the rest of the groups tasks and exit with error.
- `waitcurrent`: If a tasks in the group fails, the scheduler will wait for all running tasks to finish but won't schedule any new groups.
- `failfast`: If a task fails, the scheduler will exit with error immediately.
- `runalways`: If a group has this mode, it will be executed at all times regardless of failures in other group tasks


## Troubleshooting

### Connection issue from devcontainer

**Problem**

Debugging locally via VSCode Devcontainer:

```text
Failed to establish a new connection: [Errno 110] Connection timed out
```

**Solution**

- Reconnect to MSFTVPN
- Rebuild your devcontainer without cache, it should now work
