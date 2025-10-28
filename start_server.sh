#!/bin/bash

# 图像数据增强系统启动脚本

cd /home/engine/project

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "检查并安装依赖..."
pip install -q -r requirements.txt

# 停止已有进程
echo "停止已有的服务进程..."
pkill -f "python app.py" 2>/dev/null

# 启动服务
echo "启动服务..."
nohup python app.py > server.log 2>&1 &

sleep 2

# 检查状态
if pgrep -f "python app.py" > /dev/null; then
    echo "✓ 服务启动成功！"
    echo ""
    echo "服务信息："
    echo "- 进程ID: $(pgrep -f 'python app.py')"
    echo "- 监听端口: 5000"
    echo "- 日志文件: $(pwd)/server.log"
    echo ""
    echo "访问地址："
    echo "- 本地访问: http://localhost:5000"
    echo "- 内网访问: http://$(hostname -I | awk '{print $1}'):5000"
    echo ""
    echo "查看日志: tail -f server.log"
    echo "停止服务: pkill -f 'python app.py'"
else
    echo "✗ 服务启动失败，请查看日志: cat server.log"
    exit 1
fi
