# Rewards Script帮你简单快速获取Rewards积分

## 📋 项目概述

本项目包含多个Python自动化脚本，专门用于Rewards积分获取。

## 🚨 重要提醒

**⚠️ 驱动程序兼容性警告**

虽然项目内置了 `msedgedriver.exe`，但**可能不兼容您的Edge浏览器版本**！

如果运行脚本时出现驱动程序错误，请：
1. 检查您的Edge浏览器版本
2. 访问 [Microsoft Edge Driver下载页面](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
3. 下载与您Edge版本匹配的驱动程序
4. 替换项目中的 `msedgedriver.exe` 文件

## 📁 脚本文件说明

### 1. Rewards.py - 主程序（刷积分）
**功能**：自动执行Bing搜索，获取每日积分

**特点**：
- 支持PC端和手机端搜索
- 模拟真实用户行为（滚动、点击、输入）
- 自动加载Cookie保持登录状态
- 隐藏自动化特征，降低检测风险

**使用方法**：
```bash
# PC端搜索（默认40次）
Rewards.py --device pc --count 40

# 移动端搜索
Rewards.py --device mobile --count 30

# 无界面模式运行
Rewards.py --device pc --count 40 --headless
```

**参数说明**：
- `--device`: 设备类型（pc/mobile）
- `--count`: 搜索次数
- `--headless`: 无界面模式
- `--driver`: 自定义驱动程序路径

### 2. edge.py - 浏览器启动器（登录账户）
**功能**：打开Edge浏览器但是不执行脚本，主要用于手动登录微软账户

**特点**：
- 使用完整的浏览器配置文件
- 保持Cookie持久化
- 为后续自动化脚本提供登录状态

**使用方法**：
```bash
双击打开
```

**使用场景**：
1. 首次使用时运行此脚本登录微软账户
2. 当Cookie过期时需要重新登录
3. 手动验证账户状态

### 3. 刷新搜索词.py - 搜索词管理
**功能**：管理和刷新搜索关键词库

**特点**：
- 自动更新搜索关键词
- 防止重复搜索被检测
- 提供多样化的搜索内容

**使用方法**：
```bash
双击打开
```

### 4. 浏览器Cookie仿正常用户.py - 高级浏览器自动化
**功能**：使用完整浏览器数据模拟真实用户行为

**特点**：
- 使用1文件夹中的所有浏览器数据
- 访问25个中国热门网站
- 高度模拟人类浏览行为
- 智能滚动、点击、搜索

**使用方法**：
```bash
双击打开
```

## 📂 数据文件说明

### 1/ 文件夹
包含完整的浏览器配置和Cookie数据：
- `browser_data/`: 浏览器配置文件
- `cookies_*.json`: Cookie数据文件
- `page_*.html`: 页面缓存
- `info_*.txt`: 浏览器信息

## 🛠️ 环境要求

### 系统要求
- Windows 10/11
- Python 3.8+
- Microsoft Edge浏览器

### Python依赖
```bash
pip install selenium
pip install argparse
```

## 🔧 安装和配置

### 步骤1：安装Python依赖
```bash
pip install selenium
pip install argparse
```

### 步骤2：验证驱动程序
1. 检查Edge浏览器版本
2. 如果内置驱动不兼容，下载匹配的msedgedriver
3. 替换项目中的msedgedriver.exe文件

### 步骤3：首次使用
1. 运行 `edge.py` 登录微软账户
2. 关闭浏览器
3. 运行 `Rewards.py` 开始刷积分

## ⚡ 使用流程

### 日常使用流程
1. **启动登录**（可选）：`edge.py`
2. **执行搜索**：`Rewards.py --device pc --count 40 [默认就是可以直接双击]`
3. **移动端搜索**：`Rewards.py --device mobile --count 30`

### 高级使用流程
1. **登录账户**：`edge.py`
2. **刷新关键词**：`刷新搜索词.py`
3. **执行主程序**：`Rewards.py`
4. **模拟浏览**：`浏览器Cookie仿正常用户.py`

## ⚠️ 注意事项

### 安全提醒
- 请不要过度转发本脚本
- 定期检查账户安全状态
- 避免过度使用导致账户异常

### 技术提醒
- 驱动程序兼容性是常见问题
- 网络稳定性影响脚本运行
- 浏览器更新可能导致脚本失效

### 使用建议
- 每日积分有上限
- 建议分时段执行搜索任务
- 建议24小时执行一次

## 🐛 故障排除

### 常见问题

**问题1**：驱动程序错误
```
Message: 'msedgedriver.exe' executable needs to be available in the path.
```
**解决方案**：下载匹配的Edge驱动程序

**问题2**：Cookie加载失败
```
加载Cookie时发生错误
```
**解决方案**：运行 `python edge.py` 重新登录

**问题3**：搜索被检测
```
搜索失败或账户异常
```
**解决方案**：受者[等一会或者用edge.py过]

### 调试模式
```bash
# 查看详细日志
python Rewards.py --device pc --count 5
```

## 📞 技术支持

如果遇到问题，请：
1. 检查日志
2. 验证驱动程序兼容性
3. 检查网络连接状态
4. 查看脚本输出的错误信息
5. 给作者钱帮你搞
6. 不会搞的还没钱只能受者

## 📄 许可证

本项目仅供学习和研究使用，请使用完脚本以后立马删除加清除记忆。
[懂我意思吧hhh]
---

**最后提醒**：请务必确保您的 `msedgedriver.exe` 与Edge浏览器版本匹配，这是脚本正常运行的关键！