# browser-use in OpenClaw VPS

把 `browser-use` 当成 `web-access` 的**高性能浏览器执行层**。

## 什么时候优先用 browser-use

满足任一条就优先考虑：

- 同一任务需要多步连续浏览器动作
- 需要低延迟反复调用浏览器
- 需要稳定保持会话，不想每一步都手写 curl
- 需要命名 session 隔离任务

## 当前环境推荐用法

当前 VPS 上 OpenClaw 自带 Chrome 已暴露 CDP：`http://127.0.0.1:18800`

优先这样调用：

```bash
browser-use --cdp-url http://127.0.0.1:18800 open https://example.com
browser-use --cdp-url http://127.0.0.1:18800 state
browser-use --cdp-url http://127.0.0.1:18800 click 5
browser-use --cdp-url http://127.0.0.1:18800 type "hello"
browser-use --cdp-url http://127.0.0.1:18800 close
```

## 多 session

```bash
browser-use --session work --cdp-url http://127.0.0.1:18800 open https://example.com
browser-use --session work --cdp-url http://127.0.0.1:18800 state
browser-use --session work close
```

## 与 CDP Proxy 的分工

### 优先 browser-use 的场景
- 打开网页后持续 click / type / state
- 表单填写
- 多步交互
- 低延迟连续操作

### 优先 CDP Proxy 的场景
- 自定义 `/eval` 做复杂 DOM 提取
- 直接抓图片 / 视频 URL
- 精细控制特殊页面行为
- 需要自定义 JS 逻辑而不是元素索引点击

## 一句话原则

- **browser-use**：执行链更顺
- **CDP Proxy**：定制控制更细

先判断任务是“连续动作型”还是“定制提取型”，再选工具。
