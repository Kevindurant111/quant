#!/usr/bin/env python
"""
VeighNa Trader 完整启动脚本 (适配 vnpy >= 4.0.0 模块化版本)
最后更新: 2024-06
"""

import sys
import traceback

def main():
    print("=" * 60)
    print("VeighNa Trader 启动器")
    print("版本: 适配 vnpy 4.0.0+ 模块化架构")
    print("=" * 60)

    # 第1步：检查核心模块
    print("\n[1/4] 检查核心模块...")
    try:
        from vnpy.event import EventEngine
        from vnpy.trader.engine import MainEngine
        from vnpy.trader.ui import MainWindow, create_qapp
        print("  ✓ 核心引擎与UI模块导入成功")
    except ImportError as e:
        print(f"  ✗ 核心模块导入失败: {e}")
        print("\n请确保已安装 vnpy 核心包:")
        print("  pip install vnpy")
        input("\n按回车键退出...")
        return

    # 第2步：尝试导入功能应用
    print("\n[2/4] 导入功能应用模块...")
    apps_to_try = []
    
    # 数据管理
    try:
        from vnpy_datamanager import DataManagerApp
        apps_to_try.append(("DataManager", DataManagerApp, "vnpy_datamanager"))
        print("  ✓ 找到 DataManagerApp")
    except ImportError:
        print("  ✗ 未找到 vnpy_datamanager")
        print("     安装: pip install vnpy_datamanager")
    
    # CTA策略
    try:
        from vnpy_ctastrategy import CtaStrategyApp
        apps_to_try.append(("CtaStrategy", CtaStrategyApp, "vnpy_ctastrategy"))
        print("  ✓ 找到 CtaStrategyApp")
    except ImportError:
        print("  ✗ 未找到 vnpy_ctastrategy")
        print("     安装: pip install vnpy_ctastrategy")
    
    # CTA回测
    try:
        from vnpy_ctabacktester import CtaBacktesterApp
        apps_to_try.append(("CtaBacktester", CtaBacktesterApp, "vnpy_ctabacktester"))
        print("  ✓ 找到 CtaBacktesterApp")
    except ImportError:
        print("  - 未找到 vnpy_ctabacktester (回测功能可选)")
        print("     安装: pip install vnpy_ctabacktester")

    if not apps_to_try:
        print("\n⚠️  未找到任何功能应用，图形界面将为空。")
        print("请至少安装一个功能模块 (如 vnpy_datamanager)。")
        input("\n按回车键退出...")
        return

    # 第3步：创建Qt应用和引擎
    print("\n[3/4] 初始化系统引擎...")
    try:
        qapp = create_qapp("VeighNa Trader")
        event_engine = EventEngine()
        main_engine = MainEngine(event_engine)
        print("  ✓ 引擎初始化成功")
    except Exception as e:
        print(f"  ✗ 引擎初始化失败: {e}")
        input("\n按回车键退出...")
        return

    # 第4步：加载应用（关键部分）
    print("\n[4/4] 加载功能应用...")
    print("-" * 40)
    
    loaded_count = 0
    loaded_names = []
    
    for app_name, app_class, module_name in apps_to_try:
        try:
            # 方式A：直接传入应用类（新架构可能的方式）
            main_engine.add_app(app_class)
            loaded_count += 1
            loaded_names.append(app_name)
            print(f"  ✓ {app_name} (通过类加载)")
            
        except TypeError as e:
            if "takes no arguments" in str(e) or "unexpected keyword argument" in str(e):
                # 方式B：尝试使用APP_NAME常量
                try:
                    module = __import__(module_name)
                    if hasattr(module, 'APP_NAME'):
                        main_engine.add_app(module.APP_NAME)
                        loaded_count += 1
                        loaded_names.append(app_name)
                        print(f"  ✓ {app_name} (通过APP_NAME加载)")
                    else:
                        print(f"  ✗ {app_name}: 无法确定加载方式")
                        print(f"     错误: {e}")
                        print(f"     提示: {module_name} 模块可能需要特定初始化方式")
                except Exception as e2:
                    print(f"  ✗ {app_name}: 所有加载方式均失败")
                    print(f"     错误详情: {e2}")
            else:
                print(f"  ✗ {app_name}: 加载时出错")
                print(f"     错误: {e}")
                
        except Exception as e:
            print(f"  ✗ {app_name}: 加载失败")
            print(f"     错误: {e}")

    print(f"\n✅ 启动完成。成功加载 {loaded_count}/{len(apps_to_try)} 个应用")
    if loaded_names:
        print(f"   已加载: {', '.join(loaded_names)}")

    # 第5步：创建并显示主窗口
    try:
        print("\n" + "=" * 60)
        print("正在启动主窗口...")
        print("=" * 60)
        
        main_window = MainWindow(main_engine, event_engine)
        main_window.showMaximized()
        
        # 启动前最后提示
        if loaded_count == 0:
            print("\n⚠️  警告: 未成功加载任何功能应用，界面可能为空。")
            print("请检查上方错误信息，并确保已正确安装所需模块。")
            print("\n按 Ctrl+C 可关闭程序")
        
        print("\n" + "=" * 60)
        print("VeighNa Trader 已启动！")
        print("=" * 60)
        
        # 运行应用
        sys.exit(qapp.exec())
        
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断启动")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 启动主窗口失败: {e}")
        traceback.print_exc()
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()
