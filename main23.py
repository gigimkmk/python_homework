import asyncio
import time

tasks = [
    ("Downloading data", 3),
    ("Processing data", 2),
    ("Sending notification", 1),
    ("Saving results", 4),
]


async def do_task(name, seconds):
    print(f"{name} started")
    await asyncio.sleep(seconds)
    print(f"{name} finished")
    return f"{name} completed"


async def run_sequential():
    results = []

    start = time.perf_counter()

    for name, seconds in tasks:
        result = await do_task(name, seconds)
        results.append(result)

    end = time.perf_counter()

    print("\nResults:", results)
    print(f"Sequential execution time: {end - start:.2f} seconds\n")


 
async def run_concurrent():
    start = time.perf_counter()

    coroutines = [do_task(name, seconds) for name, seconds in tasks]
    results = await asyncio.gather(*coroutines)

    end = time.perf_counter()

    print("\nResults:", results)
    print(f"Concurrent execution time: {end - start:.2f} seconds")


async def main():
    print("=== Sequential Execution ===")
    await run_sequential()

    print("\n=== Concurrent Execution ===")
    await run_concurrent()


asyncio.run(main())