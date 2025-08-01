# Python Playwright 自动化教程

## 📚 目录

1. [简介](#简介)
2. [环境安装](#环境安装)
3. [基础概念](#基础概念)
4. [第一个脚本](#第一个脚本)
5. [页面操作](#页面操作)
6. [元素定位](#元素定位)
7. [等待策略](#等待策略)
8. [表单处理](#表单处理)
9. [文件操作](#文件操作)
10. [截图和录制](#截图和录制)
11. [多浏览器支持](#多浏览器支持)
12. [并发执行](#并发执行)
13. [测试框架集成](#测试框架集成)
14. [高级技巧](#高级技巧)
15. [最佳实践](#最佳实践)
16. [常见问题](#常见问题)

## 🚀 简介

Playwright 是微软开发的现代端到端测试框架，支持多浏览器（Chromium、Firefox、WebKit）自动化。与 Selenium 相比，Playwright 具有以下优势：

- **更快的执行速度**：原生浏览器协议，无需 WebDriver
- **更可靠的元素等待**：智能等待机制
- **更强的并发能力**：支持并行测试
- **更丰富的功能**：网络拦截、移动端模拟等
- **更好的调试体验**：内置调试工具

## 🛠️ 环境安装

### 1. 安装 Python

确保您的系统已安装 Python 3.7 或更高版本：

```bash
python --version
# 或
python3 --version
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv playwright-env

# 激活虚拟环境
# Windows:
playwright-env\Scripts\activate
# macOS/Linux:
source playwright-env/bin/activate
```

### 3. 安装 Playwright

```bash
# 安装 playwright 包
pip install playwright

# 安装浏览器
playwright install

# 或者安装特定浏览器
playwright install chromium
playwright install firefox
playwright install webkit
```

### 4. 验证安装

```bash
# 运行示例测试
playwright codegen example.com
```

## 🎯 基础概念

### 核心组件

1. **Browser（浏览器）**：浏览器实例
2. **BrowserContext（浏览器上下文）**：独立的浏览器会话
3. **Page（页面）**：浏览器标签页
4. **Frame（框架）**：页面中的 iframe
5. **ElementHandle（元素句柄）**：DOM 元素的引用
6. **Locator（定位器）**：元素查找器

### 基本架构

```
Browser → BrowserContext → Page → Locator → Element
```

## 🎬 第一个脚本

让我们创建第一个 Playwright 脚本：

```python
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        
        # 创建新页面
        page = browser.new_page()
        
        # 导航到网站
        page.goto('https://example.com')
        
        # 获取页面标题
        title = page.title()
        print(f"页面标题: {title}")
        
        # 关闭浏览器
        browser.close()

if __name__ == "__main__":
    run()
```

### 异步版本

```python
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        await page.goto('https://example.com')
        title = await page.title()
        print(f"页面标题: {title}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
```

## 🖱️ 页面操作

### 1. 导航操作

```python
# 基本导航
page.goto('https://example.com')

# 带选项的导航
page.goto('https://example.com', wait_until='networkidle')

# 前进后退
page.go_back()
page.go_forward()

# 刷新页面
page.reload()
```

### 2. 点击操作

```python
# 基本点击
page.click('button')
page.click('#submit-btn')
page.click('text=提交')

# 右键点击
page.click('button', button='right')

# 双击
page.dblclick('button')

# 带修饰键的点击
page.click('a', modifiers=['Control'])
```

### 3. 文本输入

```python
# 输入文本
page.fill('#username', 'user123')
page.type('#password', 'secret', delay=100)

# 清空输入框
page.fill('#input', '')

# 按键操作
page.press('#input', 'Enter')
page.press('#input', 'Control+A')
```

### 4. 选择操作

```python
# 下拉选择
page.select_option('#country', 'china')
page.select_option('#country', label='中国')
page.select_option('#country', index=1)

# 复选框
page.check('#agree')
page.uncheck('#agree')

# 单选按钮
page.click('#radio-option')
```

## 🎯 元素定位

### 1. CSS 选择器

```python
# ID 选择器
page.click('#submit-button')

# 类选择器
page.click('.btn-primary')

# 属性选择器
page.click('[data-testid="login-btn"]')

# 复合选择器
page.click('form .submit-button')
```

### 2. 文本定位

```python
# 精确文本匹配
page.click('text=登录')

# 部分文本匹配
page.click('text=登')

# 正则表达式
page.click('text=/^登录.*/')
```

### 3. XPath 定位

```python
# XPath 表达式
page.click('xpath=//button[@type="submit"]')
page.click('//button[contains(text(), "提交")]')
```

### 4. Playwright 定位器

```python
# 使用 locator 方法
locator = page.locator('#username')
locator.fill('user123')

# 链式操作
page.locator('form').locator('input[type="text"]').fill('value')

# 过滤定位器
page.locator('button').filter(has_text='提交').click()
```

## ⏳ 等待策略

### 1. 等待元素

```python
# 等待元素可见
page.wait_for_selector('#element')

# 等待元素消失
page.wait_for_selector('#loading', state='hidden')

# 等待元素可点击
page.wait_for_selector('button', state='visible')
```

### 2. 等待页面事件

```python
# 等待页面加载
page.wait_for_load_state('networkidle')

# 等待导航完成
with page.expect_navigation():
    page.click('a[href="/next-page"]')

# 等待请求
with page.expect_request('**/api/data') as request_info:
    page.click('#load-data')
request = request_info.value
```

### 3. 自定义等待

```python
# 等待函数返回真值
page.wait_for_function('() => document.readyState === "complete"')

# 等待超时
page.wait_for_timeout(3000)  # 等待3秒
```

## 📝 表单处理

### 1. 登录表单

```python
def login(page, username, password):
    # 导航到登录页面
    page.goto('https://example.com/login')
    
    # 填写表单
    page.fill('#username', username)
    page.fill('#password', password)
    
    # 提交表单
    page.click('#login-btn')
    
    # 等待登录完成
    page.wait_for_url('**/dashboard')
```

### 2. 复杂表单

```python
def fill_registration_form(page, user_data):
    page.goto('https://example.com/register')
    
    # 基本信息
    page.fill('#firstName', user_data['first_name'])
    page.fill('#lastName', user_data['last_name'])
    page.fill('#email', user_data['email'])
    
    # 选择国家
    page.select_option('#country', user_data['country'])
    
    # 选择性别
    page.click(f'#gender-{user_data["gender"]}')
    
    # 勾选同意条款
    page.check('#terms')
    
    # 提交
    page.click('#register-btn')
```

## 📄 文件操作

### 1. 文件上传

```python
# 单文件上传
page.set_input_files('#file-upload', 'path/to/file.pdf')

# 多文件上传
page.set_input_files('#files', [
    'path/to/file1.pdf',
    'path/to/file2.jpg'
])

# 清空文件选择
page.set_input_files('#file-upload', [])
```

### 2. 文件下载

```python
# 等待下载
with page.expect_download() as download_info:
    page.click('#download-btn')
download = download_info.value

# 保存下载的文件
download.save_as('path/to/save/file.pdf')

# 获取下载信息
print(f"文件名: {download.suggested_filename}")
print(f"下载路径: {download.path()}")
```

## 📸 截图和录制

### 1. 截图

```python
# 全页面截图
page.screenshot(path='full-page.png')

# 元素截图
page.locator('#element').screenshot(path='element.png')

# 视口截图
page.screenshot(path='viewport.png', full_page=False)

# 自定义截图选项
page.screenshot(
    path='custom.png',
    quality=80,
    type='jpeg',
    full_page=True
)
```

### 2. 视频录制

```python
# 启动录制
context = browser.new_context(record_video_dir='videos/')
page = context.new_page()

# 执行操作
page.goto('https://example.com')
page.click('button')

# 关闭页面完成录制
page.close()
context.close()
```

### 3. 跟踪记录

```python
# 开始跟踪
context.tracing.start(screenshots=True, snapshots=True)

# 执行操作
page.goto('https://example.com')
page.click('button')

# 停止跟踪并保存
context.tracing.stop(path='trace.zip')
```

## 🌐 多浏览器支持

```python
def test_multi_browser():
    with sync_playwright() as p:
        browsers = [
            p.chromium.launch(),
            p.firefox.launch(),
            p.webkit.launch()
        ]
        
        for browser in browsers:
            page = browser.new_page()
            page.goto('https://example.com')
            
            # 执行测试
            title = page.title()
            print(f"{browser.browser_type.name}: {title}")
            
            browser.close()
```

## 🚀 并发执行

### 1. 异步并发

```python
import asyncio
from playwright.async_api import async_playwright

async def test_page(browser, url):
    page = await browser.new_page()
    await page.goto(url)
    title = await page.title()
    await page.close()
    return title

async def concurrent_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        urls = [
            'https://example.com',
            'https://httpbin.org',
            'https://jsonplaceholder.typicode.com'
        ]
        
        # 并发执行
        tasks = [test_page(browser, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for url, title in zip(urls, results):
            print(f"{url}: {title}")
        
        await browser.close()
```

### 2. 多进程并发

```python
from multiprocessing import Pool
from playwright.sync_api import sync_playwright

def test_url(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        title = page.title()
        browser.close()
        return title

def parallel_test():
    urls = [
        'https://example.com',
        'https://httpbin.org',
        'https://jsonplaceholder.typicode.com'
    ]
    
    with Pool(processes=3) as pool:
        results = pool.map(test_url, urls)
    
    for url, title in zip(urls, results):
        print(f"{url}: {title}")
```

## 🧪 测试框架集成

### 1. pytest 集成

```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_login(page):
    page.goto('https://example.com/login')
    page.fill('#username', 'test')
    page.fill('#password', 'test')
    page.click('#login')
    
    assert page.url == 'https://example.com/dashboard'

def test_search(page):
    page.goto('https://example.com')
    page.fill('#search', 'playwright')
    page.press('#search', 'Enter')
    
    assert page.locator('.search-results').count() > 0
```

### 2. unittest 集成

```python
import unittest
from playwright.sync_api import sync_playwright

class PlaywrightTestCase(unittest.TestCase):
    def setUp(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
    
    def tearDown(self):
        self.browser.close()
        self.playwright.stop()
    
    def test_example(self):
        self.page.goto('https://example.com')
        self.assertEqual(self.page.title(), 'Example Domain')

if __name__ == '__main__':
    unittest.main()
```

## 🎓 高级技巧

### 1. 网络拦截

```python
# 拦截请求
def handle_request(request):
    print(f"请求: {request.url}")
    request.continue_()

page.on('request', handle_request)

# 拦截响应
def handle_response(response):
    print(f"响应: {response.url} - {response.status}")

page.on('response', handle_response)

# 模拟网络故障
page.route('**/api/*', lambda route: route.abort())

# 修改请求
page.route('**/api/data', lambda route: route.fulfill(
    status=200,
    body='{"data": "mocked"}'
))
```

### 2. Cookie 管理

```python
# 设置 Cookie
context.add_cookies([{
    'name': 'session',
    'value': 'abc123',
    'domain': 'example.com',
    'path': '/'
}])

# 获取 Cookie
cookies = context.cookies()
for cookie in cookies:
    print(f"{cookie['name']}: {cookie['value']}")

# 保存状态
context.storage_state(path='state.json')

# 恢复状态
context = browser.new_context(storage_state='state.json')
```

### 3. 移动端模拟

```python
# 使用预设设备
iphone = p.devices['iPhone 12']
context = browser.new_context(**iphone)

# 自定义设备
context = browser.new_context(
    viewport={'width': 375, 'height': 667},
    user_agent='Custom Mobile UA',
    is_mobile=True,
    has_touch=True
)
```

### 4. 地理位置

```python
# 设置地理位置
context.set_geolocation(latitude=40.7128, longitude=-74.0060)
context.grant_permissions(['geolocation'])

page.goto('https://maps.google.com')
```

## 💡 最佳实践

### 1. 页面对象模式

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator('#username')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('#login-btn')
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    
    def is_login_error_displayed(self):
        return self.page.locator('.error').is_visible()

# 使用
page = browser.new_page()
login_page = LoginPage(page)
login_page.page.goto('https://example.com/login')
login_page.login('user', 'pass')
```

### 2. 配置管理

```python
# config.py
class Config:
    BASE_URL = 'https://example.com'
    TIMEOUT = 30000
    HEADLESS = True
    BROWSER = 'chromium'

# test_runner.py
def create_browser():
    with sync_playwright() as p:
        browser_type = getattr(p, Config.BROWSER)
        return browser_type.launch(headless=Config.HEADLESS)
```

### 3. 数据驱动测试

```python
import csv
import pytest

def load_test_data():
    with open('test_data.csv', 'r') as file:
        return list(csv.DictReader(file))

@pytest.mark.parametrize('test_data', load_test_data())
def test_login_with_data(page, test_data):
    page.goto('https://example.com/login')
    page.fill('#username', test_data['username'])
    page.fill('#password', test_data['password'])
    page.click('#login')
    
    if test_data['expected'] == 'success':
        assert page.url.endswith('/dashboard')
    else:
        assert page.locator('.error').is_visible()
```

### 4. 重试机制

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def flaky_operation(page):
    page.click('#unstable-button')
    page.wait_for_selector('#result', timeout=5000)
```

## ❓ 常见问题

### 1. 元素找不到

```python
# 问题：元素未找到
# 解决：等待元素出现
try:
    page.wait_for_selector('#element', timeout=10000)
    page.click('#element')
except TimeoutError:
    print("元素未找到")

# 使用 auto-waiting
page.locator('#element').click()  # 自动等待元素可点击
```

### 2. 页面加载慢

```python
# 设置更长的超时时间
page.goto('https://slow-site.com', timeout=60000)

# 等待特定状态
page.goto('https://slow-site.com', wait_until='networkidle')

# 分步等待
page.goto('https://slow-site.com')
page.wait_for_load_state('domcontentloaded')
page.wait_for_selector('#main-content')
```

### 3. 动态内容处理

```python
# 等待 AJAX 请求完成
with page.expect_response('**/api/data') as response_info:
    page.click('#load-data')
response = response_info.value

# 等待元素文本变化
page.wait_for_function(
    'element => element.textContent !== "Loading..."',
    page.locator('#status')
)
```

### 4. 内存泄漏

```python
# 正确的资源管理
def test_with_proper_cleanup():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            context = browser.new_context()
            page = context.new_page()
            
            # 执行测试
            page.goto('https://example.com')
            
        finally:
            # 确保资源清理
            browser.close()
```

## 🔧 调试技巧

### 1. 可视化调试

```python
# 启用慢速模式
browser = p.chromium.launch(slow_mo=1000)

# 开启调试模式
browser = p.chromium.launch(headless=False, devtools=True)

# 暂停执行
page.pause()  # 打开 Playwright Inspector
```

### 2. 日志记录

```python
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 自定义日志
def log_action(action, element):
    print(f"执行操作: {action} on {element}")

log_action("click", "#submit-button")
page.click("#submit-button")
```

### 3. 错误截图

```python
def test_with_error_screenshot(page):
    try:
        page.goto('https://example.com')
        page.click('#non-existent')
    except Exception as e:
        # 发生错误时截图
        page.screenshot(path=f'error-{int(time.time())}.png')
        raise e
```

## 📚 学习资源

- [Playwright 官方文档](https://playwright.dev/python/)
- [Playwright GitHub](https://github.com/microsoft/playwright-python)
- [示例代码集合](https://github.com/microsoft/playwright-python/tree/main/examples)

## 🎯 总结

Playwright 是一个功能强大的自动化测试工具，本教程涵盖了从基础到高级的各个方面。关键要点：

1. **选择合适的等待策略**：避免使用固定延时
2. **使用 Locator**：比直接操作元素更可靠
3. **实施页面对象模式**：提高代码维护性
4. **合理使用并发**：提高测试效率
5. **添加适当的错误处理**：增强脚本健壮性

通过实践这些示例和最佳实践，您将能够构建可靠、高效的自动化测试脚本。