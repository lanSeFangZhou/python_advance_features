# 参考：https://www.liaoxuefeng.com/wiki/1016959663602400/1183565811281984
# 用python来编写脚本简化日常的运维工作是python的一个重要用途。在Linux下，有许多系统命令可以让我们时刻监控系统运行的状态，如ps,top,free等等
# 要获取这些系统信息，Python可以通过subprocess模块调用并获取结果。但这样做显得很麻烦，尤其需要写很多解析代码。

# 在python中获取系统信息的另一个好方法是使用psutil这个第三方模块。顾名思义，psutil = process and system utilities,它不仅可以通过一两行
# 代码实现系统监控，还可以跨平台使用，支持Linux/UNIX/Windows等，是系统管理员和运维小伙伴不可获取的必备模块。

# 安装psutil
# 如果安装了 Anaconda，psutil就已经可用了。否则，需要在命令下通过pip安装：
# pip install psutil
# 如果遇到Permission denied,请加上sodo重试。

# 获取CPU信息
# 我们先来获取CPU信息：
import psutil
print(psutil.cpu_count()) #CPU逻辑数量
print(psutil.cpu_count(logical=False)) # CPU物理核心
# 2说明是双核超线程，4则是4核非超线程

# 统计CPU的用户/系统/空闲时间
print(psutil.cpu_times())

# 再实现类似top命令的CPU使用率，每秒刷新一次，累计10次：
for x in range(10):
    print(psutil.cpu_percent(interval=1, percpu=True))

# 获取内存信息
# 使用psutil获取物理内存和交换内存信息，分别使用：
print(psutil.virtual_memory())
print(psutil.swap_memory())
# 返回的是字节为单位的整数，可以看到，总内存大小为8589934592 = 8GB,可用7201386496 = 6.7GB,使用了66.6%
# 而交换区大小是1073741824 = 1GB

# 获取磁盘信息
# 可以通过psutil获取磁盘分区、磁盘使用率和磁盘IO信息：
print(psutil.disk_partitions()) # 磁盘分区信息
print(psutil.disk_usage('/')) # 磁盘使用情况
psutil.disk_io_counters() # 磁盘IO
# 可以看到，磁盘'/'的总容量是998982549504 = 930GB, 使用了39.1%。文件格式是HFS， opts中包含rw表示可读写， journaled 表示支持日志。

# 获取网络信息
# psutil可以获取网络接口和网络连接信息
print(psutil.net_io_counters()) # 获取网络读写字节/包的个数
print(psutil.net_if_addrs()) # 获取网络接口信息
print(psutil.net_if_stats()) # 获取网络接口状态

# 获取当前网络连接信息，使用net_connections()
print(psutil.net_connections())

# 你可能会得到一个 AccessDenied 错误，原因是psutil获取信息也是要走系统接口，而获取网络连接信息需要root权限，这种情况下，可以退出python
# 交互环境，用sodo重新启动：
# sodo python3
# import psutil
# print(psutil.net_connections())

# 获取进程信息
# 通过psutilk可以获取到所有进程的详细信息：
print(psutil.pids()) # 所有进程id
p = psutil.Process(3776) # 获取指定进程id=3776,其实就是当前python交互环境
print(p.name()) # 进程名称
print(p.exe()) # 进程exe路径
print(p.cwd()) # 进程工作目录
print(p.cmdline()) # 进程启动的命令行
print(p.ppid()) # 父进程id
print(p.parent()) # 父进程
print(p.children()) #子进程列表
print(p.status()) # 进程状态
print(p.username()) # 进程用户名
print(p.create_time()) # 进程创建时间
print(p.terminal()) # 进程终端
print(p.cpu_times()) # 进程使用的CPU时间
print(p.memory_info()) # 进程使用的内存
print(p.open_files()) # 进程打开的文件
print(p.connections()) # 进程相关网络连接
print(p.num_threads()) # 进程的线程数量
print(p.threads()) # 所有线程信息
print(p.environ()) # 进程环境变量
print(p.terminal()) # 结束进程

# 和获取网络连接类似，获取一个root用户的进程需要root权限，启动python交互环境或者.py文件时，需要sudo权限。
# psutil还提供了一个test()函数，可以模拟出ps命令的效果。

# sudo python3
# import psutil
# psutil.test()

# 总结
# psutil使得python程序获取系统信息变得易如反掌
# psutil还可以获取用户信息、windows服务等很多有用的系统信息，具体请参考psutil的官网：https://github.com/giampaolo/psutil
# beamsearch算法
























