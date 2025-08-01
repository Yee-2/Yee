"""
异步 Playwright 示例
演示异步编程和并发执行多个任务
"""

import asyncio
import time
from playwright.async_api import async_playwright

async def basic_async_example():
    """基础异步示例"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        try:
            print("异步访问网页...")
            await page.goto('https://httpbin.org/delay/2')  # 模拟慢速加载
            
            title = await page.title()
            print(f"页面标题: {title}")
            
            # 异步等待元素
            await page.wait_for_selector('body')
            content = await page.content()
            print(f"页面内容长度: {len(content)} 字符")
            
        finally:
            await browser.close()

async def test_single_url(url, browser_type='chromium'):
    """测试单个URL"""
    
    async with async_playwright() as p:
        browser_instance = getattr(p, browser_type)
        browser = await browser_instance.launch(headless=True)
        page = await browser.new_page()
        
        try:
            start_time = time.time()
            await page.goto(url, timeout=10000)
            
            title = await page.title()
            load_time = time.time() - start_time
            
            result = {
                'url': url,
                'title': title,
                'load_time': round(load_time, 2),
                'browser': browser_type,
                'status': 'success'
            }
            
        except Exception as e:
            result = {
                'url': url,
                'title': 'Error',
                'load_time': 0,
                'browser': browser_type,
                'status': f'error: {str(e)}'
            }
            
        finally:
            await browser.close()
            
        return result

async def concurrent_url_testing():
    """并发测试多个URL"""
    
    urls = [
        'https://httpbin.org',
        'https://jsonplaceholder.typicode.com',
        'https://reqres.in',
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
    ]
    
    print(f"开始并发测试 {len(urls)} 个URL...")
    start_time = time.time()
    
    # 创建并发任务
    tasks = [test_single_url(url) for url in urls]
    
    # 等待所有任务完成
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    total_time = time.time() - start_time
    
    print(f"\n并发测试完成，总耗时: {total_time:.2f} 秒")
    print("=" * 80)
    
    for result in results:
        if isinstance(result, dict):
            print(f"URL: {result['url']}")
            print(f"标题: {result['title']}")
            print(f"加载时间: {result['load_time']}秒")
            print(f"状态: {result['status']}")
            print("-" * 40)
        else:
            print(f"错误: {result}")

async def multi_browser_testing():
    """多浏览器并发测试"""
    
    url = 'https://example.com'
    browsers = ['chromium', 'firefox', 'webkit']
    
    print(f"在 {len(browsers)} 个浏览器中测试 {url}...")
    
    # 创建多浏览器测试任务
    tasks = [test_single_url(url, browser) for browser in browsers]
    
    results = await asyncio.gather(*tasks)
    
    print("\n多浏览器测试结果:")
    print("=" * 60)
    
    for result in results:
        print(f"浏览器: {result['browser']}")
        print(f"标题: {result['title']}")
        print(f"加载时间: {result['load_time']}秒")
        print(f"状态: {result['status']}")
        print("-" * 30)

async def form_automation_async():
    """异步表单自动化"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        try:
            # 访问表单测试网站
            await page.goto('https://httpbin.org/forms/post')
            
            print("开始异步填写表单...")
            
            # 并发填写多个字段
            await asyncio.gather(
                page.fill('input[name="custname"]', '张三'),
                page.fill('input[name="custtel"]', '13800138000'),
                page.fill('input[name="custemail"]', 'zhangsan@example.com'),
                page.fill('textarea[name="comments"]', '这是一个异步测试')
            )
            
            print("表单填写完成")
            
            # 选择尺寸
            await page.click('input[value="medium"]')
            
            # 截图
            await page.screenshot(path='async_form.png')
            print("已保存表单截图")
            
            # 提交表单
            await page.click('input[type="submit"]')
            
            # 等待结果页面
            await page.wait_for_load_state('networkidle')
            
            # 获取提交结果
            result_content = await page.content()
            if 'form' in result_content.lower():
                print("✓ 表单提交成功")
            
        except Exception as e:
            print(f"异步表单处理错误: {e}")
            
        finally:
            await browser.close()

async def page_interaction_async():
    """异步页面交互示例"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        page = await browser.new_page()
        
        try:
            await page.goto('https://httpbin.org')
            
            print("开始异步页面交互...")
            
            # 获取页面信息
            title, url, content_length = await asyncio.gather(
                page.title(),
                page.evaluate('location.href'),
                page.evaluate('document.body.innerText.length')
            )
            
            print(f"页面标题: {title}")
            print(f"页面URL: {url}")
            print(f"内容长度: {content_length} 字符")
            
            # 查找所有链接
            links = await page.locator('a').all()
            print(f"页面包含 {len(links)} 个链接")
            
            # 异步获取前5个链接的文本
            if len(links) >= 5:
                link_texts = await asyncio.gather(*[
                    link.inner_text() for link in links[:5]
                ])
                
                print("前5个链接的文本:")
                for i, text in enumerate(link_texts, 1):
                    print(f"  {i}. {text}")
            
            # 截图
            await page.screenshot(path='async_interaction.png')
            print("已保存交互截图")
            
        except Exception as e:
            print(f"异步页面交互错误: {e}")
            
        finally:
            await browser.close()

async def network_monitoring_async():
    """异步网络监控示例"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        requests = []
        responses = []
        
        # 监听请求和响应
        page.on('request', lambda request: requests.append({
            'url': request.url,
            'method': request.method,
            'headers': dict(request.headers)
        }))
        
        page.on('response', lambda response: responses.append({
            'url': response.url,
            'status': response.status,
            'headers': dict(response.headers)
        }))
        
        try:
            print("开始监控网络请求...")
            
            # 访问页面
            await page.goto('https://httpbin.org/json')
            
            # 等待页面完全加载
            await page.wait_for_load_state('networkidle')
            
            print(f"捕获到 {len(requests)} 个请求")
            print(f"捕获到 {len(responses)} 个响应")
            
            # 打印请求详情
            for i, req in enumerate(requests[:3], 1):
                print(f"请求 {i}: {req['method']} {req['url']}")
            
            # 打印响应详情
            for i, resp in enumerate(responses[:3], 1):
                print(f"响应 {i}: {resp['status']} {resp['url']}")
                
        except Exception as e:
            print(f"网络监控错误: {e}")
            
        finally:
            await browser.close()

async def main():
    """主函数 - 运行所有异步示例"""
    
    print("🚀 开始异步 Playwright 示例")
    
    # 基础异步示例
    print("\n1. 基础异步示例")
    await basic_async_example()
    
    # 并发URL测试
    print("\n2. 并发URL测试")
    await concurrent_url_testing()
    
    # 多浏览器测试
    print("\n3. 多浏览器测试")
    await multi_browser_testing()
    
    # 异步表单处理
    print("\n4. 异步表单处理")
    await form_automation_async()
    
    # 异步页面交互
    print("\n5. 异步页面交互")
    await page_interaction_async()
    
    # 网络监控
    print("\n6. 异步网络监控")
    await network_monitoring_async()
    
    print("\n✅ 所有异步示例执行完成！")

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())