# AI Manus 前端

[English](README.md) | 中文

这是一个使用 Vue 3 + TypeScript + Vite 构建的 AI 聊天机器人应用。该项目是从 React 版本移植过来的，保持了同样的功能和界面设计。

## 特性

- 聊天界面
- 工具面板（搜索、文件、终端、浏览器）

## 安装

创建`.env.development`文件，并创建以下配置：

```
# 后端地址
VITE_API_URL=http://127.0.0.1:8000
```

```bash
# 安装依赖
npm install

# 开发模式运行
npm run dev

# 构建生产版本
npm run build
```

## Docker 部署

本项目支持使用 Docker 进行容器化部署：

```bash
# 构建 Docker 镜像
docker build -t ai-chatbot-vue .

# 运行容器（将容器的80端口映射到主机的8080端口）
docker run -d -p 8080:80 ai-chatbot-vue

# 访问应用
# 打开浏览器访问 http://localhost:8080
```

## 项目结构

```
src/
├── assets/          # 静态资源和CSS文件
├── components/      # 可复用组件
│   ├── ChatInput.vue    # 聊天输入组件
│   ├── ChatMessage.vue  # 聊天消息组件
│   ├── Sidebar.vue      # 侧边栏组件
│   ├── ToolPanel.vue    # 工具面板组件
│   └── ui/              # UI组件
├── pages/           # 页面组件
│   ├── ChatPage.vue     # 聊天页面
│   └── HomePage.vue     # 首页
├── App.vue          # 根组件
├── main.ts          # 入口文件
└── index.css        # 全局样式
```
