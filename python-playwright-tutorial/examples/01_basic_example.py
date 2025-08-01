"""
基础 Playwright 示例
演示基本的页面操作和元素交互
"""

from playwright.sync_api import sync_playwright
import time

def basic_example():
    """基础示例：打开页面、查找元素、执行操作"""
    
    with sync_playwright() as p:
        # 启动浏览器（可见模式，便于观察）
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        # 创建新页面
        page = browser.new_page()
        
        try:
            # 导航到示例网站
            print("正在打开网页...")
            page.goto('https://example.com')
            
            # 获取页面标题
            title = page.title()
            print(f"页面标题: {title}")
            
            # 获取页面URL
            url = page.url
            print(f"当前URL: {url}")
            
            # 查找并获取页面文本
            heading = page.locator('h1').inner_text()
            print(f"主标题: {heading}")
            
            # 获取页面的一些基本信息
            content = page.locator('p').first.inner_text()
            print(f"页面内容摘要: {content[:100]}...")
            
            # 截图
            page.screenshot(path='example_screenshot.png')
            print("已保存截图: example_screenshot.png")
            
            # 等待一会儿以便观察
            time.sleep(2)
            
        except Exception as e:
            print(f"执行过程中出现错误: {e}")
            
        finally:
            # 关闭浏览器
            browser.close()
            print("浏览器已关闭")

def search_example():
    """搜索示例：在搜索引擎中执行搜索"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        try:
            # 访问 DuckDuckGo 搜索引擎
            print("正在访问 DuckDuckGo...")
            page.goto('https://duckduckgo.com')
            
            # 查找搜索框并输入搜索词
            search_box = page.locator('#search_form_input_homepage')
            search_term = "Playwright Python 教程"
            
            print(f"正在搜索: {search_term}")
            search_box.fill(search_term)
            
            # 点击搜索按钮
            page.click('#search_button_homepage')
            
            # 等待搜索结果加载
            page.wait_for_selector('[data-testid="result"]')
            
            # 获取搜索结果
            results = page.locator('[data-testid="result"]')
            result_count = results.count()
            
            print(f"找到 {result_count} 个搜索结果")
            
            # 打印前3个搜索结果的标题
            for i in range(min(3, result_count)):
                title_element = results.nth(i).locator('h2')
                if title_element.count() > 0:
                    title = title_element.inner_text()
                    print(f"结果 {i+1}: {title}")
            
            # 截图保存搜索结果
            page.screenshot(path='search_results.png')
            print("搜索结果截图已保存: search_results.png")
            
        except Exception as e:
            print(f"搜索过程中出现错误: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    print("=== Playwright 基础示例 ===")
    basic_example()
    
    print("\n=== Playwright 搜索示例 ===")
    search_example()
    
    print("\n所有示例执行完成！")