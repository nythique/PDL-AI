import GPUtil, psutil, platform, logging
from datetime import datetime
from colorama import Fore, Style
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH

info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)



gpus = GPUtil.getGPUs()
for gpu in gpus:
    print(f"GPU {gpu.id} : {gpu.load*100:.1f}% utilisé, {gpu.memoryUsed}MB/{gpu.memoryTotal}MB")

def monitor_system():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_io = psutil.net_io_counters()
        gpus = GPUtil.getGPUs()

        system_info = {
            "timestamp": datetime.now().isoformat(),
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "disk_usage": disk_usage,
            "network_io": {
                "bytes_sent": network_io.bytes_sent,
                "bytes_recv": network_io.bytes_recv
            },
            "gpus": [
                {
                    "id": gpu.id,
                    "load": gpu.load * 100,
                    "memory_used": gpu.memoryUsed,
                    "memory_total": gpu.memoryTotal
                } for gpu in gpus
            ],
            "platform": platform.platform(),
            "processor": platform.processor()
        }
    except Exception as e:
        pass