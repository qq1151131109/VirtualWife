# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

VirtualWife 是一个虚拟数字人项目，支持语音对话、角色扮演、记忆功能和直播互动。项目采用前后端分离架构，后端使用 Django + Channels，前端使用 Next.js + Three.js。

## 核心架构

项目由三个主要服务组成：

1. **domain-chatbot** (后端服务)
   - Django 4.2 + Django REST Framework + Channels (WebSocket)
   - 端口: 8000
   - 主要应用模块位于 `apps/chatbot/` 和 `apps/speech/`

2. **domain-chatvrm** (前端服务)
   - Next.js 13.2.4 + React 18 + Three.js (3D渲染)
   - 端口: 3000 (开发环境)
   - 基于特性的目录结构: `src/features/`

3. **infrastructure-gateway** (网关服务)
   - Nginx 反向代理
   - 端口: 80/443

### 后端核心模块结构

```
domain-chatbot/apps/chatbot/
├── llms/              # LLM模型策略层 (OpenAI, Ollama, ZhipuAI)
├── memory/            # 记忆模块 (Milvus向量存储, Zep, Local)
├── chat/              # 聊天服务核心逻辑
├── character/         # 角色管理
├── emotion/           # 情感控制
├── config/            # 配置管理
├── process/           # 消息处理流程
├── schedule/          # 定时任务
└── insight/           # 洞察分析
```

```
domain-chatbot/apps/speech/
├── tts/               # 文字转语音 (Edge TTS, Bert-VITS2)
├── translation/       # 翻译服务
└── ars/               # 语音识别
```

### 前端核心模块结构

```
domain-chatvrm/src/features/
├── vrmViewer/         # VRM 3D模型渲染
├── messages/          # 消息处理和剧本生成
├── chat/              # 对话接口
├── blivedm/           # B站直播弹幕
├── emoteController/   # 表情控制
├── lipSync/           # 口型同步
├── tts/               # 语音合成
├── config/            # 配置管理
└── media/             # 媒体资源
```

## 常用开发命令

### 本地开发环境设置

**环境要求:**
- Python: 3.10.12
- Node.js: 16.14.2 (chatvrm package.json 指定)
- Conda (推荐用于环境管理)

**初始化开发环境:**
```bash
# 创建 conda 环境
conda create -n vw python=3.10.12
conda activate vw
conda install -c conda-forge nodejs=16.14.2
```

### 后端 (domain-chatbot)

**首次设置:**
```bash
cd domain-chatbot
pip3 install -r requirements.txt

# 初始化数据库
python manage.py makemigrations
python manage.py migrate
```

**启动开发服务器:**
```bash
cd domain-chatbot
python manage.py runserver
```

**Django 常用命令:**
```bash
# 创建数据库迁移
python manage.py makemigrations

# 应用数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 进入 Django Shell
python manage.py shell
```

### 前端 (domain-chatvrm)

**首次设置:**
```bash
cd domain-chatvrm
rm package-lock.json  # 如果遇到依赖问题
npm install
```

**启动开发服务器:**
```bash
cd domain-chatvrm
npm run dev
# 访问 http://localhost:3000/
```

**构建和部署:**
```bash
npm run build          # 生产构建
npm run build:with-lint # 构建并执行 lint
npm run lint          # 代码检查
npm start             # 启动生产服务器
```

### Docker 部署

**启动完整服务:**
```bash
cd installer/linux
sh start.sh
# 访问 http://localhost/
```

**停止服务:**
```bash
cd installer/linux
sh stop.sh
```

**启动 Milvus (向量数据库):**
```bash
cd installer/milvus
sudo docker compose up -d
```

**环境配置:**
- 复制 `installer/env_example` 到 `installer/.env`
- 配置必要的环境变量 (TIMEZONE, CHATBOT_TAG, CHATVRM_TAG, GATEWAY_TAG)

## 关键技术集成

### LLM 模型支持
- OpenAI (GPT系列)
- Ollama (本地私有化模型)
- ZhipuAI (智谱AI)
- 策略模式实现在 `apps/chatbot/llms/llm_model_strategy.py`

### 记忆系统
- **Milvus**: 向量数据库，用于长期记忆和语义检索
- **Zep**: 对话记忆管理
- **Local**: 本地存储实现
- 接口定义在 `apps/chatbot/memory/base_storage.py`

### B站直播集成
- 弹幕监听和互动
- 需要配置: B站直播间ID, 主播UID, B_COOKIE
- 前端集成在 `src/features/blivedm/`

### VRM 模型渲染
- 使用 @pixiv/three-vrm 加载 VRM 模型
- 支持表情控制、动作驱动、口型同步
- 模型可从 https://hub.vroid.com/ 下载

### 语音系统
- **TTS**: Edge TTS (微软), Bert-VITS2
- **ASR**: 语音识别
- 后端实现在 `apps/speech/`

## API 端点

主要 REST API 路径 (参考 `domain-chatbot/apps/chatbot/urls.py`):
- `POST /chatbot/chat` - 聊天接口 (WebSocket)
- `POST /chatbot/memory/clear` - 清空记忆
- `GET /chatbot/config/get` - 获取配置
- `POST /chatbot/config/save` - 保存配置
- `GET /chatbot/customrole/list` - 角色列表
- `POST /chatbot/customrole/create` - 创建角色
- `POST /chatbot/config/vrm/upload` - 上传VRM模型

## Docker 网络配置

使用 Docker 时的特殊配置:
- 访问宿主机服务: `http://host.docker.internal:端口`
- HTTP 代理设置: `HTTP_PROXY=http://host.docker.internal:代理端口`
- Ollama API: `OLLAMA_API_URL=http://host.docker.internal:11434`

## 重要文件位置

- Django设置: `domain-chatbot/VirtualWife/settings.py`
- Docker编排: `installer/docker-compose.yaml`
- 后端依赖: `domain-chatbot/requirements.txt`
- 前端依赖: `domain-chatvrm/package.json`
- 开发文档: `develop.md`
- 常见问题: `FAQ.md`
