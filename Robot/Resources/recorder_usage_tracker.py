import psutil
import GPUtil
import time
import pandas as pd
from datetime import datetime

# List of process names to monitor
process_names = ['RecorderManagement.Host.exe', 'RecorderPreview.exe', 'AVEngine.exe']

def get_gpu_usage():
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]  # Assuming a single GPU
        return gpu.load * 100  # GPU load as a percentage
    return 0

def log_process_usage():
    data = []
    while True:
        for process_name in process_names:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == process_name:
                    cpu_usage = proc.cpu_percent(interval=1) / psutil.cpu_count()
                    memory_usage = proc.memory_info().rss / (1024 * 1024)  # Convert to MB
                    gpu_usage = get_gpu_usage()
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data.append([timestamp, process_name, cpu_usage, memory_usage, gpu_usage])
        # Save data to CSV every minute
        df = pd.DataFrame(data, columns=['Timestamp', 'Process', 'CPU_Usage', 'Memory_Usage', 'GPU_Usage'])
        df.to_csv('process_usage.csv', index=False)
        time.sleep(60)

#if __name__ == '__main__':
#    log_process_usage()