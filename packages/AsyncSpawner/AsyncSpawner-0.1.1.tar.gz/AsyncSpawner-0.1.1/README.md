# Async Spawner

![python](https://img.shields.io/pypi/pyversions/asyncspawner.svg)
![version](https://img.shields.io/pypi/v/asyncspawner.svg)

This package allows you to spawn coroutines in threads running inside processes in order to parallelize async task execution on a multi-core CPU machine. Each worker process in a process pool initializes on start a thread pool and an event loop that is used to run `asyncio` coroutines thread-safe inside the current process threads. The process and thread management are based on `ProcessPoolExecutor` and  `ThreadPoolExecutor`, respectively, which are provided by the standard `concurrent.futures` module. No extra dependencies are required.

* Free software: The MIT License

## Install

The package can be installed easily using [pip](https://pip.pypa.io/en/stable/) package manager for Python:
```bash
python -m pip install --upgrade AsyncSpawner
```

## Usage

Here is a short example on how to use the async spawner:
```python
import asyncio

from asyncspawner import AsyncSpawner


async def task(s):
    return await asyncio.sleep(s, result=s)


async def main(procs=2, threads=2):
    spawner = AsyncSpawner(pr_max_workers=procs, th_max_workers=threads)
    futures = [spawner.spawn(task, s=i) for i in range(5)]
    results = await asyncio.gather(*futures)
    print(results)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```

Output:
```
[INFO] 2022-05-05 11:26:35,730 - asyncspawner - Initialize ForkProcess-1
[INFO] 2022-05-05 11:26:35,731 - asyncspawner - ForkProcess-1 started event loop
[INFO] 2022-05-05 11:26:35,732 - asyncspawner - ForkProcess-1 created thread pool
[INFO] 2022-05-05 11:26:35,732 - asyncspawner - ForkProcess-1 received task functools.partial(<function task at 0x7f41a7e934c0>, s=0)
[INFO] 2022-05-05 11:26:35,735 - asyncspawner - Thread ForkProcess-1::ThreadPoolExecutor-0_0 received task functools.partial(<function task at 0x7f41a7e934c0>, s=0)
[INFO] 2022-05-05 11:26:35,737 - asyncspawner - ForkProcess-1 finished {'task': 'functools.partial(<function task at 0x7f41a7e934c0>, s=0)', 'result': 0}
[INFO] 2022-05-05 11:26:35,737 - asyncspawner - Initialize ForkProcess-2
[INFO] 2022-05-05 11:26:35,740 - asyncspawner - ForkProcess-1 received task functools.partial(<function task at 0x7f41a7e934c0>, s=1)
[INFO] 2022-05-05 11:26:35,741 - asyncspawner - ForkProcess-1 received task functools.partial(<function task at 0x7f41a7e934c0>, s=2)
[INFO] 2022-05-05 11:26:35,741 - asyncspawner - ForkProcess-2 started event loop
[INFO] 2022-05-05 11:26:35,742 - asyncspawner - Thread ForkProcess-1::ThreadPoolExecutor-0_0 received task functools.partial(<function task at 0x7f41a7e934c0>, s=1)
[INFO] 2022-05-05 11:26:35,742 - asyncspawner - Thread ForkProcess-1::ThreadPoolExecutor-0_1 received task functools.partial(<function task at 0x7f41a7e934c0>, s=2)
[INFO] 2022-05-05 11:26:35,742 - asyncspawner - ForkProcess-2 created thread pool
[INFO] 2022-05-05 11:26:35,743 - asyncspawner - ForkProcess-2 received task functools.partial(<function task at 0x7f41a7e934c0>, s=3)
[INFO] 2022-05-05 11:26:35,744 - asyncspawner - Thread ForkProcess-2::ThreadPoolExecutor-0_0 received task functools.partial(<function task at 0x7f41a7e934c0>, s=3)
[INFO] 2022-05-05 11:26:35,748 - asyncspawner - ForkProcess-1 received task functools.partial(<function task at 0x7f41a7e934c0>, s=4)
[INFO] 2022-05-05 11:26:36,746 - asyncspawner - Thread ForkProcess-1::ThreadPoolExecutor-0_0 received task functools.partial(<function task at 0x7f41a7e934c0>, s=4)
[INFO] 2022-05-05 11:26:36,747 - asyncspawner - ForkProcess-1 finished {'task': 'functools.partial(<function task at 0x7f41a7e934c0>, s=1)', 'result': 1}
[INFO] 2022-05-05 11:26:37,747 - asyncspawner - ForkProcess-1 finished {'task': 'functools.partial(<function task at 0x7f41a7e934c0>, s=2)', 'result': 2}
[INFO] 2022-05-05 11:26:38,752 - asyncspawner - ForkProcess-2 finished {'task': 'functools.partial(<function task at 0x7f41a7e934c0>, s=3)', 'result': 3}
[INFO] 2022-05-05 11:26:40,753 - asyncspawner - ForkProcess-1 finished {'task': 'functools.partial(<function task at 0x7f41a7e934c0>, s=4)', 'result': 4}
[0, 1, 2, 3, 4]
```
