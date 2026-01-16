#!/usr/bin/env python
"""
VeighNa Trader 启动脚本
解决入口点命令不存在的问题
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_imports():
    """检查必要的导入"""
    try:
        from vnpy.event import EventEngine
        from vnpy.trader.engine import MainEngine
        from vnpy.trader.ui import MainWindow, create_qapp
        print("✓ 所有必要的模块都可以导入")
        return True
    except ImportError as e:
        print(f"✗ 导入错误: {e}")
        return False

def get_available_apps(main_engine):
    """获取可用的应用列表"""
    try:
        # 尝试获取所有应用
        return main_engine.get_all_apps()
    except:
        # 如果失败，返回常用应用列表
        return [
            "DataManager",
            "CtaStrategy", 
            "CtaBacktester",
            "RiskManager",
            "ScriptTrader",
            "AlgoTrading",
            "DataRecorder",
            "ChartWizard",
            "PortfolioStrategy",
            "PortfolioManager",
            "RpcService"
        ]

def main():
    """主启动函数"""
    print("=" * 50)
    print("VeighNa Trader 启动器")
    print("=" * 50)
    
    # 检查导入
    if not check_imports():
        print("\n请确保已正确安装 vnpy:")
        print("pip install vnpy")
        input("按回车键退出...")
        return
    
    try:
        from vnpy.event import EventEngine
        from vnpy.trader.engine import MainEngine
        from vnpy.trader.ui import MainWindow, create_qapp
        
        # 创建Qt应用
        print("\n创建Qt应用...")
        qapp = create_qapp("VeighNa Trader")
        
        # 创建事件引擎
        print("创建事件引擎...")
        event_engine = EventEngine()
        
        # 创建主引擎
        print("创建主引擎...")
        main_engine = MainEngine(event_engine)
        
        # 加载应用模块
        print("\n加载应用模块:")
        print("-" * 30)
        
        available_apps = get_available_apps(main_engine)
        loaded_apps = []
        
        for app_name in available_apps:
            try:
                main_engine.add_app(app_name)
                loaded_apps.append(app_name)
                print(f"  ✓ {app_name}")
            except Exception as e:
                error_msg = str(e)
                if "No module named" in error_msg:
                    print(f"  - {app_name}: 需要单独安装")
                else:
                    print(f"  ✗ {app_name}: {error_msg[:40]}...")
        
        print(f"\n成功加载 {len(loaded_apps)} 个应用")
        
        # 创建主窗口
        print("\n创建主窗口...")
        main_window = MainWindow(main_engine, event_engine)
        main_window.showMaximized()
        
        print("\n" + "=" * 50)
        print("VeighNa Trader 启动成功！")
        print("=" * 50)
        
        # 运行应用
        sys.exit(qapp.exec())
        
    except Exception as e:
        print(f"\n启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()
