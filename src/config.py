import toml
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class YunhuConfig:
    """云湖相关配置"""

    api_url: str = field(
        default="https://chat-go.jwzhd.com/open-apis/v1/bot/messages"
    )  # 默认API URL
    api_key: str


@dataclass
class MaiBotConfig:
    """麦麦连接相关配置"""

    server: str = field(default="127.0.0.1")
    port: int = field(default=8000)


class BaseConfig:
    """主要配置"""

    yunhu_config: YunhuConfig
    mai_config: MaiBotConfig

    def __init__(self, config_path: str):
        self.config_data: Dict[str, Any] = load_config(config_path)
        self.yunhu_config = YunhuConfig(**self.config_data.get("YunhuConfig", {}))
        self.mai_config = MaiBotConfig(**self.config_data.get("MaiBotConfig", {}))


def load_config(file_path: str) -> "BaseConfig":
    """Load configuration from a TOML file."""
    try:
        return toml.load(file_path)
    except Exception as e:
        raise RuntimeError(f"加载配置文件失败: {e}")
