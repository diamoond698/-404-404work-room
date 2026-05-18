@echo off
echo 正在启动 Game AI Agent 后端服务...
echo.

:: 检查Python是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请安装Python并添加到环境变量
    pause
    exit /b 1
)

:: 安装依赖（如果需要）
echo 正在检查依赖...
python -m pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    python -m pip install fastapi uvicorn sqlalchemy requests python-dotenv passlib bcrypt
)

echo.
echo 启动服务...
echo 服务将在 http://localhost:8000 启动
echo Swagger文档: http://localhost:8000/docs
echo.

:: 启动服务
python main.py

pause
