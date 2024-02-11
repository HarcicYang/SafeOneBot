<div align="center">
<h1><img src="logo.ico" alt="icon" width="32px"> SafeOneBot</h1>
</div>
<p align="center">转发OneBot SDK的请求，快速解决不规范开发、CQ码不支持的问题，对小白友好、高效、易用</p>
<div align="center">
<img src="https://img.shields.io/badge/OneBot-11-black?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYLBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==" alt="Badge">
<img src="https://img.shields.io/static/v1?label=LICENSE&message=GPL-3.0&color=lightrey" alt="Badge">
</div>


### 概览

SafeOneBot作为中间件，用于解决：

- 不规范开发导致不能与OneBot实现正常对接；
- 框架不支持CQ码导致小白开发困难；
- 小白不会写WebSocket / Websocket对项目结构有所波坏。

### 使用
您可以选择下载源代码或下载[Release](https://github.com/HarcicYang/SafeOneBot/releases)。

SafeOneBot使用JSON作为配置文件。`config.json`内容如下:

```json
{
  "log_level": "INFO",
  "report_url": "http://127.0.0.1:1145",
  "onebot_url": "ws://127.0.0.1:1144",
  "listen_port": "5045",
  "onebot_port": "5044",
  "listen_protocol": "ForwardWebSocket"
}
```

其中：

- `log_level`: 额，应该不用解释吧；
- `report_url`: SafeOneBot向这里上报事件；
- `onebot_url`: SafeOneBot从这里接受事件上报(仅[正向Websocket](https://github.com/botuniverse/onebot-11/blob/master/communication/ws.md))并向这里转发请求；
- `listen_port`: SafeOneBot在这里接受OneBot实现的事件上报 和 返回内容(仅[正向Websocket](https://github.com/botuniverse/onebot-11/blob/master/communication/ws.md))
- `onebot_port`: SafeOneBot会将OneBot SDK的请求向这里转发；
- `listen_protocol`: 与OneBot实现对接使用的协议，目前仅支持`HTTP`和`ForwardWebSocket`。
