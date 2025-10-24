import os
import json
import random
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
class FullBrowserAutomation:
    def __init__(self, data_folder="1"):
        self.data_folder = data_folder
        self.driver = None
        self.user_data_dir = os.path.join(os.getcwd(), "temp_user_data")
        self.hot_sites = [
            "https://www.baidu.com",
            "https://www.taobao.com", 
            "https://www.jd.com",
            "https://www.weibo.com",
            "https://www.zhihu.com",
            "https://www.bilibili.com",
            "https://www.douyin.com",
            "https://www.qq.com",
            "https://www.sina.com.cn",
            "https://www.sohu.com",
            "https://www.163.com",
            "https://www.360.com",
            "https://www.csdn.net",
            "https://www.oschina.net",
            "https://www.aliyun.com",
            "https://www.tencent.com",
            "https://www.xiaomi.com",
            "https://www.huawei.com",
            "https://www.meituan.com",
            "https://www.dianping.com",
            "https://www.douban.com",
            "https://www.ximalaya.com",
            "https://www.kuaishou.com",
            "https://www.toutiao.com",
            "https://www.ixigua.com"
        ]
    def setup_browser_with_full_data(self):
        try:
            if os.path.exists(self.user_data_dir):
                shutil.rmtree(self.user_data_dir)
            browser_data_source = os.path.join(self.data_folder, "browser_data")
            if os.path.exists(browser_data_source):
                print("复制浏览器数据文件...")
                shutil.copytree(browser_data_source, self.user_data_dir)
                print("浏览器数据复制完成")
            else:
                print("警告: 未找到完整的浏览器数据目录")
                os.makedirs(self.user_data_dir, exist_ok=True)
            edge_options = Options()
            edge_options.add_argument(f"--user-data-dir={self.user_data_dir}")
            edge_options.add_argument("--disable-blink-features=AutomationControlled")
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0"
            ]
            edge_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            edge_options.add_argument("--window-size=1200,800")
            driver_path = os.path.join(os.getcwd(), "msedgedriver.exe")
            service = Service(driver_path)
            self.driver = webdriver.Edge(service=service, options=edge_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("浏览器驱动设置完成（使用完整用户数据）")
            return True
        except Exception as e:
            print(f"设置浏览器驱动失败: {e}")
            return False
    def load_additional_cookies(self):
        try:
            cookie_files = []
            for file in os.listdir(self.data_folder):
                if file.startswith("cookies_") and file.endswith(".json"):
                    cookie_files.append(file)
            if not cookie_files:
                print("未找到额外的Cookie文件")
                return False
            all_cookies = []
            for cookie_file in cookie_files:
                cookie_path = os.path.join(self.data_folder, cookie_file)
                print(f"加载Cookie文件: {cookie_file}")
                with open(cookie_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                    all_cookies.extend(cookies)
            self.driver.get("https://www.bing.com")
            time.sleep(2)
            added_count = 0
            for cookie in all_cookies:
                try:
                    cookie_dict = {
                        'name': cookie.get('name', ''),
                        'value': cookie.get('value', ''),
                        'domain': cookie.get('domain', ''),
                        'path': cookie.get('path', '/'),
                        'secure': cookie.get('secure', False),
                        'httpOnly': cookie.get('httpOnly', False)
                    }
                    if 'expiry' in cookie:
                        cookie_dict['expiry'] = cookie['expiry']
                    self.driver.add_cookie(cookie_dict)
                    added_count += 1
                except Exception as e:
                    print(f"添加Cookie失败: {cookie.get('name', 'unknown')} - {e}")
            print(f"额外Cookie加载完成，成功添加 {added_count} 个Cookie")
            return True
        except Exception as e:
            print(f"加载额外Cookie失败: {e}")
            return False
    def simulate_real_user_behavior(self, site_url, wait_time=8):
        try:
            print(f"模拟真实用户行为，预计停留 {wait_time} 秒...")
            scroll_types = [
                ("快速浏览", 2, 0.3),
                ("仔细阅读", 4, 0.8),
                ("深度浏览", 6, 1.2)
            ]
            scroll_type = random.choice(scroll_types)
            scroll_count, scroll_delay = scroll_type[1], scroll_type[2]
            print(f"滚动模式: {scroll_type[0]}")
            for i in range(scroll_count):
                scroll_actions = [
                    ("向下滚动", f"window.scrollBy(0, {random.randint(200, 500)});"),
                    ("向上滚动", f"window.scrollBy(0, -{random.randint(100, 300)});"),
                    ("滚动到底部", "window.scrollTo(0, document.body.scrollHeight);"),
                    ("滚动到顶部", "window.scrollTo(0, 0);")
                ]
                action_name, script = random.choice(scroll_actions)
                self.driver.execute_script(script)
                print(f"  {action_name}")
                time.sleep(scroll_delay + random.uniform(0.1, 0.5))
            if random.random() > 0.3:  
                try:
                    links = self.driver.find_elements(By.TAG_NAME, "a")
                    visible_links = [link for link in links[:20] if link.is_displayed()]
                    if visible_links:
                        link_to_click = random.choice(visible_links)
                        link_text = link_to_click.text[:30] if link_to_click.text else "无文本链接"
                        print(f"点击链接: {link_text}...")
                        self.driver.execute_script("window.open(arguments[0].href);", link_to_click)
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        new_page_time = random.uniform(3, 8)
                        time.sleep(new_page_time)
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        print("新标签页浏览完成")
                except Exception as e:
                    print(f"点击链接时出错: {e}")
            if random.random() > 0.6:  
                try:
                    search_terms = ["Python", "人工智能", "机器学习", "编程", "技术", "新闻", "教程"]
                    search_box_selectors = [
                        "input[type='search']",
                        "input[name='q']", 
                        "input[name='wd']",
                        ".search-input",
                        "#search",
                        "#kw"
                    ]
                    for selector in search_boxes:
                        try:
                            search_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                            if search_box.is_displayed():
                                search_term = random.choice(search_terms)
                                search_box.clear()
                                search_box.send_keys(search_term)
                                if random.choice([True, False]):
                                    search_box.send_keys(Keys.RETURN)
                                    print(f"执行搜索: {search_term}")
                                    time.sleep(3)
                                    self.driver.back()
                                    time.sleep(1)
                                else:
                                    print(f"输入搜索词: {search_term}（未提交）")
                                    time.sleep(2)
                                    search_box.clear()
                                break
                        except:
                            continue
                except Exception as e:
                    print(f"搜索行为模拟失败: {e}")
            remaining_time = wait_time - (scroll_count * scroll_delay)
            if remaining_time > 0:
                print(f"等待剩余时间: {remaining_time:.1f}秒")
                time.sleep(remaining_time)
            print("用户行为模拟完成")
        except Exception as e:
            print(f"模拟用户行为时出错: {e}")
    def visit_hot_sites_with_full_data(self, max_sites=8):
        try:
            sites_to_visit = random.sample(self.hot_sites, min(max_sites, len(self.hot_sites)))
            print(f"计划访问 {len(sites_to_visit)} 个热门网站")
            print("=" * 50)
            for i, site in enumerate(sites_to_visit, 1):
                print(f"\n[{i}/{len(sites_to_visit)}] 正在访问: {site}")
                try:
                    self.driver.get(site)
                    WebDriverWait(self.driver, 15).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                    print(f"页面标题: {self.driver.title}")
                    visit_time = random.uniform(8, 15)
                    self.simulate_real_user_behavior(site, visit_time)
                    print(f"✓ 完成访问: {site}")
                except Exception as e:
                    print(f"✗ 访问 {site} 时出错: {e}")
                    continue
                if i < len(sites_to_visit):
                    wait_between = random.uniform(3, 6)
                    print(f"等待 {wait_between:.1f} 秒后访问下一个网站...")
                    time.sleep(wait_between)
            print("\n" + "=" * 50)
            print("所有热门网站访问完成！")
        except Exception as e:
            print(f"访问热门网站时出错: {e}")
    def run_full_automation(self, max_sites=8):
        try:
            print("=" * 50)
            print("完整浏览器自动化脚本")
            print("使用1文件夹中的所有浏览器数据和Cookie")
            print("=" * 50)
            if not self.setup_browser_with_full_data():
                print("浏览器设置失败")
                return False
            print("\n加载额外Cookie...")
            self.load_additional_cookies()
            print("\n开始访问热门网站...")
            self.visit_hot_sites_with_full_data(max_sites)
            print("\n浏览完成，浏览器将保持打开15秒...")
            time.sleep(15)
            return True
        except Exception as e:
            print(f"运行完整自动化时出错: {e}")
            return False
        finally:
            if self.driver:
                print("关闭浏览器...")
                self.driver.quit()
            if os.path.exists(self.user_data_dir):
                try:
                    shutil.rmtree(self.user_data_dir)
                    print("清理临时文件完成")
                except:
                    print("清理临时文件失败")
def main():
    automation = FullBrowserAutomation(data_folder="1")
    max_sites = 8
    success = automation.run_full_automation(max_sites=max_sites)
    if success:
        print("\n脚本执行成功！")
    else:
        print("\n脚本执行失败！")
if __name__ == "__main__":
    main()