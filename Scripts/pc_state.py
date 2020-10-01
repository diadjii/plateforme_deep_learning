import psutil
import platform
from datetime import datetime
import schedule
from psutil._common import bytes2human

# let's print CPU information
class  PCState():
    def _init_(self):
        self.data = {}

    def get_info(self):
        self.data['physical_cores'] = psutil.cpu_count(logical=False)
        self.data['total_cores'] = psutil.cpu_count(logical=True)
        cpufreq = psutil.cpu_freq()
        self.data['max_freq'] = f"{cpufreq.max:.2f}Mhz"
        self.data['min_freq'] = f"{cpufreq.min:.2f}Mhz"
        self.data['current_freq'] = f"{cpufreq.current:.2f}"
        self.data['physical_cores'] = psutil.cpu_count(logical=False)
        self.data['total_cores'] = psutil.cpu_count(logical=True)
       
        self.data['ram_usage'] = bytes2human(psutil.virtual_memory().active)
        self.data['ram_total'] =  bytes2human(psutil.virtual_memory().total)
        # CPU usage
        self.data['temperature'] = psutil.sensors_temperatures()
        
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            self.data[f"Core_{i}"] = percentage
            print(f"Core {i}: {percentage}%")
        
        return self.data