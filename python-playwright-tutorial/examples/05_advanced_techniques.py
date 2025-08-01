"""
Playwright 高级技巧示例
演示网络拦截、移动端模拟、Cookie管理、性能监控等高级功能
"""

import json
import time
from playwright.sync_api import sync_playwright
from datetime import datetime

def network_interception_example():
    """网络拦截和修改示例"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        # 存储网络请求和响应
        requests = []
        responses = []
        failed_requests = []
        
        # 监听网络事件
        def handle_request(request):
            requests.append({
                'url': request.url,
                'method': request.method,
                'headers': dict(request.headers),
                'timestamp': datetime.now().isoformat()
            })
            print(f"🔄 请求: {request.method} {request.url}")
        
        def handle_response(response):
            responses.append({
                'url': response.url,
                'status': response.status,
                'headers': dict(response.headers),
                'timestamp': datetime.now().isoformat()
            })
            print(f"✅ 响应: {response.status} {response.url}")
        
        def handle_request_failed(request):
            failed_requests.append({
                'url': request.url,
                'failure': request.failure,
                'timestamp': datetime.now().isoformat()
            })
            print(f"❌ 请求失败: {request.url}")
        
        # 绑定事件监听器
        page.on('request', handle_request)
        page.on('response', handle_response)
        page.on('requestfailed', handle_request_failed)
        
        # 拦截并修改API响应
        def mock_api_response(route):
            if 'json' in route.request.url:
                # 返回模拟数据
                mock_data = {
                    "mocked": True,
                    "timestamp": datetime.now().isoformat(),
                    "message": "这是被拦截和修改的响应"
                }
                route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps(mock_data, ensure_ascii=False)
                )
            else:
                route.continue_()
        
        # 设置路由拦截
        page.route('**/json', mock_api_response)
        
        try:
            print("开始网络拦截演示...")
            
            # 访问页面
            page.goto('https://httpbin.org')
            page.wait_for_load_state('networkidle')
            
            # 点击JSON API链接
            page.click('a[href="/json"]')
            page.wait_for_load_state('networkidle')
            
            # 检查是否显示了模拟数据
            content = page.content()
            if "这是被拦截和修改的响应" in content:
                print("✅ API响应拦截成功")
            
            # 保存网络日志
            network_log = {
                'requests': requests,
                'responses': responses,
                'failed_requests': failed_requests,
                'summary': {
                    'total_requests': len(requests),
                    'total_responses': len(responses),
                    'failed_requests': len(failed_requests)
                }
            }
            
            with open('network_log.json', 'w', encoding='utf-8') as f:
                json.dump(network_log, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 网络日志已保存: {len(requests)} 请求, {len(responses)} 响应")
            
        finally:
            browser.close()

def mobile_simulation_example():
    """移动端设备模拟示例"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 使用预设的移动设备配置
        device_configs = [
            p.devices['iPhone 12'],
            p.devices['iPhone 12 Pro'],
            p.devices['Pixel 5'],
            p.devices['Samsung Galaxy S21']
        ]
        
        for i, device in enumerate(device_configs):
            print(f"\n📱 测试设备 {i+1}: {device.get('user_agent', '').split(')')[-1]}")
            
            # 创建移动设备上下文
            context = browser.new_context(**device)
            page = context.new_page()
            
            try:
                # 访问响应式网站
                page.goto('https://whatismyviewport.com')
                page.wait_for_load_state('networkidle')
                
                # 获取视口信息
                viewport_info = page.evaluate('''() => {
                    return {
                        width: window.innerWidth,
                        height: window.innerHeight,
                        userAgent: navigator.userAgent,
                        devicePixelRatio: window.devicePixelRatio
                    }
                }''')
                
                print(f"  视口尺寸: {viewport_info['width']}x{viewport_info['height']}")
                print(f"  设备像素比: {viewport_info['devicePixelRatio']}")
                
                # 测试触摸事件
                if device.get('has_touch', False):
                    print("  📱 支持触摸操作")
                    # 模拟触摸滑动
                    page.touch_screen.tap(viewport_info['width']//2, viewport_info['height']//2)
                
                # 截图保存
                page.screenshot(path=f'mobile_screenshot_device_{i+1}.png')
                print(f"  📸 截图已保存: mobile_screenshot_device_{i+1}.png")
                
                time.sleep(1)
                
            finally:
                context.close()
        
        browser.close()

def cookie_and_storage_example():
    """Cookie和本地存储管理示例"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            print("开始Cookie和存储管理演示...")
            
            # 访问测试页面
            page.goto('https://httpbin.org/cookies/set/test-cookie/test-value')
            page.wait_for_load_state('networkidle')
            
            # 设置自定义Cookie
            context.add_cookies([
                {
                    'name': 'custom_session',
                    'value': 'abc123def456',
                    'domain': 'httpbin.org',
                    'path': '/'
                },
                {
                    'name': 'user_preference',
                    'value': 'dark_mode',
                    'domain': 'httpbin.org',
                    'path': '/'
                }
            ])
            
            print("✅ 已设置自定义Cookie")
            
            # 访问Cookie查看页面
            page.goto('https://httpbin.org/cookies')
            
            # 获取所有Cookie
            cookies = context.cookies()
            print(f"\n📝 当前Cookie数量: {len(cookies)}")
            
            for cookie in cookies:
                print(f"  {cookie['name']}: {cookie['value']}")
            
            # 设置本地存储
            page.evaluate('''() => {
                localStorage.setItem('app_version', '1.2.3');
                localStorage.setItem('last_visit', new Date().toISOString());
                sessionStorage.setItem('session_id', 'session_' + Math.random());
            }''')
            
            # 读取本地存储
            storage_data = page.evaluate('''() => {
                return {
                    localStorage: {...localStorage},
                    sessionStorage: {...sessionStorage}
                }
            }''')
            
            print(f"\n💾 本地存储数据:")
            print(f"  localStorage: {storage_data['localStorage']}")
            print(f"  sessionStorage: {storage_data['sessionStorage']}")
            
            # 保存浏览器状态
            state = context.storage_state()
            with open('browser_state.json', 'w') as f:
                json.dump(state, f, indent=2)
            print("✅ 浏览器状态已保存到 browser_state.json")
            
            # 演示状态恢复
            page.goto('https://httpbin.org/cookies')
            page.screenshot(path='cookies_before_clear.png')
            
            # 清除特定Cookie
            context.clear_cookies()
            page.reload()
            page.screenshot(path='cookies_after_clear.png')
            print("✅ Cookie已清除，截图已保存")
            
        finally:
            browser.close()

def performance_monitoring_example():
    """性能监控示例"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 性能指标收集
        performance_metrics = []
        load_times = []
        
        def collect_metrics():
            metrics = page.evaluate('''() => {
                const navigation = performance.getEntriesByType('navigation')[0];
                return {
                    domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                    loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
                    firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime || 0,
                    firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0,
                    networkRequests: performance.getEntriesByType('resource').length,
                    memoryInfo: performance.memory ? {
                        usedJSHeapSize: performance.memory.usedJSHeapSize,
                        totalJSHeapSize: performance.memory.totalJSHeapSize
                    } : null
                }
            }''')
            return metrics
        
        try:
            print("开始性能监控演示...")
            
            # 测试多个网站的性能
            test_urls = [
                'https://example.com',
                'https://httpbin.org',
                'https://jsonplaceholder.typicode.com'
            ]
            
            for url in test_urls:
                print(f"\n🔍 测试网站: {url}")
                
                start_time = time.time()
                page.goto(url, wait_until='networkidle')
                load_time = time.time() - start_time
                
                # 收集性能指标
                metrics = collect_metrics()
                metrics['url'] = url
                metrics['totalLoadTime'] = load_time
                
                performance_metrics.append(metrics)
                
                print(f"  📊 加载时间: {load_time:.2f}秒")
                print(f"  📊 DOM加载: {metrics['domContentLoaded']:.2f}ms")
                print(f"  📊 首次绘制: {metrics['firstPaint']:.2f}ms")
                print(f"  📊 网络请求: {metrics['networkRequests']}个")
                
                if metrics['memoryInfo']:
                    memory_mb = metrics['memoryInfo']['usedJSHeapSize'] / 1024 / 1024
                    print(f"  📊 内存使用: {memory_mb:.2f}MB")
            
            # 保存性能报告
            performance_report = {
                'timestamp': datetime.now().isoformat(),
                'metrics': performance_metrics,
                'summary': {
                    'average_load_time': sum(m['totalLoadTime'] for m in performance_metrics) / len(performance_metrics),
                    'fastest_site': min(performance_metrics, key=lambda x: x['totalLoadTime'])['url'],
                    'slowest_site': max(performance_metrics, key=lambda x: x['totalLoadTime'])['url']
                }
            }
            
            with open('performance_report.json', 'w') as f:
                json.dump(performance_report, f, indent=2)
            
            print(f"\n✅ 性能报告已保存到 performance_report.json")
            print(f"📈 平均加载时间: {performance_report['summary']['average_load_time']:.2f}秒")
            
        finally:
            browser.close()

def geolocation_and_permissions_example():
    """地理位置和权限管理示例"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        
        # 设置地理位置（模拟在北京）
        context = browser.new_context(
            geolocation={'latitude': 39.9042, 'longitude': 116.4074},
            permissions=['geolocation']
        )
        page = context.new_page()
        
        try:
            print("开始地理位置和权限演示...")
            
            # 创建测试页面
            html_content = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>地理位置测试</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    button { padding: 10px 20px; margin: 10px; font-size: 16px; }
                    #result { margin-top: 20px; padding: 10px; background: #f0f0f0; }
                </style>
            </head>
            <body>
                <h1>地理位置权限测试</h1>
                <button onclick="getLocation()">获取当前位置</button>
                <button onclick="watchLocation()">监控位置变化</button>
                <div id="result"></div>
                
                <script>
                    function getLocation() {
                        if (navigator.geolocation) {
                            navigator.geolocation.getCurrentPosition(showPosition, showError);
                        } else {
                            document.getElementById("result").innerHTML = "浏览器不支持地理位置";
                        }
                    }
                    
                    function watchLocation() {
                        if (navigator.geolocation) {
                            navigator.geolocation.watchPosition(showPosition, showError);
                        }
                    }
                    
                    function showPosition(position) {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        document.getElementById("result").innerHTML = 
                            `纬度: ${lat}<br>经度: ${lon}<br>精度: ${position.coords.accuracy}米`;
                    }
                    
                    function showError(error) {
                        document.getElementById("result").innerHTML = "错误: " + error.message;
                    }
                </script>
            </body>
            </html>
            '''
            
            # 保存并加载HTML文件
            with open('temp_geo.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            import os
            page.goto(f'file://{os.path.abspath("temp_geo.html")}')
            
            # 点击获取位置按钮
            page.click('button:has-text("获取当前位置")')
            
            # 等待位置信息显示
            page.wait_for_function('document.getElementById("result").innerHTML.includes("纬度")')
            
            # 获取位置信息
            location_info = page.locator('#result').inner_text()
            print(f"📍 获取到的位置信息:\n{location_info}")
            
            # 截图
            page.screenshot(path='geolocation_test.png')
            print("✅ 地理位置测试截图已保存")
            
            # 测试其他权限
            print("\n🔐 测试其他权限...")
            
            # 测试通知权限
            context.grant_permissions(['notifications'])
            notification_result = page.evaluate('''() => {
                return Notification.permission;
            }''')
            print(f"📢 通知权限状态: {notification_result}")
            
            # 测试摄像头权限（仅检查，不实际访问）
            context.grant_permissions(['camera'])
            camera_permission = page.evaluate('''async () => {
                try {
                    const result = await navigator.permissions.query({name: 'camera'});
                    return result.state;
                } catch (e) {
                    return 'error: ' + e.message;
                }
            }''')
            print(f"📷 摄像头权限状态: {camera_permission}")
            
        finally:
            browser.close()
            
            # 清理临时文件
            import os
            if os.path.exists('temp_geo.html'):
                os.remove('temp_geo.html')

def main():
    """运行所有高级技巧示例"""
    
    print("🚀 Playwright 高级技巧演示开始")
    
    # 网络拦截
    print("\n" + "="*60)
    print("1. 网络拦截和修改")
    network_interception_example()
    
    # 移动端模拟
    print("\n" + "="*60)
    print("2. 移动端设备模拟")
    mobile_simulation_example()
    
    # Cookie和存储管理
    print("\n" + "="*60)
    print("3. Cookie和本地存储管理")
    cookie_and_storage_example()
    
    # 性能监控
    print("\n" + "="*60)
    print("4. 性能监控")
    performance_monitoring_example()
    
    # 地理位置和权限
    print("\n" + "="*60)
    print("5. 地理位置和权限管理")
    geolocation_and_permissions_example()
    
    print("\n" + "="*60)
    print("✅ 所有高级技巧演示完成！")
    print("\n生成的文件:")
    print("- network_log.json: 网络请求日志")
    print("- mobile_screenshot_device_*.png: 移动设备截图")
    print("- browser_state.json: 浏览器状态")
    print("- performance_report.json: 性能报告")
    print("- geolocation_test.png: 地理位置测试截图")

if __name__ == "__main__":
    main()