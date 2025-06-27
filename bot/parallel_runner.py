import multiprocessing
import time
from clone_utils import clone_instance, launch_instance
from run_instance import run_cycle
from config import BASE_INSTANCE, TOTAL_ACCOUNTS, INSTANCES_PER_BATCH

def prepare_batch(batch_num):
    instance_names = []
    for i in range(INSTANCES_PER_BATCH):
        new_name = f"LDPlayer-{(batch_num - 1) * INSTANCES_PER_BATCH + i + 1}"
        clone_instance(BASE_INSTANCE, new_name)
        launch_instance(new_name)
        instance_names.append(new_name)
    return instance_names

def run_batch(batch_num, start_guest_index):
    instance_names = prepare_batch(batch_num)
    time.sleep(40)
    device_ids = [f"emulator-555{i}" for i in range(len(instance_names))]

    jobs = []
    for i, (name, device) in enumerate(zip(instance_names, device_ids)):
        guest_index = start_guest_index + i
        p = multiprocessing.Process(target=run_cycle, args=(name, device, guest_index))
        p.start()
        jobs.append(p)

    for p in jobs:
        p.join()

if __name__ == "__main__":
    total_batches = TOTAL_ACCOUNTS // INSTANCES_PER_BATCH
    guest_index = 1

    for batch in range(1, total_batches + 1):
        print(f"\n🚀 Starting batch {batch}")
        run_batch(batch, guest_index)
        guest_index += INSTANCES_PER_BATCH
