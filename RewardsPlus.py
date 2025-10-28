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
import subprocess
import signal
import socket
import psutil
class BingRewardsAutomation:
    def __init__(self, driver_path="msedgedriver.exe"):
        self.driver_path = driver_path
        self.driver = None
        self.failed_count = 0  
    def setup_driver(self):
        max_retries = 3
        retry_count = 0
        self.cleanup_driver_resources()
        while retry_count < max_retries:
            try:
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
                options.add_argument("--remote-debugging-timeout=300")  
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.0.0"
                ]
                options.add_argument(f"--user-agent={random.choice(user_agents)}")
                port = self.find_available_port_with_retry(max_retries=3)
                if port and port != 0:
                    print(f"使用端口 {port} 启动浏览器驱动")
                else:
                    print("使用系统分配的随机端口")
                service = Service(self.driver_path, port=port)
                try:
                    service.start()
                    self.driver = webdriver.Edge(service=service, options=options)
                    self.driver.set_page_load_timeout(60)  
                    self.driver.set_script_timeout(30)    
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
                    self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']})")
                    self.load_existing_cookies()
                    print("浏览器驱动设置成功")
                    return self.driver
                except Exception as driver_error:
                    try:
                        service.stop()
                    except:
                        pass
                    raise driver_error
            except Exception as e:
                retry_count += 1
                print(f"设置浏览器驱动失败 (尝试 {retry_count}/{max_retries}): {e}")
                self.cleanup_driver_resources()
                if retry_count < max_retries:
                    wait_time = retry_count * 5
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("浏览器驱动设置失败，已达到最大重试次数")
                    raise
    def find_available_port(self):
        port_range = range(9000, 10000)  
        used_ports_file = os.path.join("1", "used_ports_rewardsplus.json")
        recently_used_ports = set()
        try:
            if os.path.exists(used_ports_file):
                with open(used_ports_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    current_time = time.time()
                    recently_used_ports = {int(port) for port, timestamp in data.items() 
                                         if current_time - timestamp < 1800}  
        except Exception as e:
            print(f"读取端口使用记录失败: {e}")
        system_used_ports = set()
        try:
            for conn in psutil.net_connections():
                if hasattr(conn.laddr, 'port'):
                    system_used_ports.add(conn.laddr.port)
        except:
            pass
        shuffled_ports = list(port_range)
        random.shuffle(shuffled_ports)
        for port in shuffled_ports:
            if port not in system_used_ports and port not in recently_used_ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        result = s.connect_ex(('localhost', port))
                        if result != 0:  
                            print(f"找到可用端口: {port}")
                            self._record_port_usage(port)
                            return port
                except:
                    continue
        for port in shuffled_ports:
            if port not in system_used_ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        result = s.connect_ex(('localhost', port))
                        if result != 0:  
                            print(f"找到可用端口: {port}")
                            self._record_port_usage(port)
                            return port
                except:
                    continue
        print("警告：未找到可用端口，使用系统分配的随机端口")
        return 0
    def find_available_port_with_retry(self, max_retries=100):
        for attempt in range(max_retries):
            try:
                port = self.find_available_port()
                if port == 0:
                    print(f"端口查找失败，使用系统随机端口 (尝试 {attempt + 1}/{max_retries})")
                    return 0
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    result = s.connect_ex(('localhost', port))
                    if result != 0:  
                        print(f"端口 {port} 验证通过 (尝试 {attempt + 1}/{max_retries})")
                        return port
                    else:
                        print(f"端口 {port} 被占用，重试中... (尝试 {attempt + 1}/{max_retries})")
            except Exception as e:
                print(f"端口检查异常: {e} (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        print(f"端口查找失败，已达到最大重试次数 {max_retries}，使用系统随机端口")
        return 0
    def _record_port_usage(self, port):
        import json
        import os
        used_ports_file = os.path.join("1", "used_ports_rewardsplus.json")
        used_ports = {}
        try:
            if os.path.exists(used_ports_file):
                with open(used_ports_file, 'r', encoding='utf-8') as f:
                    used_ports = json.load(f)
        except Exception as e:
            print(f"读取端口使用记录失败: {e}")
        used_ports[str(port)] = time.time()
        current_time = time.time()
        expired_ports = []
        for port_str, timestamp in used_ports.items():
            if current_time - timestamp > 1800:  
                expired_ports.append(port_str)
        for port_str in expired_ports:
            del used_ports[port_str]
        if expired_ports:
            print(f"清理了 {len(expired_ports)} 个过期端口")
        if len(used_ports) > 200:
            sorted_ports = sorted(used_ports.items(), key=lambda x: x[1], reverse=True)
            removed_count = len(used_ports) - 200
            used_ports = dict(sorted_ports[:200])
            print(f"清理了 {removed_count} 个最旧的端口记录，保留最新的 200 个记录")
        try:
            with open(used_ports_file, 'w', encoding='utf-8') as f:
                json.dump(used_ports, f, indent=2)
        except Exception as e:
            print(f"保存端口使用记录失败: {e}")
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
                    self.failed_count = 0
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
                        self.failed_count += 1
                        if self.failed_count >= 20:
                            print("=== 点击一键领取失败，可能原因是没有额外任务 ===")
                            print("提示：连续20次未找到一键领取按钮，可能当前没有可领取的额外任务")
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
                    self.failed_count += 1
                    if self.failed_count >= 20:
                        print("=== 点击一键领取失败，可能原因是没有额外任务 ===")
                        print("提示：连续20次未找到一键领取按钮，可能当前没有可领取的额外任务")
                    return False
        return False
    def cleanup_driver_resources(self):
        try:
            import psutil
            print("检查浏览器驱动残留资源...")
            current_pid = os.getpid()
            found_count = 0
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        if proc.info['name'] and 'msedgedriver.exe' in proc.info['name'].lower():
                            if proc.info['cmdline']:
                                cmdline = ' '.join(proc.info['cmdline'])
                                if str(current_pid) in cmdline or '--port=' in cmdline:
                                    print(f"发现与本程序相关的Edge驱动进程 (PID: {proc.info['pid']}) - 仅记录不终止")
                                    found_count += 1
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            except Exception as e:
                print(f"检查Edge驱动进程时发生错误: {e}")
            self.release_occupied_ports_smart()
            print(f"资源检查完成，共发现 {found_count} 个相关进程")
        except Exception as e:
            print(f"检查驱动资源时发生错误: {e}")
    def release_occupied_ports_smart(self):
        try:
            import psutil
            common_ports = [8074, 9515, 4444, 5555, 63280]
            current_pid = os.getpid()
            found_count = 0
            for port in common_ports:
                try:
                    for conn in psutil.net_connections():
                        if conn.laddr.port == port and conn.status == 'LISTEN':
                            pid = conn.pid
                            if pid:
                                try:
                                    proc = psutil.Process(pid)
                                    if proc.is_running():
                                        cmdline = ' '.join(proc.cmdline()) if proc.cmdline() else ''
                                        if (str(current_pid) in cmdline or 
                                            'msedgedriver.exe' in cmdline.lower() or
                                            '--port=' in cmdline):
                                            print(f"发现端口 {port} 被本程序相关进程占用 (PID: {pid}) - 仅记录不释放")
                                            found_count += 1
                                        else:
                                            print(f"端口 {port} 被其他程序占用 (PID: {pid})，跳过检查")
                                except (psutil.NoSuchProcess, psutil.AccessDenied):
                                    continue
                except Exception as e:
                    print(f"检查端口 {port} 时发生错误: {e}")
            print(f"端口检查完成，共发现 {found_count} 个相关端口占用")
        except Exception as e:
            print(f"检查占用端口时发生错误: {e}")
    def release_occupied_ports(self):
        self.release_occupied_ports_smart()
    def safe_quit_driver(self):
        try:
            if self.driver:
                print("正在关闭浏览器...")
                self.driver.quit()
                print("浏览器已关闭")
                self.driver = None
                self.cleanup_driver_resources()
        except Exception as e:
            print(f"关闭浏览器时发生错误: {e}")
            self.cleanup_driver_resources()
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
            self.safe_quit_driver()
            print("Bing Rewards自动化流程结束")
        except Exception as e:
            print(f"自动化流程发生错误: {e}")
            self.safe_quit_driver()
            print("程序因错误退出")
            exit(1)
def main():
    try:
        print("=== Bing Rewards Plus 自动化脚本 ===")
        automation = BingRewardsAutomation()
        automation.run_rewards_automation()
        print("脚本执行完成")
    except KeyboardInterrupt:
        print("\n用户中断执行")
        exit(0)
    except Exception as e:
        print(f"主程序发生未捕获的错误: {e}")
        exit(1)
if __name__ == "__main__":
    main()