# py_ts_demux

#### 介绍

python版的tsDemuxer，参考项目：https://github.com/goldvideo/demuxer
目前仅ts流解密
####联系作者:`xuhx20@qq.com`
#### 快速起步

```
pip install ts-demuxer

# 实例化TsDemux对象
ts_demux = TsDemux()

# 传递视频数据进行demux，返回ts数据（包含视频数据及音频数据）
ts_data = ts_demux.start_demux(video_data)

# 获取音频数据
audio_bytes = ts_data.audio_bytes

# 获取视频数据
video_bytes = ts_data.video_bytes
```



