# 部署指南 - 将图像数据增强系统部署到 Render.com

本指南将帮助你将这个 Flask 应用免费部署到 Render.com，让它可以在线访问。

## 前提条件

- GitHub 账号
- Render.com 账号（可以使用 GitHub 账号直接登录）

## 部署步骤

### 1. 将代码推送到 GitHub

```bash
# 如果还没有初始化 git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "准备部署到 Render"

# 创建 GitHub 仓库后，添加远程仓库
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 2. 在 Render.com 上部署

1. **访问 Render.com**
   - 打开 https://render.com
   - 使用 GitHub 账号登录

2. **创建新的 Web Service**
   - 点击 "New +" 按钮
   - 选择 "Web Service"
   - 连接你的 GitHub 仓库
   - 选择刚才推送代码的仓库

3. **配置部署设置**

   Render 会自动检测到 `render.yaml` 文件并使用其中的配置。确认以下设置：

   - **Name**: image-augmentation（或你喜欢的名字）
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free（免费套餐）

4. **点击 "Create Web Service"**

   Render 会自动开始构建和部署你的应用。

5. **等待部署完成**

   首次部署可能需要 5-10 分钟。你可以在 Logs 标签页查看部署进度。

6. **访问你的应用**

   部署成功后，Render 会提供一个 URL，类似：
   ```
   https://image-augmentation.onrender.com
   ```

   点击这个 URL 就可以访问你的应用了！

## 重要说明

### 免费套餐限制

- **休眠机制**: 15 分钟无活动后，应用会进入休眠状态
- **唤醒时间**: 休眠后首次访问可能需要 30-60 秒唤醒
- **磁盘存储**: 上传的文件在应用重启后会丢失（临时文件系统）
- **带宽**: 每月 100 GB 免费带宽

### 文件存储问题

由于 Render 免费套餐使用临时文件系统，上传的图片在应用重启后会丢失。如果需要持久化存储，可以考虑：

1. **使用云存储服务**（AWS S3, Cloudinary 等）
2. **升级到 Render 付费套餐**（支持持久化磁盘）

## 故障排查

### 如果部署失败

1. **检查日志**
   - 在 Render 控制台的 Logs 标签页查看错误信息

2. **常见问题**
   - 确保 `requirements.txt` 中所有依赖都正确
   - 确保 `render.yaml` 格式正确
   - 检查 Python 版本兼容性

3. **手动触发重新部署**
   - 在 Render 控制台点击 "Manual Deploy" -> "Deploy latest commit"

## 更新应用

每次你推送新代码到 GitHub，Render 会自动检测并重新部署：

```bash
git add .
git commit -m "更新功能"
git push
```

## 自定义域名（可选）

如果你有自己的域名，可以在 Render 控制台的 "Settings" -> "Custom Domain" 中配置。

## 监控应用

- **查看日志**: Render 控制台 -> Logs
- **查看指标**: Render 控制台 -> Metrics（CPU、内存使用情况）

## 替代方案

如果 Render 不满足需求，还可以考虑：

1. **Railway.app** - 类似的免费托管服务
2. **PythonAnywhere** - 专门的 Python 托管平台
3. **Vercel** - 支持 Python serverless 函数
4. **Heroku** - 需要付费但功能更强大

## 支持

如果遇到问题，可以：
- 查看 Render 文档: https://render.com/docs
- 查看项目 README.md
- 提交 Issue 到 GitHub 仓库
