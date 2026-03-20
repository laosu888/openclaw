# Memory Framework v2

## 分层

### 1. `current-task.md`
只放当前正在做的事，任务完成后可清空或归档。

### 2. `YYYY-MM-DD.md`
只放当天事件、变化、复盘、发布记录。

### 3. `MEMORY.md`
长期稳定信息：人物、规则、长期偏好、长期项目状态。

### 4. `facts.json`
结构化事实，便于快速读取。

### 5. `preferences.json`
稳定偏好，尤其是写作、发布、配图、回复习惯。

## 迁移策略
- 旧 `memory.json` / `vector_memory.json` 先保留，不立刻删除。
- 后续只把“高复用价值”信息迁移到 `facts.json` / `preferences.json`。
- 敏感配置不进入长期公开记忆，继续留在 `memory/private/CONFIG.md` 等私有位置。
