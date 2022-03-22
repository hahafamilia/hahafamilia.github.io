---
layout: default
parent: development
title: FFMPEG를 이용해 음악 플레이리스트 동영상 만들기
tags: 
    - 2019
    - ffmpeg
    - ffmpeg-music-youtube
---

음원의 플레이리스트를 앨범 자켓 이미지를 포함시켜 동영상으로 만들 수 있나요? 
라는 얘기를 듣게 되었어요.
의도는 Youtube 에는 음악등록을 할 수 없어서, 동영상으로 만들어서 업로드 해야된다고 하네요.

그래서 간단하게 프로토타입을 만들어 봤어요. FFMPEG 검색을 해보니 이러한 시도를 하는 분들이 꽤 있나 보군요.

### 프로토타입 
1. 하나의 음원을 이미지를 포함시켜 동영상으로 제작
1. 각 동영상들을 이어 붙히기
```bash
ffmpeg -loop 1 -i Happy.jpg -i Happy.mp3 -shortest -acodec copy 2.mp4
ffmpeg -loop 1 -i StellaJang.jpg -i StellaJang.mp3 -shortest -acodec copy 1.mp4

echo "file 1.mp4" > playlist.txt
echo "file 2.mp4" >> playlist.txt

ffmpeg -f concat -i playlist.txt -c copy playlist.mp4
```
