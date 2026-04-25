# debug_agent.py
import os
import sys

# 检查Python版本
print(f"Python版本: {sys.version}")
print()

# 检查文件结构
print("=== 检查文件结构 ===")
base_path = r"C:\Users\Lenovo\Desktop\unity瓦片素材\game project"
game_plan_path = os.path.join(base_path, "game_plan")
ai_agent_path = os.path.join(game_plan_path, "ai_agent")

print(f"基础路径: {base_path}")
print(f"game_plan路径: {game_plan_path}")
print(f"ai_agent路径: {ai_agent_path}")
print()

# 检查文件是否存在
print("=== 检查文件存在性 ===")
files_to_check = [
    os.path.join(game_plan_path, "main.py"),
    os.path.join(ai_agent_path, "__init__.py"),
    os.path.join(ai_agent_path, "core.py"),
    os.path.join(ai_agent_path, "tools.py"),
    os.path.join(ai_agent_path, "agent.py"),
    os.path.join(ai_agent_path, "interface.py")
]

for file_path in files_to_check:
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✓ {os.path.basename(file_path)} - {size} 字节")
    else:
        print(f"✗ {os.path.basename(file_path)} - 不存在")
print()

# 检查依赖
print("=== 检查依赖 ===")
try:
    import langchain
    import langchain_community
    import chromadb
    print(f"✓ 依赖安装成功 - LangChain版本: {langchain.__version__}")
except ImportError as e:
    print(f"✗ 依赖缺失: {e}")
print()

print("调试完成！")