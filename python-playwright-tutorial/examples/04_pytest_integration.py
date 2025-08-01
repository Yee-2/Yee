"""
Pytest 集成示例
演示如何在 pytest 测试框架中使用 Playwright
运行方式: pytest 04_pytest_integration.py -v
"""

import pytest
import json
from playwright.sync_api import sync_playwright, Page, Browser
from dataclasses import dataclass
from typing import List

# 测试数据类
@dataclass
class UserData:
    username: str
    email: str
    password: str
    expected_result: str

# 测试配置
class TestConfig:
    BASE_URL = "https://httpbin.org"
    TIMEOUT = 30000
    SLOW_MO = 500

# Fixtures - 测试前置设置
@pytest.fixture(scope="session")
def browser_context():
    """会话级别的浏览器上下文"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=TestConfig.SLOW_MO
        )
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Playwright Test Bot'
        )
        yield context
        context.close()
        browser.close()

@pytest.fixture
def page(browser_context):
    """每个测试函数的独立页面"""
    page = browser_context.new_page()
    page.set_default_timeout(TestConfig.TIMEOUT)
    yield page
    page.close()

@pytest.fixture
def test_data():
    """测试数据fixture"""
    return [
        UserData("testuser1", "test1@example.com", "password123", "success"),
        UserData("testuser2", "test2@example.com", "password456", "success"),
        UserData("", "invalid-email", "123", "error"),  # 无效数据
    ]

# 基础测试类
class TestBasicOperations:
    """基础操作测试"""
    
    def test_page_title(self, page: Page):
        """测试页面标题"""
        page.goto(f"{TestConfig.BASE_URL}/html")
        title = page.title()
        assert "httpbin" in title.lower()
    
    def test_page_navigation(self, page: Page):
        """测试页面导航"""
        # 访问首页
        page.goto(TestConfig.BASE_URL)
        assert page.url == f"{TestConfig.BASE_URL}/"
        
        # 点击链接导航
        page.click('a[href="/forms/post"]')
        page.wait_for_url('**/forms/post')
        assert "/forms/post" in page.url
        
        # 后退
        page.go_back()
        page.wait_for_url(TestConfig.BASE_URL)
    
    def test_element_visibility(self, page: Page):
        """测试元素可见性"""
        page.goto(f"{TestConfig.BASE_URL}/html")
        
        # 检查必要元素是否存在
        assert page.locator('h1').is_visible()
        assert page.locator('body').is_visible()
        
        # 检查不存在的元素
        assert not page.locator('#non-existent').is_visible()
    
    def test_text_content(self, page: Page):
        """测试文本内容"""
        page.goto(f"{TestConfig.BASE_URL}/html")
        
        # 获取页面标题文本
        h1_text = page.locator('h1').inner_text()
        assert len(h1_text) > 0
        
        # 检查页面是否包含特定文本
        assert page.get_by_text("httpbin").count() > 0

class TestFormOperations:
    """表单操作测试"""
    
    def test_form_submission(self, page: Page):
        """测试表单提交"""
        page.goto(f"{TestConfig.BASE_URL}/forms/post")
        
        # 填写表单
        page.fill('input[name="custname"]', 'Test User')
        page.fill('input[name="custtel"]', '13800138000')
        page.fill('input[name="custemail"]', 'test@example.com')
        page.fill('textarea[name="comments"]', 'This is a test comment')
        
        # 选择单选按钮
        page.click('input[value="medium"]')
        
        # 提交表单
        page.click('input[type="submit"]')
        
        # 验证提交结果
        page.wait_for_load_state('networkidle')
        content = page.content()
        assert 'Test User' in content
        assert 'test@example.com' in content
    
    def test_form_validation(self, page: Page):
        """测试表单验证"""
        page.goto(f"{TestConfig.BASE_URL}/forms/post")
        
        # 不填写必要字段直接提交
        page.click('input[type="submit"]')
        
        # 检查是否停留在表单页面（说明有验证）
        assert "/forms/post" in page.url
    
    @pytest.mark.parametrize("field_name,test_value", [
        ("custname", "张三"),
        ("custtel", "13912345678"),
        ("custemail", "zhangsan@test.com"),
        ("comments", "测试评论内容")
    ])
    def test_individual_form_fields(self, page: Page, field_name, test_value):
        """参数化测试各个表单字段"""
        page.goto(f"{TestConfig.BASE_URL}/forms/post")
        
        # 填写指定字段
        if field_name == "comments":
            page.fill(f'textarea[name="{field_name}"]', test_value)
        else:
            page.fill(f'input[name="{field_name}"]', test_value)
        
        # 验证值是否正确填入
        if field_name == "comments":
            actual_value = page.locator(f'textarea[name="{field_name}"]').input_value()
        else:
            actual_value = page.locator(f'input[name="{field_name}"]').input_value()
        
        assert actual_value == test_value

class TestApiInteraction:
    """API交互测试"""
    
    def test_json_response(self, page: Page):
        """测试JSON API响应"""
        page.goto(f"{TestConfig.BASE_URL}/json")
        
        # 获取页面内容
        content = page.content()
        
        # 验证JSON内容
        assert 'slideshow' in content
        assert 'application/json' in content or 'json' in content.lower()
    
    def test_status_codes(self, page: Page):
        """测试不同HTTP状态码"""
        # 测试200状态码
        response = page.goto(f"{TestConfig.BASE_URL}/status/200")
        assert response.status == 200
        
        # 测试404状态码
        response = page.goto(f"{TestConfig.BASE_URL}/status/404")
        assert response.status == 404
        
        # 测试500状态码
        response = page.goto(f"{TestConfig.BASE_URL}/status/500")
        assert response.status == 500
    
    def test_headers(self, page: Page):
        """测试HTTP头部"""
        page.goto(f"{TestConfig.BASE_URL}/headers")
        
        content = page.content()
        assert 'User-Agent' in content
        assert 'headers' in content.lower()

class TestScreenshotAndRecording:
    """截图和录制测试"""
    
    def test_screenshot_on_failure(self, page: Page):
        """测试失败时截图"""
        try:
            page.goto(f"{TestConfig.BASE_URL}/html")
            
            # 故意制造一个失败的断言
            assert page.locator('#non-existent-element').is_visible()
            
        except AssertionError:
            # 失败时截图
            page.screenshot(path='test_failure.png')
            raise
    
    def test_element_screenshot(self, page: Page):
        """测试元素截图"""
        page.goto(f"{TestConfig.BASE_URL}/html")
        
        # 截取特定元素
        if page.locator('h1').count() > 0:
            page.locator('h1').screenshot(path='h1_element.png')
        
        # 全页面截图
        page.screenshot(path='full_page.png', full_page=True)

class TestNetworkInterception:
    """网络拦截测试"""
    
    def test_request_interception(self, page: Page):
        """测试请求拦截"""
        requests = []
        
        # 监听所有请求
        page.on('request', lambda request: requests.append({
            'url': request.url,
            'method': request.method
        }))
        
        page.goto(f"{TestConfig.BASE_URL}/html")
        
        # 验证捕获到请求
        assert len(requests) > 0
        assert any(TestConfig.BASE_URL in req['url'] for req in requests)
    
    def test_response_modification(self, page: Page):
        """测试响应修改"""
        # 拦截JSON API并修改响应
        page.route(f"{TestConfig.BASE_URL}/json", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"modified": true, "test": "success"}'
        ))
        
        page.goto(f"{TestConfig.BASE_URL}/json")
        content = page.content()
        
        assert '"modified": true' in content
        assert '"test": "success"' in content

class TestDataDriven:
    """数据驱动测试"""
    
    @pytest.mark.parametrize("user_data", [
        UserData("user1", "user1@test.com", "pass123", "success"),
        UserData("user2", "user2@test.com", "pass456", "success"),
    ], ids=['user1', 'user2'])
    def test_parameterized_users(self, page: Page, user_data: UserData):
        """参数化用户测试"""
        page.goto(f"{TestConfig.BASE_URL}/forms/post")
        
        # 使用测试数据填写表单
        page.fill('input[name="custname"]', user_data.username)
        page.fill('input[name="custemail"]', user_data.email)
        page.fill('textarea[name="comments"]', f"Password: {user_data.password}")
        
        # 验证填写内容
        assert page.locator('input[name="custname"]').input_value() == user_data.username
        assert page.locator('input[name="custemail"]').input_value() == user_data.email

# 自定义标记的测试
@pytest.mark.slow
class TestSlowOperations:
    """慢速操作测试（标记为slow）"""
    
    def test_delayed_response(self, page: Page):
        """测试延迟响应"""
        page.goto(f"{TestConfig.BASE_URL}/delay/3")
        
        # 验证页面最终加载成功
        assert "delay" in page.url
        content = page.content()
        assert len(content) > 0

@pytest.mark.skip(reason="演示跳过测试")
def test_skipped_example(page: Page):
    """被跳过的测试示例"""
    pass

# 测试失败时的自动截图
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """pytest钩子：测试失败时自动截图"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # 获取page fixture
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            # 生成截图文件名
            test_name = item.name.replace("[", "_").replace("]", "_")
            screenshot_path = f"screenshots/failed_{test_name}.png"
            
            try:
                page.screenshot(path=screenshot_path)
                print(f"\n截图已保存: {screenshot_path}")
            except Exception as e:
                print(f"\n保存截图失败: {e}")

if __name__ == "__main__":
    # 创建截图目录
    import os
    os.makedirs("screenshots", exist_ok=True)
    
    # 运行测试
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-m", "not slow"  # 跳过标记为slow的测试
    ])