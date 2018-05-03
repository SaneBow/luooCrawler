# LuooCrawler

调用落网API爬取期刊信息

特性：

- 支持自定义排序
- 支持iTerm显示封面图片

## 开发动机

落网一直是我的听歌首选，唯一美中不足，落网网页版按时间列出期刊，不支持自定义排序规则，然而手机端支持该功能。

## 使用说明

```text
usage: luoo.py [-h] [-l LIMIT] [-s {fav,new,comment}] [N]

Luoo.net crawler, with support of sorting.

positional arguments:
  N                     page number (default: 0)

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT              vols each page (default: 5)
  -s {fav,new,comment}  sort by (default: fav)
```

## 效果

![screenshot](screenshot.jpg)