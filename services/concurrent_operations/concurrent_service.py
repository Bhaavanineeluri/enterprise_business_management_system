import asyncio
import time


async def perform_operation(
    operation_name: str,
    delay: float = 2.0,
) -> dict:
    print(f"Started: {operation_name}")

    await asyncio.sleep(delay)

    print(f"Completed: {operation_name}")

    return {
        "operation": operation_name,
        "status": "completed",
        "delay": delay,
    }


async def run_concurrent_operations(
    operation_names: list[str],
) -> dict:
    start_time = time.perf_counter()

    results = await asyncio.gather(
        *[
            perform_operation(operation_name)
            for operation_name in operation_names
        ]
    )

    elapsed_time = round(
        time.perf_counter() - start_time,
        2,
    )

    return {
        "operations": results,
        "total_time": elapsed_time,
    }
