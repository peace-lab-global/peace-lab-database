#!/usr/bin/env python3
"""
自动化部署和维护脚本
功能：一键安装依赖、初始化系统、定时任务设置
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """安装必要的Python依赖"""
    requirements = [
        "whoosh>=2.7.4",
        "PyYAML>=6.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "jinja2>=3.0.0"
    ]
    
    print("正在安装依赖包...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"✗ {package} 安装失败")

def initialize_system():
    """初始化系统配置"""
    print("正在初始化系统...")
    
    # 创建必要的目录
    dirs_to_create = ["index", "reports", "logs", "backups"]
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ 创建目录: {dir_name}")
    
    # 复制配置模板
    config_template = """
# 知识库管理系统配置文件
knowledge_base_path: "."
index_path: "index"
reports_path: "reports"
auto_backup: true
backup_frequency: "daily"
quality_threshold: 80
    """
    
    config_file = Path("config.yaml")
    if not config_file.exists():
        config_file.write_text(config_template.strip())
        print("✓ 创建配置文件")
    
    print("系统初始化完成！")

def setup_cron_jobs():
    """设置定时任务（Linux/Mac）"""
    cron_commands = [
        "# 知识库自动维护任务",
        "0 2 * * * cd $(pwd) && python3 quality_checker.py >> logs/quality_check.log 2>&1",
        "0 3 * * * cd $(pwd) && python3 doc_analyzer.py >> logs/analysis.log 2>&1",
        "0 4 * * 1 cd $(pwd) && python3 dashboard.py >> logs/dashboard.log 2>&1"
    ]
    
    try:
        # 获取当前用户的crontab
        current_crontab = subprocess.check_output(["crontab", "-l"], stderr=subprocess.DEVNULL).decode()
        
        # 添加新任务
        new_crontab = current_crontab + "\n" + "\n".join(cron_commands) + "\n"
        
        # 更新crontab
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE)
        process.communicate(input=new_crontab.encode())
        
        print("✓ 定时任务设置成功")
        print("已添加以下任务:")
        for cmd in cron_commands[1:]:
            print(f"  {cmd}")
            
    except Exception as e:
        print(f"✗ 定时任务设置失败: {e}")
        print("请手动添加crontab任务")

def main():
    """主函数"""
    print("🧠 知识库管理系统部署工具")
    print("=" * 40)
    
    while True:
        print("\n请选择操作:")
        print("1. 安装依赖包")
        print("2. 初始化系统")
        print("3. 设置定时任务")
        print("4. 执行完整部署")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == "1":
            install_dependencies()
        elif choice == "2":
            initialize_system()
        elif choice == "3":
            setup_cron_jobs()
        elif choice == "4":
            print("开始完整部署...")
            install_dependencies()
            initialize_system()
            setup_cron_jobs()
            print("✅ 部署完成！")
        elif choice == "5":
            print("再见！")
            break
        else:
            print("无效选项，请重新选择")

if __name__ == "__main__":
    main()