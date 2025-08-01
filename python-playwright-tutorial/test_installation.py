#!/usr/bin/env python3
"""
Playwright 安装验证脚本
快速检查 Playwright 是否正确安装和配置
"""

import sys
import traceback
from datetime import datetime

def test_import():
    """测试 Playwright 导入"""
    try:
        from playwright.sync_api import sync_playwright
        print("✅ Playwright 导入成功")
        return True
    except ImportError as e:
        print(f"❌ Playwright 导入失败: {e}")
        print("💡 请运行: pip install playwright")
        return False

def test_browser_launch():
    """测试浏览器启动"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            print("✅ 浏览器启动成功")
            browser.close()
            return True
    except Exception as e:
        print(f"❌ 浏览器启动失败: {e}")
        print("💡 请运行: playwright install")
        return False

def test_basic_navigation():
    """测试基本页面导航"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 导航到简单页面
            page.goto('data:text/html,<html><body><h1>Test Page</h1></body></html>')
            
            # 获取标题
            title = page.title()
            
            # 查找元素
            heading = page.locator('h1').inner_text()
            
            browser.close()
            
            if heading == "Test Page":
                print("✅ 基本页面操作成功")
                return True
            else:
                print("❌ 页面操作验证失败")
                return False
                
    except Exception as e:
        print(f"❌ 基本导航测试失败: {e}")
        return False

def test_network_access():
    """测试网络访问"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 访问外部网站
            response = page.goto('https://example.com', timeout=10000)
            
            if response.status == 200:
                title = page.title()
                browser.close()
                print("✅ 网络访问正常")
                return True
            else:
                browser.close()
                print(f"❌ 网络访问异常，状态码: {response.status}")
                return False
                
    except Exception as e:
        print(f"❌ 网络访问测试失败: {e}")
        print("💡 请检查网络连接")
        return False

def test_async_support():
    """测试异步支持"""
    try:
        import asyncio
        from playwright.async_api import async_playwright
        
        async def async_test():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto('data:text/html,<html><body><h1>Async Test</h1></body></html>')
                title = await page.title()
                await browser.close()
                return True
        
        # 运行异步测试
        result = asyncio.run(async_test())
        
        if result:
            print("✅ 异步功能正常")
            return True
        else:
            print("❌ 异步功能测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 异步支持测试失败: {e}")
        return False

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python 版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python 版本过低: {version.major}.{version.minor}.{version.micro}")
        print("💡 需要 Python 3.7 或更高版本")
        return False

def main():
    """运行所有测试"""
    print("🚀 Playwright 安装验证开始")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("Python 版本检查", check_python_version),
        ("Playwright 导入", test_import),
        ("浏览器启动", test_browser_launch),
        ("基本页面操作", test_basic_navigation),
        ("网络访问", test_network_access),
        ("异步功能", test_async_support),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 测试: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            if "--verbose" in sys.argv:
                traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Playwright 安装正确！")
        print("\n下一步:")
        print("- 阅读 setup_guide.md 了解更多")
        print("- 运行 python examples/01_basic_example.py")
        print("- 开始您的 Playwright 学习之旅！")
        return True
    else:
        print("❌ 部分测试失败，请检查安装")
        print("\n常见解决方案:")
        print("1. pip install playwright")
        print("2. playwright install")
        print("3. 检查网络连接")
        print("4. 查看详细错误信息: python test_installation.py --verbose")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程中发生未预期的错误: {e}")
        if "--verbose" in sys.argv:
            traceback.print_exc()
        sys.exit(1)