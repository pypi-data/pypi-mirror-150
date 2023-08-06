# -*- coding:utf-8 -*-
from ts_demuxer import TsDemux


if __name__ == '__main__':
    # 读取ts文件字节数据
    video_data = open('test.ts', 'rb').read()
    # 实例化TsDemux对象
    ts_demux = TsDemux()
    # 传递视频数据进行demux，返回ts数据（包含视频数据及音频数据）
    ts_data = ts_demux.start_demux(video_data)
    # 获取音频数据
    audio_bytes = ts_data.audio_bytes
    # 获取视频数据
    video_bytes = ts_data.video_bytes

    # 写入文件进行查看测试
    open('test_demux.mp3', 'wb').write(audio_bytes)
    open('test_demux.ts', 'wb').write(video_bytes)
