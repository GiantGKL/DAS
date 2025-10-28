# 访问指南

## 🚀 项目已启动

Flask应用已经成功运行在端口 **5000** 上。

## 📍 访问方式

### 方式一：本地访问（仅限VM内部）
```
http://localhost:5000
http://127.0.0.1:5000
```

### 方式二：内网访问
```
http://10.16.6.120:5000
```
**注意：** 这个IP地址是VM的内部IP，只能在同一网络内访问。

### 方式三：通过端口转发访问（推荐）

如果你在本地机器上无法访问VM的端口，你需要设置端口转发：

#### SSH端口转发
如果你通过SSH连接到这个VM，可以使用端口转发：

```bash
# 在你的本地机器上执行
ssh -L 5000:localhost:5000 user@vm-host
```

然后在本地浏览器访问：`http://localhost:5000`

#### VS Code端口转发
如果你使用VS Code Remote连接：
1. 打开命令面板（Ctrl+Shift+P 或 Cmd+Shift+P）
2. 输入 "Forward a Port"
3. 输入端口号：5000
4. 访问 `http://localhost:5000`

## 🔧 服务管理

### 启动服务
```bash
bash start_server.sh
```

### 查看服务状态
```bash
ps aux | grep "python app.py" | grep -v grep
```

### 查看实时日志
```bash
tail -f server.log
```

### 停止服务
```bash
pkill -f "python app.py"
```

### 重启服务
```bash
pkill -f "python app.py" && bash start_server.sh
```

## 🌐 测试连接

在VM内测试服务是否正常：
```bash
curl http://localhost:5000
```

## 📦 功能说明

这是一个**图像数据增强Web应用**，提供以下功能：

- ✅ 图像上传（支持拖拽）
- ✅ 随机旋转
- ✅ 随机翻转
- ✅ 随机裁剪
- ✅ 随机缩放
- ✅ 颜色抖动
- ✅ 增强效果预览
- ✅ 批量处理
- ✅ 下载增强后的图像

## ❓ 常见问题

### Q: 为什么我无法从浏览器访问？
A: 如果你的浏览器不在VM内，你需要使用端口转发或VPN来访问VM的端口。

### Q: 服务突然停止了怎么办？
A: 运行 `bash start_server.sh` 重新启动服务。

### Q: 如何查看错误信息？
A: 查看日志文件：`cat server.log` 或 `tail -f server.log`

### Q: 端口5000被占用怎么办？
A: 修改 `app.py` 中的端口号，或设置环境变量：
```bash
export PORT=8080
bash start_server.sh
```

## 🔒 安全提示

这是一个开发服务器，**不建议在生产环境中使用**。如果需要在生产环境部署，请使用生产级WSGI服务器（如gunicorn或uwsgi）。

## 当前服务状态

✅ **服务正在运行**
- 进程ID: $(pgrep -f 'python app.py' 2>/dev/null || echo "未运行")
- 监听地址: 0.0.0.0:5000
- 访问地址: http://localhost:5000
