# 快速上手

本文档帮助你快速部署和运行 AI Manus。

## 环境要求

### Docker 环境

- Docker 20.10+
- Docker Compose v2

### 模型要求

AI Manus 需要使用兼容 OpenAI 接口的大语言模型：

- 支持 FunctionCall (工具调用)
- 支持 JSON Format 输出

推荐模型：
- DeepSeek (deepseek-chat)
- OpenAI GPT-4o / GPT-4-turbo
- Claude 3.5 Sonnet (通过兼容层)

## 安装 Docker

### Windows / macOS

安装 Docker Desktop: https://docs.docker.com/desktop/

### Linux

安装 Docker Engine: https://docs.docker.com/engine/

验证安装：

```bash
docker --version
docker compose version
```

## 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/nuoyimanaituling/manus-x.git
cd manus-x
```

### 2. 配置环境变量

复制示例配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置必要参数：

```bash
# LLM 配置（必填）
API_KEY=your-api-key
API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-4o

# 认证配置
AUTH_PROVIDER=none  # 可选: none, local, password
```

### 3. 启动服务

```bash
./run.sh up -d
```

等待所有镜像拉取完成后，访问 http://localhost:5173 即可使用。

> 提示：如果看到 `sandbox-1 exited with code 0` 这是正常的，sandbox 容器仅用于预拉取镜像。

### 4. 停止服务

```bash
./run.sh down
```

## 配置说明

### LLM 配置

| 变量 | 说明 | 示例 |
|------|------|------|
| `LLM_PROVIDER` | LLM 提供商 | `openai` / `anthropic` |
| `API_KEY` | API 密钥 | `sk-xxxx` |
| `API_BASE` | API 地址 | `https://api.openai.com/v1` |
| `MODEL_NAME` | 模型名称 | `gpt-4o` |
| `TEMPERATURE` | 温度参数 | `0.7` |
| `MAX_TOKENS` | 最大 token | `2000` |

### 认证配置

| AUTH_PROVIDER | 说明 |
|---------------|------|
| `none` | 无需认证，直接使用 |
| `local` | 本地账户认证 |
| `password` | 邮箱密码认证 |

本地认证配置示例：

```bash
AUTH_PROVIDER=local
LOCAL_AUTH_EMAIL=admin@example.com
LOCAL_AUTH_PASSWORD=admin
```

### 搜索引擎配置

| 变量 | 说明 |
|------|------|
| `SEARCH_PROVIDER` | 搜索引擎: `bing` / `google` / `baidu` |
| `GOOGLE_SEARCH_API_KEY` | Google 搜索 API 密钥 |
| `GOOGLE_SEARCH_ENGINE_ID` | Google 搜索引擎 ID |

### Sandbox 配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SANDBOX_IMAGE` | 沙箱镜像 | `dockerdockerdockerxzw/manus-sandbox` |
| `SANDBOX_TTL_MINUTES` | 容器存活时间(分钟) | `30` |
| `SANDBOX_NETWORK` | Docker 网络 | `manus-network` |

## 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Frontend | 5173 | Web 界面 |
| Backend | 8000 | API 服务 |
| MongoDB | 27017 | 数据库 |
| Redis | 6379 | 缓存 |

## 开发模式

如需进行开发调试，使用开发脚本：

```bash
# 启动开发环境（支持热重载）
./dev.sh up

# 查看日志
./dev.sh logs -f backend

# 停止服务
./dev.sh down
```

## 常见问题

### 镜像拉取慢

可配置 Docker 镜像加速器，或使用代理：

```bash
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
docker compose pull
```

### Sandbox 无法启动

确保 Docker socket 挂载正确：

```bash
ls -la /var/run/docker.sock
```

如使用 Docker Desktop，确保已开启 socket 共享。

### 模型调用失败

检查以下配置：
1. API_KEY 是否正确
2. API_BASE 是否可访问
3. 模型是否支持 FunctionCall

### 查看日志

```bash
# 查看所有服务日志
./run.sh logs -f

# 查看特定服务
./run.sh logs -f backend
```

## 下一步

- 阅读 [系统架构](architecture.md) 了解整体设计
- 查看 [配置说明](configuration.md) 了解完整配置
