"""
表单处理示例
演示如何处理各种类型的表单元素：输入框、下拉菜单、复选框、单选按钮等
"""

from playwright.sync_api import sync_playwright
import time

def form_handling_example():
    """表单处理示例"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()
        
        try:
            # 创建一个测试表单页面
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>表单测试页面</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .form-group { margin: 15px 0; }
                    label { display: block; margin-bottom: 5px; font-weight: bold; }
                    input, select, textarea { padding: 8px; margin: 5px 0; }
                    input[type="text"], input[type="email"], input[type="password"], 
                    select, textarea { width: 300px; }
                    button { padding: 10px 20px; background: #007cba; color: white; border: none; }
                    .result { margin-top: 20px; padding: 10px; background: #f0f0f0; }
                </style>
            </head>
            <body>
                <h1>用户注册表单</h1>
                <form id="registration-form">
                    <div class="form-group">
                        <label for="username">用户名:</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">邮箱:</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">密码:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="country">国家:</label>
                        <select id="country" name="country">
                            <option value="">请选择国家</option>
                            <option value="china">中国</option>
                            <option value="usa">美国</option>
                            <option value="uk">英国</option>
                            <option value="japan">日本</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>性别:</label>
                        <input type="radio" id="male" name="gender" value="male">
                        <label for="male" style="display: inline; margin-left: 5px;">男</label>
                        <input type="radio" id="female" name="gender" value="female">
                        <label for="female" style="display: inline; margin-left: 5px;">女</label>
                    </div>
                    
                    <div class="form-group">
                        <label>兴趣爱好:</label>
                        <input type="checkbox" id="reading" name="hobbies" value="reading">
                        <label for="reading" style="display: inline; margin-left: 5px;">阅读</label><br>
                        <input type="checkbox" id="sports" name="hobbies" value="sports">
                        <label for="sports" style="display: inline; margin-left: 5px;">运动</label><br>
                        <input type="checkbox" id="music" name="hobbies" value="music">
                        <label for="music" style="display: inline; margin-left: 5px;">音乐</label>
                    </div>
                    
                    <div class="form-group">
                        <label for="bio">个人简介:</label>
                        <textarea id="bio" name="bio" rows="4" placeholder="请输入个人简介..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <input type="checkbox" id="terms" name="terms" required>
                        <label for="terms" style="display: inline; margin-left: 5px;">我同意用户协议</label>
                    </div>
                    
                    <button type="submit" id="submit-btn">提交注册</button>
                </form>
                
                <div id="result" class="result" style="display: none;">
                    <h3>提交成功！</h3>
                    <p>表单数据已成功提交。</p>
                </div>
                
                <script>
                    document.getElementById('registration-form').addEventListener('submit', function(e) {
                        e.preventDefault();
                        document.getElementById('result').style.display = 'block';
                        this.style.display = 'none';
                    });
                </script>
            </body>
            </html>
            """
            
            # 创建临时HTML文件
            with open('temp_form.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 加载本地HTML文件
            page.goto(f'file://{abs_path}/temp_form.html')
            
            print("正在填写表单...")
            
            # 填写文本输入框
            page.fill('#username', 'testuser123')
            print("✓ 已填写用户名")
            
            page.fill('#email', 'testuser@example.com')
            print("✓ 已填写邮箱")
            
            page.fill('#password', 'securepassword123')
            print("✓ 已填写密码")
            
            # 选择下拉菜单
            page.select_option('#country', 'china')
            print("✓ 已选择国家")
            
            # 选择单选按钮
            page.click('#male')
            print("✓ 已选择性别")
            
            # 选择多个复选框
            page.check('#reading')
            page.check('#music')
            print("✓ 已选择兴趣爱好")
            
            # 填写文本域
            bio_text = "我是一名软件开发工程师，热爱编程和学习新技术。喜欢阅读技术书籍和听音乐。"
            page.fill('#bio', bio_text)
            print("✓ 已填写个人简介")
            
            # 勾选同意条款
            page.check('#terms')
            print("✓ 已同意用户协议")
            
            # 截图显示填写完成的表单
            page.screenshot(path='filled_form.png', full_page=True)
            print("✓ 已保存表单截图: filled_form.png")
            
            # 提交表单
            page.click('#submit-btn')
            print("✓ 已提交表单")
            
            # 等待提交结果显示
            page.wait_for_selector('#result', state='visible')
            
            # 验证提交结果
            result_text = page.locator('#result h3').inner_text()
            print(f"✓ 提交结果: {result_text}")
            
            # 截图显示提交结果
            page.screenshot(path='form_submitted.png')
            print("✓ 已保存提交结果截图: form_submitted.png")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"表单处理过程中出现错误: {e}")
            page.screenshot(path='form_error.png')
            
        finally:
            browser.close()
            
            # 清理临时文件
            import os
            if os.path.exists('temp_form.html'):
                os.remove('temp_form.html')

def login_form_example():
    """登录表单示例 - 使用真实网站"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        try:
            # 访问GitHub登录页面作为示例
            print("正在访问GitHub登录页面...")
            page.goto('https://github.com/login')
            
            # 等待页面加载
            page.wait_for_selector('#login_field')
            
            print("页面加载完成，开始演示表单操作...")
            
            # 找到用户名输入框并输入（但不真正登录）
            username_field = page.locator('#login_field')
            username_field.fill('demo_user')  # 使用演示用户名
            print("✓ 已填写用户名字段")
            
            # 找到密码输入框
            password_field = page.locator('#password')
            password_field.fill('demo_password')  # 使用演示密码
            print("✓ 已填写密码字段")
            
            # 截图显示填写的登录表单
            page.screenshot(path='github_login_form.png')
            print("✓ 已保存登录表单截图: github_login_form.png")
            
            # 清空表单（不实际提交）
            username_field.fill('')
            password_field.fill('')
            print("✓ 已清空表单内容（演示用途）")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"登录表单演示过程中出现错误: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    import os
    abs_path = os.path.abspath('.')
    
    print("=== 表单处理示例 ===")
    form_handling_example()
    
    print("\n=== 登录表单示例 ===")
    login_form_example()
    
    print("\n表单处理示例执行完成！")