from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
import random
import argparse
import sys
import json
import os
import glob


KEYWORDS_PC = [

    "Best laptops 2025", "Smartphone deals", "Fashion trends women", "Online shopping discounts",
    "Gaming console prices", "Home appliance reviews", "Sneaker brands", "Luxury watches",
    "Budget headphones", "Furniture sales", "Electronics deals", "Black Friday 2025",
    "Amazon best sellers", "Tech gadgets 2025", "Winter clothing trends", "Jewelry gift ideas",
    

    "Top travel destinations", "Cheap flights 2025", "Hotel booking tips", "Beach vacation ideas",
    "City break Europe", "Adventure travel packages", "Cruise deals 2025", "Travel insurance comparison",
    "Camping gear reviews", "Best hiking trails", "Family vacation spots", "Solo travel tips",
    "Backpacking destinations", "Luxury resorts Asia", "Travel safety tips", "Road trip ideas",
    

    "Breaking news today", "World news updates", "US election 2025", "Global economy trends",
    "Climate change solutions", "Political debates 2025", "International conflicts", "Tech industry updates",
    "Stock market predictions", "Health policy news", "Space mission updates", "Energy crisis 2025",
    

    "Online courses free", "Best coding bootcamps", "Study abroad programs", "Scholarship opportunities",
    "Academic research tools", "Math learning apps", "History documentaries", "Science podcasts",
    "University rankings 2025", "Career training programs", "Language learning tips", "STEM resources",
    

    "Weight loss diets", "Home workout routines", "Mental health tips", "Meditation apps",
    "Healthy meal plans", "Fitness equipment reviews", "Yoga for beginners", "Nutrition supplements",
    "Running shoes reviews", "Stress management techniques", "Sleep improvement tips", "Vegan recipes easy",
    

    "New movie releases", "TV show reviews 2025", "Music festivals 2025", "Book recommendations",
    "Streaming service deals", "Celebrity news today", "Top video games 2025", "Art exhibitions",
    "Theater shows 2025", "Pop music charts", "Comedy specials Netflix", "Cultural events near me",
    

    "Smart home devices 2025", "Wearable tech reviews", "Electric car prices", "AI innovations",
    "5G network updates", "Virtual reality headsets", "Drone technology", "Cybersecurity tips",
    "Tech startups 2025", "Cloud storage comparison", "Programming tutorials", "Data privacy laws",
    

    "Local weather forecast", "Event planning ideas", "DIY craft projects", "Pet adoption near me",
    "Gardening for beginners", "Car maintenance tips", "Home renovation ideas", "Wedding planning guide",
    "Photography gear reviews", "Best coffee machines", "Restaurant reviews near me", "Online grocery delivery",
    "Real estate trends 2025", "Job search websites", "Personal finance apps", "Charity organizations"
]

KEYWORDS_MOBILE = [
    "Python programming", "AI technology", "Machine learning", "Data science", "Web development",
    "Cloud computing", "Cybersecurity", "Blockchain", "Quantum computing", "Big data",
    "Artificial intelligence", "Deep learning", "Software engineering", "DevOps", "Mobile apps",
    "Game development", "Network security", "Database management", "API integration", "Microservices",
    "Computer vision", "Natural language processing", "Robotics", "IoT devices", "5G technology",
    "Augmented reality", "Virtual reality", "Edge computing", "Serverless architecture", "Fintech",
    "Cryptocurrency", "Digital transformation", "Agile methodology", "Selenium automation", "Bing rewards",
    "Cloud security", "Web3", "Data analytics", "Neural networks", "Kubernetes", "Docker containers",
    "Cybersecurity trends", "Generative AI", "Low-code platforms", "Quantum cryptography",
    "Latest movies 2025", "Music streaming services", "Top Netflix shows", "Hollywood news",
    "Video game releases", "Pop culture trends", "Celebrity interviews", "Anime recommendations",
    "Streaming platforms comparison", "Oscar predictions 2025", "K-pop trends", "Virtual concerts",
    "Football highlights", "Basketball NBA news", "Olympics 2024 updates", "Tennis rankings",
    "Soccer World Cup", "Sports betting trends", "Fitness training tips", "Marathon training",
    "Healthy recipes", "Sustainable living", "Minimalist lifestyle", "Travel destinations 2025",
    "Home decor ideas", "Personal finance tips", "Mental health awareness", "Yoga benefits",
    "Vegan diet plans", "DIY home projects", "Eco-friendly products", "Budget travel tips",
    "Global news today", "Climate change updates", "Economic trends 2025", "International politics",
    "Tech industry news", "Stock market analysis", "World health organization updates",
    "Renewable energy trends", "Geopolitical events", "Space exploration news",
    "Online learning platforms", "Free coding tutorials", "Language learning apps",
    "STEM education trends", "Virtual classrooms", "Best universities 2025",
    "Weather forecast", "Local events near me", "Photography tips", "Pet care advice",
    "Gardening tips", "Electric vehicles 2025", "Smart home devices", "Fashion trends 2025",
    "Food delivery apps", "Virtual reality gaming", "Productivity tools", "Remote work tips",
    "Cryptocurrency prices", "Artificial intelligence ethics", "Space tourism", "Fitness trackers"
]

