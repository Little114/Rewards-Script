from selenium import webdriver
from selenium.webdriver.edge.service import Service
import os
import time
import json
class SimpleBrowserDataSaver:
    def __init__(self, driver_path="msedgedriver.exe", save_folder="1"):
        self.driver_path = driver_path
        self.save_folder = save_folder
        self.driver = None
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
    def setup_driver(self):
        options = webdriver.EdgeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        user_data_dir = os.path.join(os.path.abspath(self.save_folder), "browser_data")
        options.add_argument(f"--user-data-dir={user_data_dir}")
        service = Service(self.driver_path)
        self.driver = webdriver.Edge(service=service, options=options)
        self.load_existing_cookies()
        return self.driver
    def load_existing_cookies(self):
        try:
            cookie_files = []
            if os.path.exists(self.save_folder):
                for file in os.listdir(self.save_folder):
                    if file.startswith("final_cookies_") and file.endswith(".json"):
                        cookie_files.append(file)
            if cookie_files:
                cookie_files.sort(reverse=True)
                latest_cookie_file = cookie_files[0]
                cookie_path = os.path.join(self.save_folder, latest_cookie_file)
                print(f"正在加载已有的Cookie数据: {latest_cookie_file}")
                with open(cookie_path, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                for cookie in cookies:
                    try:
                        if 'name' in cookie and 'value' in cookie:
                            self.driver.add_cookie(cookie)
                    except Exception as e:
                        print(f"添加Cookie {cookie.get('name', 'unknown')} 时出错: {e}")
                print(f"成功加载了 {len(cookies)} 个Cookie")
                self.driver.refresh()
            else:
                print("未找到已有的Cookie数据，将创建新的会话")
        except Exception as e:
            print(f"加载已有Cookie数据时发生错误: {e}")
            print("将继续创建新的浏览器会话")
    def save_browser_data(self, url):
        try:
            self.driver.get(url)
            time.sleep(3)  
            timestamp = str(int(time.time()))
            html_path = os.path.join(self.save_folder, f"page_{timestamp}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            info_path = os.path.join(self.save_folder, f"info_{timestamp}.txt")
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")
                f.write(f"标题: {self.driver.title}\n")
                f.write(f"当前URL: {self.driver.current_url}\n")
                f.write(f"时间戳: {timestamp}\n")
            cookies = self.driver.get_cookies()
            cookie_path = os.path.join(self.save_folder, f"cookies_{timestamp}.json")
            with open(cookie_path, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {self.save_folder} 文件夹:")
            print(f"- 源代码: page_{timestamp}.html")
            print(f"- 页面信息: info_{timestamp}.txt")
            print(f"- Cookie数据: cookies_{timestamp}.json")
            print(f"- 浏览器用户数据: {self.save_folder}/browser_data/ (包含Cookie、缓存等)")
            return True
        except Exception as e:
            print(f"保存数据时发生错误: {e}")
            return False
    def wait_for_user_close(self):
        print("\n浏览器已打开，数据已保存到1文件夹")
        print("请手动关闭浏览器窗口...")
        print("关闭浏览器后，程序将自动保存Cookie并退出")
        try:
            while True:
                try:
                    self.driver.current_url
                    time.sleep(1)  
                except:
                    print("浏览器已关闭，正在保存最终的Cookie数据...")
                    self.save_final_cookies()
                    break
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        except Exception as e:
            print(f"等待过程中发生错误: {e}")
    def save_final_cookies(self):
        try:
            timestamp = str(int(time.time()))
            cookies = self.driver.get_cookies()
            final_cookie_path = os.path.join(self.save_folder, f"final_cookies_{timestamp}.json")
            with open(final_cookie_path, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            print(f"最终的Cookie数据已保存: final_cookies_{timestamp}.json")
            print(f"共保存了 {len(cookies)} 个Cookie")
            if cookies:
                print("Cookie摘要:")
                for i, cookie in enumerate(cookies[:5]):  
                    print(f"  {i+1}. {cookie.get('name', 'N/A')} - {cookie.get('domain', 'N/A')}")
                if len(cookies) > 5:
                    print(f"  ... 还有 {len(cookies) - 5} 个Cookie")
            return True
        except Exception as e:
            print(f"保存最终Cookie数据时发生错误: {e}")
            return False
    def close(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
def main():
    data_saver = SimpleBrowserDataSaver(
        driver_path="msedgedriver.exe",
        save_folder="1"
    )
    try:
        driver = data_saver.setup_driver()
        data_saver.save_browser_data("https://www.bing.com")
        driver.get("https://rewards.bing.com")
        time.sleep(3)  
        timestamp = str(int(time.time()))
        html_path = os.path.join(data_saver.save_folder, f"rewards_page_{timestamp}.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"Rewards页面已保存: rewards_page_{timestamp}.html")
        data_saver.wait_for_user_close()
        print("\n程序已退出")
    except Exception as e:
        print(f"程序执行失败: {e}")
        return 1
    return 0
if __name__ == "__main__":
    main()