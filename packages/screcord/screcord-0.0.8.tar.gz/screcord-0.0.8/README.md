# screcord

一个手机屏幕录制库，基于python3.6+，支持安卓系统和iOS系统，详细原理见 [#Python移动端录屏库](https://www.cnblogs.com/freedomlidi/p/13199790.html)

# 操作系统

因为底层录制工具，安卓端使用[scrcpy](https://github.com/Genymobile/scrcpy)，iOS端使用[xrecord](https://github.com/WPO-Foundation/xrecord)，所以操作系统依赖与底层工具保持一致即可。
通常iOS手机录屏需要使用`MacOS`系统，安卓手机录屏使用`Win、MacOS、Linux`皆可

# 快速使用

第一步，安装`screcord`库，要求py3.6+

```sh
pip3 install screcord
```

第二步，安装底层录制工具依赖

* 录制安卓手机，需要安装[scrcpy](https://github.com/Genymobile/scrcpy)，具体安装方法参考见[scrcpy#summary](https://github.com/Genymobile/scrcpy#summary)
* 录制iOS手机，无需安装依赖，已经内置在`screcord`库里，见[可执行文件xrecord](/screcord/xrecord)

第三步，在需要录制的case上引入`record`这个装饰器即可，可参考[example/demo.py](/example/demo.py)

> record 方法入参格式如下：
> 
> * platform - 安卓/iOS可缩写为：`a`/`i`
> * file_path - 录屏视频的文件路径，建议mp4格式
> * offset - 偏移量，tuple类型，表示录屏开始后，在case开始前等待几秒，case执行完等待几秒，通常用于case前后的等待缓冲期
> * pre_kill - 在开始录屏前是否需要kill掉已有的进程

```py
from screcord import record

# 安卓端
device_id = "xxxxx"
video_fp = "./demo.mp4"
@record('android', device, video_fp, offset=(1, 2))
def start_app():
    # your case
    ......
    
# iOS端
udid = "xxxxx"
video_fp = "./demo.mp4"
@record('ios', udid, video_fp, offset=(1, 1), pre_kill=False)
def start_app():
    # your case
    ......
```

值得注意的是：

* 因为`scrcpy`同一时刻只允许一个进程运行，所以安卓端建议将pre_kill置为True
* iOS端建议将pre_kill置为False，因为每次启动`xrecord`时候都会重连设备，这会导致`WDA自动化测试`中断

# 常见问题

## 运行demo

正确运行[demo.py](/example/demo.py)方式如下
1. 连接设备，修改device为自己手机的device_id/udid
2. 在终端（如：iterm2、cmd等）执行：`cd screcord/example ; python3 demo.py`
    ```bash
    ➜  example git:(master) ✗ python3 demo.py
    2021-11-18 19:18:51.759 | INFO     | screcord:_update_offset:128 - current case offset: (2, 1)
    2021-11-18 19:18:51.759 | INFO     | screcord:_cmd:111 -
    ===== CMD INFO =====
    platform: ios
    name: xrecord
    cmd: "/usr/local/lib/python3.7/site-packages/screcord/xrecord" -q -i="00008020-001D1D900CB9002E" -o="./demo2.mp4" -f
    ====================
    2021-11-18 19:18:51.812 | INFO     | screcord:start:57 - ========= START RECORD ==========
    5
    4
    3
    2
    1
    2021-11-18 19:18:59.838 | INFO     | screcord:stop:69 - ========== STOP RECORD ==========
    ```
3. 录制结束后会在`example`目录下生成`demo1.mp4`或`demo2.mp4`文件

## 安卓端

1. 安卓手机录制失败请先检查`scrcpy`是否已经正常安装，并配置好环境变量，配置正常执行以下命令展示如下
    ```bash
    (venv) ➜  screcord git:(master) ✗ scrcpy -v
    scrcpy 1.10
    
    dependencies:
     - SDL 2.0.9
     - libavcodec 58.35.100
     - libavformat 58.20.100
     - libavutil 56.22.100
    ```

## iOS端

2. iOS手机录制报错先检查`Quicktime`是否打开正常，详情见[运行报错 #3](https://github.com/ssfanli/screcord/issues/3)
3. iOS手机录制需在终端上运行，不能在IDE下运行，原因见[Using IntelliJ IDEA command line tool, xrecord process is killed #13
](https://github.com/WPO-Foundation/xrecord/issues/13)
4. iOS端录屏会中断WDA，解决方案见[pre_kill置为False，iOS端录屏会中断WDA #5](https://github.com/ssfanli/screcord/issues/5)


