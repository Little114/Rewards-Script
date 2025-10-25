from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
import random
import json
import os
import glob
class BingRewardsAutomation:
    def __init__(self, driver_path="msedgedriver.exe"):
        self.driver_path = driver_path
        self.driver = None
    def setup_driver(self):
        options = webdriver.EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        user_data_dir = os.path.join(os.getcwd(), "1", "browser_data")
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--window-size=1200,800")
        options.add_argument("--window-position=100,100")
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0"
        ]
        options.add_argument(f"--user-agent={random.choice(user_agents)}")
        service = Service(self.driver_path)
        self.driver = webdriver.Edge(service=service, options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']})")
        self.load_existing_cookies()
        return self.driver
    def load_existing_cookies(self):
        try:
            cookie_files = glob.glob(os.path.join("1", "cookies_*.json"))
            if not cookie_files:
                print("未找到Cookie文件，将创建新的会话")
                return
            latest_cookie_file = max(cookie_files, key=os.path.getmtime)
            print(f"加载Cookie文件: {latest_cookie_file}")
            with open(latest_cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            self.driver.get("https://www.bing.com")
            for cookie in cookies:
                try:
                    if 'name' in cookie and 'value' in cookie:
                        self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"添加Cookie失败: {cookie.get('name', 'unknown')} - {e}")
            self.driver.refresh()
            print(f"成功加载 {len(cookies)} 个Cookie，登录状态已恢复")
        except Exception as e:
            print(f"加载Cookie时发生错误: {e}")
    def wait_for_element(self, by, value, timeout=30):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            print(f"等待元素超时: {value} - {e}")
            return None
    def click_rewards_button(self):
        max_retries = 3  
        retry_count = 0
        while retry_count < max_retries:
            try:
                button = self.wait_for_element(By.ID, "bing_rewards_button")
                if button:
                    print("找到一键领取按钮，准备点击...")
                    time.sleep(random.uniform(1.0, 2.0))
                    button.click()
                    print("成功点击一键领取按钮")
                    print("等待10秒...")
                    time.sleep(10)
                    return True
                else:
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"未找到一键领取按钮，第{retry_count}次刷新页面重试...")
                        self.driver.refresh()
                        time.sleep(3)
                        WebDriverWait(self.driver, 30).until(
                            lambda driver: driver.execute_script("return document.readyState") == "complete"
                        )
                        print("页面刷新完成，重新查找按钮...")
                    else:
                        print(f"经过{max_retries}次重试仍未找到一键领取按钮")
                        return False
            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"点击按钮时发生错误: {e}，第{retry_count}次刷新页面重试...")
                    self.driver.refresh()
                    time.sleep(3)
                    WebDriverWait(self.driver, 30).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                    print("页面刷新完成，重新查找按钮...")
                else:
                    print(f"经过{max_retries}次重试后仍失败: {e}")
                    return False
        return False
    def run_rewards_automation(self):
        try:
            print("开始Bing Rewards自动化流程...")
            self.setup_driver()
            print("正在打开 https://rewards.bing.com/ ...")
            self.driver.get("https://rewards.bing.com/")
            print("等待页面加载完毕...")
            time.sleep(5)
            page_title = self.driver.title
            print(f"页面标题: {page_title}")
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("页面加载完毕，开始查找一键领取按钮...")
            if self.click_rewards_button():
                print("Bing Rewards领取流程完成")
            else:
                print("Bing Rewards领取流程失败")
            print("关闭浏览器...")
            self.driver.quit()
            print("Bing Rewards自动化流程结束")
        except Exception as e:
            print(f"自动化流程发生错误: {e}")
            if self.driver:
                self.driver.quit()
def main():
    print("=== Bing Rewards Plus 自动化脚本 ===")
    automation = BingRewardsAutomation()
    automation.run_rewards_automation()
if __name__ == "__main__":
    main()