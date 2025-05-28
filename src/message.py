import asyncio
import time
import requests

from .config import BaseConfig


class ChatMessageFetcher:
    def __init__(self, config_path):
        self.config = BaseConfig(config_path)
        # 请求头配置
        self.headers = {
            "Authorization": f"Bearer {self.config.yunhu_config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "BotChatFetcher/1.0",
        }
        # 状态跟踪
        self.last_timestamp = int(time.time() * 1000)  # 初始化为当前时间戳（毫秒）
        self.running = True

    async def fetch_messages(self):
        """获取新消息"""
        try:
            params = {
                "since": self.last_timestamp,
                "limit": 100,  # 根据API限制调整
            }
            response = requests.get(
                self.api_url, headers=self.headers, params=params, timeout=10
            )
            response.raise_for_status()
            print(response.json)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {str(e)}")
            return None

    def process_messages(self, messages):
        """处理消息（示例逻辑）"""
        print(str(messages))
        if messages and len(messages) > 0:
            for msg in messages:
                print(f"收到新消息 [{msg['timestamp']}]: {msg['content']}")
                # 更新最后时间戳
                self.last_timestamp = max(self.last_timestamp, msg["timestamp"])
                # 在这里添加你的消息处理逻辑
                # 例如：调用机器人回复接口、进行数据分析等

    def run(self, interval=5):  # sourcery skip: use-named-expression
        """启动轮询"""
        print("消息监控已启动...")
        while self.running:
            try:
                messages = self.fetch_messages()
                if messages:
                    self.process_messages(messages)
                else:
                    print("没有新消息")
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n收到停止信号，正在退出...")
                self.running = False
            except Exception as e:
                print(f"运行异常: {str(e)}")
                time.sleep(interval * 2)  # 异常时延长等待