class BingSearchAutomation:
    def __init__(self, device_type="pc", headless=False, driver_path="msedgedriver.exe", user_data_dir=None, mode="search"):

        self.device_type = device_type
        self.headless = headless
        self.driver_path = driver_path
        self.user_data_dir = user_data_dir
        self.mode = mode
        self.driver = None
        

        self.keywords = self.load_keywords_from_file()
    
    def load_keywords_from_file(self):

        keywords = []
        try:
            with open("1.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if line and not line.startswith("#"):
                        keywords.append(line)
            
            if not keywords:
                print("警告：1.txt文件中没有找到关键词，将使用默认关键词库")
                
                return KEYWORDS_PC if self.device_type == "pc" else KEYWORDS_MOBILE
            
            print(f"从1.txt文件成功加载 {len(keywords)} 个关键词")
            return keywords
            
        except FileNotFoundError:
            print("警告：1.txt文件不存在，将使用默认关键词库")
            return KEYWORDS_PC if self.device_type == "pc" else KEYWORDS_MOBILE
        except Exception as e:
            print(f"读取1.txt文件时发生错误: {e}，将使用默认关键词库")
            return KEYWORDS_PC if self.device_type == "pc" else KEYWORDS_MOBILE
        
    def setup_driver(self):
        
        options = webdriver.EdgeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        
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
        
        
        if self.device_type == "mobile":
            mobile_user_agents = [
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 EdgA/121.0.0.0",
                "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 EdgA/120.0.0.0",
                "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36 EdgA/119.0.0.0"
            ]
            mobile_user_agent = random.choice(mobile_user_agents)
            options.add_argument(f"user-agent={mobile_user_agent}")
            options.add_experimental_option("mobileEmulation", {
                "deviceMetrics": {"width": 414, "height": 736, "pixelRatio": 3.0},
                "userAgent": mobile_user_agent
            })
        
        service = Service(self.driver_path)
        self.driver = webdriver.Edge(service=service, options=options)
        
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']})")
        
        
        self.load_existing_cookies()
        
        return self.driver
    
    def load_existing_cookies(self):
       
        try:
            
            cookie_files = glob.glob(os.path.join("1", "final_cookies_*.json"))
            
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
    
    def simulate_human_scroll(self, continuous=False):
        
        try:
            
            page_height = self.driver.execute_script(
                "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, "
                "document.body.offsetHeight, document.documentElement.offsetHeight, "
                "document.body.clientHeight, document.documentElement.clientHeight);"
            )
            
            current_position = self.driver.execute_script(
                "return window.pageYOffset || document.documentElement.scrollTop || 0;"
            )
            
            viewport_height = self.driver.execute_script(
                "return window.innerHeight || document.documentElement.clientHeight || 0;"
            )
            
            print(f"页面高度: {page_height}px, 当前位置: {current_position}px, 视口高度: {viewport_height}px")
            
            
            target_position = max(0, page_height - viewport_height)
            
            if current_position >= target_position:
                print("页面已经滚动到底部")
                if continuous:
                    
                    print("持续滑动模式：滚动回顶部重新开始")
                    
                    
                    scroll_steps = random.randint(3, 6)
                    for step in range(scroll_steps):
                        scroll_distance = -current_position / scroll_steps
                        self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                        time.sleep(0.05 + random.uniform(0.02, 0.08)) 
                    
                    
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(0.5 + random.uniform(0.2, 0.5))
                    
                    
                    current_position = 0
                else:
                    
                    wait_time = 4 + random.uniform(1, 3)
                    print(f"直接等待{wait_time:.1f}秒")
                    time.sleep(wait_time)
                    return
            
            if self.device_type == "mobile":
               
                print("手机模式：使用优化的平滑滑动")
                
                
                scroll_distance = target_position - current_position
                
                
                smooth_scroll_mobile = """
                const startY = window.pageYOffset || document.documentElement.scrollTop || 0;
                const targetY = arguments[0];
                const distance = targetY - startY;
                
                
                const baseDuration = 1200; 
                const distanceFactor = Math.min(distance / 800, 2.5); 
                const randomFactor = Math.random() * 0.3 + 0.85; 
                const duration = (baseDuration + (distanceFactor * 300)) * randomFactor;
                
                const startTime = performance.now();
                
                
                const easeFunctions = [
                    function easeOutCubic(t) { return (--t) * t * t + 1; },
                    function easeOutQuad(t) { return t * (2 - t); },
                    function easeOutExpo(t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); },
                    function easeInOutSine(t) { return -(Math.cos(Math.PI * t) - 1) / 2; }
                ];
                
                const selectedEase = easeFunctions[Math.floor(Math.random() * easeFunctions.length)];
                
                function scrollStep(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    
                    
                    const currentY = startY + distance * selectedEase(progress);
                    window.scrollTo(0, currentY);
                    
                    if (progress < 1) {
                        requestAnimationFrame(scrollStep);
                    }
                }
                
                requestAnimationFrame(scrollStep);
                """
                
                
                self.driver.execute_script(smooth_scroll_mobile, target_position)
                
                
                base_wait_time = 2.0
                wait_variation = random.uniform(0.3, 1.2)  
                wait_time = base_wait_time + wait_variation
                print(f"手机端平滑滑动完成，等待{wait_time:.1f}秒...")
                time.sleep(wait_time)
                
                
                max_attempts = 3
                for attempt in range(max_attempts):
                    
                    current_info = self.driver.execute_script("""
                        const scrollTop = (document.scrollingElement || document.documentElement).scrollTop || 0;
                        const scrollHeight = document.body.scrollHeight || document.documentElement.scrollHeight;
                        const clientHeight = document.documentElement.clientHeight || window.innerHeight;
                        const distanceToBottom = scrollHeight - scrollTop - clientHeight;
                        
                        return {
                            scrollTop: scrollTop,
                            scrollHeight: scrollHeight,
                            clientHeight: clientHeight,
                            distanceToBottom: distanceToBottom,
                            isAtBottom: distanceToBottom <= 50  
                        };
                    """)
                    
                    print(f"验证滑动结果 - 尝试 {attempt + 1}/{max_attempts}:")
                    print(f"  当前位置: {current_info['scrollTop']}px")
                    print(f"  页面高度: {current_info['scrollHeight']}px")
                    print(f"  视口高度: {current_info['clientHeight']}px")
                    print(f"  距离底部: {current_info['distanceToBottom']}px")
                    print(f"  是否到达底部: {'是' if current_info['isAtBottom'] else '否'}")
                    
                    
                    if current_info['isAtBottom']:
                        print("✓ 成功滑动到页面底部")
                        break
                    
                    
                    if attempt < max_attempts - 1:
                        print(f"未到达底部，使用备用方案 {attempt + 1}...")
                        
                        
                        if attempt == 0:
                            
                            try:
                                self.driver.execute_script("""
                                    window.scrollTo({
                                        top: document.body.scrollHeight || document.documentElement.scrollHeight,
                                        behavior: 'smooth'
                                    });
                                """)
                                time.sleep(1.5)
                                print("备用方案1执行成功")
                            except Exception as e1:
                                print(f"备用方案1失败: {e1}")
                        elif attempt == 1:
                            
                            try:
                                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);")
                                time.sleep(1.0)
                                print("备用方案2执行成功")
                            except Exception as e2:
                                print(f"备用方案2失败: {e2}")
                    else:
                        
                        print("最后一次尝试：使用最可靠的滚动方案")
                        try:
                            
                            remaining_distance = current_info['distanceToBottom']
                            steps = max(3, min(10, int(remaining_distance / 200)))
                            
                            for step in range(steps):
                                step_distance = remaining_distance / (steps - step)
                                self.driver.execute_script(f"window.scrollBy(0, {step_distance});")
                                time.sleep(0.3 + random.uniform(0.1, 0.3))
                            
                            
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);")
                            time.sleep(0.5)
                            print("备用方案3执行成功")
                        except Exception as e3:
                            print(f"备用方案3失败: {e3}")
                
                
                final_verification = self.driver.execute_script("""
                    const scrollTop = (document.scrollingElement || document.documentElement).scrollTop || 0;
                    const scrollHeight = document.body.scrollHeight || document.documentElement.scrollHeight;
                    const clientHeight = document.documentElement.clientHeight || window.innerHeight;
                    const distanceToBottom = scrollHeight - scrollTop - clientHeight;
                    
                    return distanceToBottom <= 50;
                """)
                
                if final_verification:
                    print("✓ 最终验证：成功到达页面底部")
                else:
                    print("⚠ 最终验证：可能未完全到达底部，但已尽力滑动")
                    
                    
                    final_info = self.driver.execute_script("""
                        return {
                            scrollTop: (document.scrollingElement || document.documentElement).scrollTop || 0,
                            scrollHeight: document.body.scrollHeight || document.documentElement.scrollHeight,
                            clientHeight: document.documentElement.clientHeight || window.innerHeight
                        };
                    """)
                    print(f"  最终位置: {final_info['scrollTop']}px")
                    print(f"  页面高度: {final_info['scrollHeight']}px")
                    print(f"  视口高度: {final_info['clientHeight']}px")
                
            else:
                
                smooth_scroll_pc = """
                const startY = window.pageYOffset || document.documentElement.scrollTop || 0;
                const targetY = arguments[0];
                const distance = targetY - startY;
                
                
                const baseDuration = 1800;
                const distanceFactor = Math.min(distance / 1000, 3); 
                const randomFactor = Math.random() * 0.4 + 0.8;
                const duration = (baseDuration + (distanceFactor * 400)) * randomFactor;
                
                const startTime = performance.now();
                
                
                const easeFunctions = [
                    function easeOutQuart(t) { return 1 - Math.pow(1 - t, 4); },
                    function easeInOutExpo(t) {
                        return t === 0 ? 0 : t === 1 ? 1 : t < 0.5 
                            ? Math.pow(2, 20 * t - 10) / 2
                            : (2 - Math.pow(2, -20 * t + 10)) / 2;
                    },
                    function easeInOutQuad(t) { return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; },
                    function easeOutCubic(t) { return (--t) * t * t + 1; }
                ];
                
                const selectedEase = easeFunctions[Math.floor(Math.random() * easeFunctions.length)];
                
                function scrollStep(currentTime) {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    
                    
                    const currentY = startY + distance * selectedEase(progress);
                    window.scrollTo(0, currentY);
                    
                    if (progress < 1) {
                        requestAnimationFrame(scrollStep);
                    }
                }
                
                requestAnimationFrame(scrollStep);
                """
                
                
                self.driver.execute_script(smooth_scroll_pc, target_position)
                
                
                base_wait_time = 2.5
                wait_variation = random.uniform(0.5, 2.0)  
                wait_time = base_wait_time + wait_variation
                print(f"PC端平滑滚动完成，等待{wait_time:.1f}秒...")
                time.sleep(wait_time)
            
            
            max_attempts_pc = 3
            for attempt in range(max_attempts_pc):
                
                current_info = self.driver.execute_script("""
                    const scrollTop = (document.scrollingElement || document.documentElement).scrollTop || 0;
                    const scrollHeight = document.body.scrollHeight || document.documentElement.scrollHeight;
                    const clientHeight = document.documentElement.clientHeight || window.innerHeight;
                    const distanceToBottom = scrollHeight - scrollTop - clientHeight;
                    
                    return {
                        scrollTop: scrollTop,
                        scrollHeight: scrollHeight,
                        clientHeight: clientHeight,
                        distanceToBottom: distanceToBottom,
                        isAtBottom: distanceToBottom <= 50  
                    };
                """)
                
                print(f"PC端验证滑动结果 - 尝试 {attempt + 1}/{max_attempts_pc}:")
                print(f"  当前位置: {current_info['scrollTop']}px")
                print(f"  页面高度: {current_info['scrollHeight']}px")
                print(f"  视口高度: {current_info['clientHeight']}px")
                print(f"  距离底部: {current_info['distanceToBottom']}px")
                print(f"  是否到达底部: {'是' if current_info['isAtBottom'] else '否'}")
                
                
                if current_info['isAtBottom']:
                    print("✓ PC端成功滑动到页面底部")
                    break
                
                
                if attempt < max_attempts_pc - 1:
                    print(f"PC端未到达底部，使用备用方案 {attempt + 1}...")
                    
                    
                    if attempt == 0:
                        
                        try:
                            self.driver.execute_script("""
                                window.scrollTo({
                                    top: document.body.scrollHeight || document.documentElement.scrollHeight,
                                    behavior: 'smooth'
                                });
                            """)
                            time.sleep(2.0)
                            print("PC端备用方案1执行成功")
                        except Exception as e1:
                            print(f"PC端备用方案1失败: {e1}")
                    elif attempt == 1:
                        
                        try:
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);")
                            time.sleep(1.5)
                            print("PC端备用方案2执行成功")
                        except Exception as e2:
                            print(f"PC端备用方案2失败: {e2}")
                else:
                    
                    print("PC端最后一次尝试：使用最可靠的滚动方案")
                    try:
                        
                        remaining_distance = current_info['distanceToBottom']
                        steps = max(3, min(10, int(remaining_distance / 200)))
                        
                        for step in range(steps):
                            step_distance = remaining_distance / (steps - step)
                            self.driver.execute_script(f"window.scrollBy(0, {step_distance});")
                            time.sleep(0.4 + random.uniform(0.1, 0.3))
                        
                        
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);")
                        time.sleep(0.5)
                        print("PC端备用方案3执行成功")
                    except Exception as e3:
                        print(f"PC端备用方案3失败: {e3}")
            
            
            final_verification_pc = self.driver.execute_script("""
                const scrollTop = (document.scrollingElement || document.documentElement).scrollTop || 0;
                const scrollHeight = document.body.scrollHeight || document.documentElement.scrollHeight;
                const clientHeight = document.documentElement.clientHeight || window.innerHeight;
                const distanceToBottom = scrollHeight - scrollTop - clientHeight;
                
                return distanceToBottom <= 50;
            """)
            
            if final_verification_pc:
                print("✓ PC端最终验证：成功到达页面底部")
            else:
                print("⚠ PC端最终验证：可能未完全到达底部，但已尽力滑动")
                
                
                final_info_pc = self.driver.execute_script("""
                    return {
                        scrollTop: (document.scrollingElement || document.documentElement).scrollTop || 0,
                        scrollHeight: document.body.scrollHeight || document.documentElement.scrollHeight,
                        clientHeight: document.documentElement.clientHeight || window.innerHeight
                    };
                """)
                print(f"  PC端最终位置: {final_info_pc['scrollTop']}px")
                print(f"  PC端页面高度: {final_info_pc['scrollHeight']}px")
                print(f"  PC端视口高度: {final_info_pc['clientHeight']}px")
            
            print(f"PC端滑动完成，等待5秒...")
            
            
            time.sleep(5)
            
            print("5秒等待结束，滑动完成")
            
            
            if continuous:
                print("持续滑动模式：准备下一次滑动")
                
                wait_time = random.uniform(3, 8)
                print(f"等待{wait_time:.1f}秒后继续滑动...")
                time.sleep(wait_time)
                
                
                self.simulate_human_scroll(continuous=False)
            
        except Exception as e:
            print(f"滑动时发生错误: {e}")
            
            
            error_type = type(e).__name__
            print(f"错误类型: {error_type}")
            
            
            backup_success = False
            
            
            if not backup_success:
                try:
                    print("尝试方案1：原生平滑滚动")
                    self.driver.execute_script("""
                        window.scrollTo({
                            top: document.body.scrollHeight || document.documentElement.scrollHeight,
                            behavior: 'smooth'
                        });
                    """)
                    time.sleep(3)
                    backup_success = True
                    print("方案1执行成功")
                except Exception as e1:
                    print(f"方案1失败: {e1}")
            
            
            if not backup_success:
                try:
                    print("尝试方案2：直接滚动到底部")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);")
                    time.sleep(2)
                    backup_success = True
                    print("方案2执行成功")
                except Exception as e2:
                    print(f"方案2失败: {e2}")
            
            
            if not backup_success:
                try:
                    print("尝试方案3：分步滚动")
                    steps = 20 if self.device_type == "pc" else 15
                    for i in range(steps):
                        try:
                            
                            scroll_distance = 100 + (i * 15)
                            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                            time.sleep(0.1)
                        except Exception as step_error:
                            print(f"分步滚动第{i+1}步失败: {step_error}")
                            continue
                    backup_success = True
                    print("方案3执行成功")
                except Exception as e3:
                    print(f"方案3失败: {e3}")
            
            
            if not backup_success and self.device_type == "pc":
                try:
                    print("尝试方案4：键盘滚动")
                    from selenium.webdriver.common.keys import Keys
                    body = self.driver.find_element(By.TAG_NAME, "body")
                    for i in range(15):
                        try:
                            body.send_keys(Keys.PAGE_DOWN)
                            time.sleep(0.12)
                        except Exception as key_error:
                            print(f"键盘滚动第{i+1}次失败: {key_error}")
                            continue
                    backup_success = True
                    print("方案4执行成功")
                except Exception as e4:
                    print(f"方案4失败: {e4}")
            
           
            if not backup_success:
                try:
                    print("尝试方案5：简单滚动")
                    for _ in range(10):
                        self.driver.execute_script("window.scrollBy(0, 300);")
                        time.sleep(0.2)
                    backup_success = True
                    print("方案5执行成功")
                except Exception as e5:
                    print(f"方案5失败: {e5}")
            
            
            if not backup_success:
                try:
                    print("所有备用方案都失败，尝试刷新页面")
                    self.driver.refresh()
                    time.sleep(3)
                    
                   
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    print("页面刷新后滚动成功")
                except Exception as final_error:
                    print(f"最终方案也失败: {final_error}")
                    print("使用简单等待方案")
            
           
            time.sleep(5)
            print("备用方案执行完成")
    
    def bing_search(self, query):
        
        try:
           
            self.driver.get("https://www.bing.com")
            
            
            wait_time = 2 + random.uniform(0.5, 2.0)
            time.sleep(wait_time)
            
            
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            
            search_box.click()
            time.sleep(random.uniform(0.2, 0.5))
            
            
            search_box.clear()
            time.sleep(random.uniform(0.1, 0.3))
            
           
            for i, char in enumerate(query):
                search_box.send_keys(char)
                
                
                delay = random.uniform(0.08, 0.25) 
                
                
                if random.random() < 0.05 and i > 2: 
                    search_box.send_keys(Keys.BACKSPACE)
                    time.sleep(random.uniform(0.1, 0.3))
                    search_box.send_keys(char)
                    delay += random.uniform(0.1, 0.3)
                
                time.sleep(delay)
            
            
            think_time = random.uniform(0.5, 2.5)
            time.sleep(think_time)
            
            
            if random.random() < 0.3:  
                try:
                    search_button = self.driver.find_element(By.ID, "search_icon")
                    search_button.click()
                except:
                    search_box.send_keys(Keys.RETURN)
            else:
                search_box.send_keys(Keys.RETURN)
            
           
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "b_results"))
            )
            
            print(f"搜索完成: {query}")
            
           
            self.simulate_human_scroll(continuous=False)
            
            return True
            
        except Exception as e:
            print(f"搜索失败: {query} - {e}")
           
            try:
                self.driver.refresh()
                time.sleep(8)
            except:
                pass
            return False
    
    def run_searches(self, search_count):
        
        successful_searches = 0
        
        try:
            print(f"开始执行{search_count}次{self.device_type.upper()}端搜索...")
            
            for i in range(search_count):
                keyword = random.choice(self.keywords)
                print(f"执行第 {i + 1} 次{self.device_type.upper()}端搜索: {keyword}")
                
                if self.bing_search(keyword):
                    successful_searches += 1
                
               
                if (i + 1) % 5 == 0:
                    time.sleep(random.uniform(30, 50))
            
            print(f"\n搜索完成！成功执行 {successful_searches}/{search_count} 次搜索")
            return successful_searches
            
        except Exception as e:
            print(f"执行搜索时发生错误: {e}")
            return successful_searches
    
    def close(self):
        
        if self.driver:
            self.driver.quit()

def main():
    
    parser = argparse.ArgumentParser(description='Bing搜索自动化脚本')
    parser.add_argument('--device', choices=['pc', 'mobile'], default='pc', 
                       help='设备类型: pc (电脑端) 或 mobile (移动端)')
    parser.add_argument('--count', type=int, default=40, 
                       help='搜索次数 (默认: 40次)')
    parser.add_argument('--headless', action='store_true', 
                       help='无界面模式运行')
    parser.add_argument('--driver', default='msedgedriver.exe', 
                       help='Edge驱动程序路径[默认有内置]')
    
    args = parser.parse_args()
    
   
    automation = BingSearchAutomation(
        device_type=args.device,
        headless=args.headless,
        driver_path=args.driver
    )
    
    try:
       
        automation.setup_driver()
        
       
        successful_searches = automation.run_searches(args.count)
        
        print(f"\n任务完成！设备类型: {args.device.upper()}")
        print(f"搜索次数: {args.count}")
        print(f"成功次数: {successful_searches}")
        
    except Exception as e:
        print(f"程序执行失败: {e}")
        return 1
    
    finally:
        automation.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
