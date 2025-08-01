# Playwright Python 自动化教程 - 快速设置指南

## 🚀 快速开始

### 1. 环境要求

- Python 3.7 或更高版本
- 操作系统: Windows, macOS, Linux
- 内存: 至少 4GB RAM
- 硬盘空间: 至少 2GB 可用空间

### 2. 安装步骤

#### 步骤 1: 创建项目目录
```bash
mkdir my-playwright-project
cd my-playwright-project
```

#### 步骤 2: 创建虚拟环境（推荐）
```bash
# Windows
python -m venv playwright-env
playwright-env\Scripts\activate

# macOS/Linux
python3 -m venv playwright-env
source playwright-env/bin/activate
```

#### 步骤 3: 安装依赖
```bash
# 基础安装
pip install playwright

# 或者使用 requirements.txt（包含更多可选依赖）
pip install -r requirements.txt

# 安装浏览器
playwright install
```

#### 步骤 4: 验证安装
```bash
# 运行代码生成器测试安装
playwright codegen example.com
```

### 3. 运行示例

#### 运行基础示例
```bash
python examples/01_basic_example.py
```

#### 运行表单处理示例
```bash
python examples/02_form_handling.py
```

#### 运行异步示例
```bash
python examples/03_async_example.py
```

#### 运行测试示例
```bash
# 安装 pytest（如果还没安装）
pip install pytest

# 运行测试
pytest examples/04_pytest_integration.py -v
```

### 4. 常见问题解决

#### 问题 1: 浏览器下载失败
```bash
# 手动下载浏览器
playwright install --force

# 或者只下载特定浏览器
playwright install chromium
```

#### 问题 2: 权限问题（Linux）
```bash
# 安装依赖
sudo apt-get update
sudo apt-get install -y libnss3 libnspr4 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libgtk-3-0 libgbm-dev
```

#### 问题 3: 无头模式问题
```python
# 如果图形界面有问题，使用无头模式
browser = p.chromium.launch(headless=True)
```

### 5. 目录结构

```
python-playwright-tutorial/
├── README.md                    # 主教程文档
├── setup_guide.md              # 本设置指南
├── requirements.txt             # 依赖包列表
├── examples/                    # 示例代码
│   ├── 01_basic_example.py     # 基础示例
│   ├── 02_form_handling.py     # 表单处理
│   ├── 03_async_example.py     # 异步编程
│   └── 04_pytest_integration.py # 测试框架集成
└── screenshots/                 # 截图输出目录（自动创建）
```

### 6. 下一步

1. 阅读主教程文档：[README.md](README.md)
2. 运行并修改示例代码
3. 尝试自己的自动化项目
4. 参考官方文档：https://playwright.dev/python/

### 7. 获得帮助

- 📖 官方文档: https://playwright.dev/python/
- 💬 GitHub Issues: https://github.com/microsoft/playwright-python/issues
- 🤝 社区讨论: https://github.com/microsoft/playwright/discussions

## 🎯 快速测试

创建一个简单的测试文件来验证一切正常：

```python
# test_quick.py
from playwright.sync_api import sync_playwright

def test_quick():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://example.com')
        
        title = page.title()
        print(f"页面标题: {title}")
        
        assert 'Example Domain' in title
        browser.close()
        print("✅ 测试通过！Playwright 安装成功！")

if __name__ == "__main__":
    test_quick()
```

运行测试：
```bash
python test_quick.py
```

如果看到 "✅ 测试通过！Playwright 安装成功！"，说明一切就绪！

## 📚 学习路径建议

1. **初学者**: 
   - 阅读教程基础部分
   - 运行 `01_basic_example.py`
   - 学习基本的页面操作

2. **进阶用户**:
   - 学习表单处理和等待策略
   - 运行 `02_form_handling.py`
   - 掌握定位器的使用

3. **高级用户**:
   - 学习异步编程和并发
   - 运行 `03_async_example.py`
   - 集成到测试框架中

4. **测试工程师**:
   - 学习 pytest 集成
   - 运行 `04_pytest_integration.py`
   - 构建完整的测试套件

开始您的 Playwright 自动化之旅吧！🚀