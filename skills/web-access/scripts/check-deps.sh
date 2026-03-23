#!/usr/bin/env bash
# 环境检查 + 确保 CDP Proxy 就绪

# Node.js
if command -v node &>/dev/null; then
  NODE_VER=$(node --version 2>/dev/null)
  NODE_MAJOR=$(echo "$NODE_VER" | sed 's/v//' | cut -d. -f1)
  if [ "$NODE_MAJOR" -ge 22 ] 2>/dev/null; then
    echo "node: ok ($NODE_VER)"
  else
    echo "node: warn ($NODE_VER, 建议升级到 22+)"
  fi
else
  echo "node: missing — 请安装 Node.js 22+"
  exit 1
fi

# Chrome 调试端口探测（兼容 VPS / OpenClaw browser / 本地 Chrome）
if ! PORT=$(node - <<'EOF'
const net = require('net');
const ports = [18800, 9222, 9229, 9333];
(async () => {
  for (const port of ports) {
    const ok = await new Promise((resolve) => {
      const s = net.createConnection(port, '127.0.0.1');
      const timer = setTimeout(() => { s.destroy(); resolve(false); }, 1500);
      s.on('connect', () => { clearTimeout(timer); s.destroy(); resolve(true); });
      s.on('error', () => { clearTimeout(timer); resolve(false); });
    });
    if (ok) { console.log(port); process.exit(0); }
  }
  process.exit(1);
})();
EOF
); then
  echo "chrome: not connected — 未发现可用调试端口（已检查 18800/9222/9229/9333）"
  exit 1
fi
echo "chrome: ok (port $PORT)"
export WEB_ACCESS_CHROME_PORT="$PORT"

# CDP Proxy — 已运行则跳过，未运行则启动并等待连接
HEALTH=$(curl -s --connect-timeout 2 "http://127.0.0.1:3456/health" 2>/dev/null)
if echo "$HEALTH" | grep -q '"connected":true'; then
  echo "proxy: ready"
else
  if ! echo "$HEALTH" | grep -q '"ok"'; then
    echo "proxy: starting..."
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    node "$SCRIPT_DIR/cdp-proxy.mjs" > /tmp/cdp-proxy.log 2>&1 &
  fi
  for i in $(seq 1 15); do
    sleep 1
    curl -s http://localhost:3456/health | grep -q '"connected":true' && echo "proxy: ready" && exit 0
    [ $i -eq 3 ] && echo "⚠️  Chrome 可能有授权弹窗，请点击「允许」后等待连接..."
  done
  echo "❌ 连接超时，请检查 Chrome 调试设置"
  exit 1
fi
