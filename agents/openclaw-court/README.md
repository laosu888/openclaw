# OpenClaw 五角色 MVP 架构

这套架构把复杂任务拆成 5 个固定职责角色，避免所有事情都挤在一个主会话里。

## 角色
- `taizi`：入口分拣
- `zhongshu`：任务规划
- `menxia`：方案审查
- `shangshu`：任务协调
- `hubu`：数据执行

## 适用场景
- 足球单场分析
- ETH / 金十 / 新闻
- 公众号写作与发布
- 技能开发与流程自动化

## 推荐调用链
1. 用户消息进入主会话
2. 主会话按需调用 `taizi.md` 做分拣
3. 复杂任务交给 `zhongshu.md` 拆解
4. 高风险或容易打架的方案交给 `menxia.md` 审
5. `shangshu.md` 决定派发顺序
6. `hubu.md` 负责拉数据和结构化输出

## 足球分析建议调用链
用户提比赛 -> taizi -> zhongshu -> hubu -> menxia -> shangshu -> 主会话输出
