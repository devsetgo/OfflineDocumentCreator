import asyncio
from tqdm import tqdm

def variable_computation(iterations):
    result = 0
    for i in range(iterations):
        result += (i ** 0.5) * (i ** 2)
    return result

async def async_task(task_id, duration, complexity):
    for _ in tqdm(range(duration), desc=f"Task {task_id}"):
        # Perform a variable time-consuming computation
        variable_computation(complexity)
        await asyncio.sleep(1)  # Simulating a task

async def main():
    # Initialize 3 async tasks with varying complexity
    tasks = [async_task(i, 5, complexity=1000 * (i + 1)) for i in range(3)]
    await asyncio.gather(*tasks)

# Run the main function
asyncio.run(main())
