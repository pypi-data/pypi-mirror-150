import psutil

def getDiskUsage():
    
    """
    空きディスク容量(%)
    """
    
    disk = psutil.disk_usage('/')
    
    return disk.percent

# 空きディスク容量
dskUsage = getDiskUsage()
