"""
Anti-detect browser configuration with fingerprint spoofing
"""

import random
from typing import Dict, Any, Optional


class AntiDetectConfig:
    """Configuration for anti-detect browser with fingerprint spoofing"""
    
    # Common screen resolutions for Windows/Mac
    SCREEN_RESOLUTIONS = [
        {"width": 1920, "height": 1080},  # Full HD (most common)
        {"width": 2560, "height": 1440},  # 2K
        {"width": 1366, "height": 768},   # Common laptop
        {"width": 1536, "height": 864},   # Windows scaled
        {"width": 1440, "height": 900},   # MacBook Pro 13"
        {"width": 2880, "height": 1800},  # MacBook Pro 15" Retina
        {"width": 1280, "height": 720},   # HD
    ]
    
    # Windows user agents (Chrome on Windows 10/11)
    WINDOWS_USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    # Mac user agents (Chrome on macOS)
    MAC_USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ]
    
    # Platform-specific configurations
    WINDOWS_PLATFORMS = ["Win32", "Win64"]
    MAC_PLATFORMS = ["MacIntel"]
    
    # Languages (will be auto-detected based on proxy location)
    LANGUAGES_MAP = {
        "en": "en-US,en;q=0.9",
        "es": "es-ES,es;q=0.9,en;q=0.8",
        "fr": "fr-FR,fr;q=0.9,en;q=0.8",
        "de": "de-DE,de;q=0.9,en;q=0.8",
        "it": "it-IT,it;q=0.9,en;q=0.8",
        "pt": "pt-BR,pt;q=0.9,en;q=0.8",
        "ru": "ru-RU,ru;q=0.9,en;q=0.8",
        "ja": "ja-JP,ja;q=0.9,en;q=0.8",
        "zh": "zh-CN,zh;q=0.9,en;q=0.8",
        "default": "en-US,en;q=0.9",
    }
    
    # WebGL vendors and renderers for Windows/Mac
    WINDOWS_WEBGL_CONFIGS = [
        {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) UHD Graphics 630, OpenGL 4.1)"},
        {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060, OpenGL 4.5)"},
        {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060, OpenGL 4.6)"},
        {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon RX 580, OpenGL 4.5)"},
        {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics, OpenGL 4.5)"},
    ]
    
    MAC_WEBGL_CONFIGS = [
        {"vendor": "Intel Inc.", "renderer": "Intel Iris OpenGL Engine"},
        {"vendor": "Intel Inc.", "renderer": "Intel Iris Pro OpenGL Engine"},
        {"vendor": "Apple Inc.", "renderer": "Apple M1"},
        {"vendor": "Apple Inc.", "renderer": "Apple M2"},
        {"vendor": "AMD", "renderer": "AMD Radeon Pro 5500M OpenGL Engine"},
    ]
    
    @staticmethod
    def get_random_config(platform: str = None) -> Dict[str, Any]:
        """
        Generate a random anti-detect configuration
        
        Args:
            platform: "windows" or "mac" (random if None)
            
        Returns:
            Dictionary with configuration
        """
        # Choose platform if not specified
        if not platform:
            platform = random.choice(["windows", "mac"])
        
        # Select appropriate user agent and WebGL config
        if platform == "mac":
            user_agent = random.choice(AntiDetectConfig.MAC_USER_AGENTS)
            webgl = random.choice(AntiDetectConfig.MAC_WEBGL_CONFIGS)
            platform_name = random.choice(AntiDetectConfig.MAC_PLATFORMS)
            cores = random.choice([4, 8, 10])  # Mac common configs
            memory = random.choice([8, 16, 32])
        else:  # windows
            user_agent = random.choice(AntiDetectConfig.WINDOWS_USER_AGENTS)
            webgl = random.choice(AntiDetectConfig.WINDOWS_WEBGL_CONFIGS)
            platform_name = random.choice(AntiDetectConfig.WINDOWS_PLATFORMS)
            cores = random.choice([4, 6, 8, 12, 16])  # Windows common configs
            memory = random.choice([8, 16, 32])
        
        resolution = random.choice(AntiDetectConfig.SCREEN_RESOLUTIONS)
        
        # Pixel ratio: Mac more likely to be 2 (Retina), Windows mostly 1
        if platform == "mac":
            pixel_ratio = random.choice([2, 2, 2, 1])  # 75% chance of Retina
        else:
            pixel_ratio = random.choice([1, 1, 1, 2])  # 75% chance of standard
        
        return {
            "user_agent": user_agent,
            "platform": platform,
            "platform_name": platform_name,
            "viewport": resolution,
            "timezone": "America/New_York",  # Will be updated based on proxy location
            "locale": "en-US",  # Will be updated based on proxy location
            "language": "en-US,en;q=0.9",  # Will be updated based on proxy location
            "webgl": webgl,
            "screen": {
                "width": resolution["width"],
                "height": resolution["height"],
                "color_depth": 24,
                "pixel_ratio": pixel_ratio,
            },
            "hardware": {
                "cores": cores,
                "memory": memory,
            },
        }
    
    @staticmethod
    def update_config_for_country(config: Dict[str, Any], country_code: str) -> Dict[str, Any]:
        """
        Update configuration based on country code
        
        Args:
            config: Base configuration
            country_code: Two-letter country code (e.g., "US", "GB")
            
        Returns:
            Updated configuration
        """
        # Country to timezone mapping
        timezone_map = {
            "US": "America/New_York",
            "GB": "Europe/London",
            "FR": "Europe/Paris",
            "DE": "Europe/Berlin",
            "IT": "Europe/Rome",
            "ES": "Europe/Madrid",
            "BR": "America/Sao_Paulo",
            "RU": "Europe/Moscow",
            "JP": "Asia/Tokyo",
            "CN": "Asia/Shanghai",
            "AU": "Australia/Sydney",
            "CA": "America/Toronto",
            "MX": "America/Mexico_City",
            "IN": "Asia/Kolkata",
            "KR": "Asia/Seoul",
        }
        
        # Country to language mapping
        language_map = {
            "US": "en-US,en;q=0.9",
            "GB": "en-GB,en;q=0.9",
            "FR": "fr-FR,fr;q=0.9,en;q=0.8",
            "DE": "de-DE,de;q=0.9,en;q=0.8",
            "IT": "it-IT,it;q=0.9,en;q=0.8",
            "ES": "es-ES,es;q=0.9,en;q=0.8",
            "BR": "pt-BR,pt;q=0.9,en;q=0.8",
            "RU": "ru-RU,ru;q=0.9,en;q=0.8",
            "JP": "ja-JP,ja;q=0.9,en;q=0.8",
            "CN": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        
        # Country to locale mapping
        locale_map = {
            "US": "en-US",
            "GB": "en-GB",
            "FR": "fr-FR",
            "DE": "de-DE",
            "IT": "it-IT",
            "ES": "es-ES",
            "BR": "pt-BR",
            "RU": "ru-RU",
            "JP": "ja-JP",
            "CN": "zh-CN",
        }
        
        # Update config
        config["timezone"] = timezone_map.get(country_code, "America/New_York")
        config["language"] = language_map.get(country_code, "en-US,en;q=0.9")
        config["locale"] = locale_map.get(country_code, "en-US")
        
        return config
    
    @staticmethod
    def get_stealth_scripts(platform_name: str = "Win32") -> list:
        """
        Get JavaScript scripts for anti-detection
        
        Args:
            platform_name: Platform name (Win32, Win64, MacIntel)
        """
        return [
            # WebDriver removal
            """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """,
            
            # Platform spoofing
            f"""
            Object.defineProperty(navigator, 'platform', {{
                get: () => '{platform_name}'
            }});
            """,
            
            # Chrome automation detection
            """
            window.navigator.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {},
            };
            """,
            
            # Plugin spoofing
            """
            Object.defineProperty(navigator, 'plugins', {
                get: () => {
                    const plugins = [
                        {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                        {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                        {name: 'Native Client', filename: 'internal-nacl-plugin'}
                    ];
                    return plugins;
                }
            });
            """,
            
            # Languages spoofing
            """
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            """,
            
            # Permissions override
            """
            const originalGetContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type, ...args) {
                const context = originalGetContext.call(this, type, ...args);
                if (type === '2d') {
                    const originalFillText = context.fillText;
                    context.fillText = function(...args) {
                        args[0] = args[0] + String.fromCharCode(Math.floor(Math.random() * 26) + 97);
                        return originalFillText.apply(this, args);
                    };
                }
                return context;
            };
            """,
            
            # Permissions override
            """
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            """,
            
            # Battery API blocking
            """
            if ('getBattery' in navigator) {
                navigator.getBattery = undefined;
            }
            """,
            
            # Media devices blocking (for privacy)
            """
            const originalEnumerateDevices = navigator.mediaDevices.enumerateDevices;
            navigator.mediaDevices.enumerateDevices = async () => {
                return [];
            };
            """,
        ]


def get_context_options(config: Dict[str, Any], proxy_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate Playwright context options with anti-detect configuration
    
    Args:
        config: Anti-detect configuration dictionary
        proxy_url: Proxy URL if using proxy (HTTP/HTTPS only for Playwright)
        
    Returns:
        Dictionary of context options for Playwright
    """
    options = {
        "user_agent": config["user_agent"],
        "viewport": config["viewport"],
        "locale": config["locale"],
        "timezone_id": config["timezone"],
        "permissions": [],
        "color_scheme": "light",
        "device_scale_factor": config["screen"]["pixel_ratio"],
        "has_touch": False,
        "is_mobile": False,
        "extra_http_headers": {
            "Accept-Language": config["language"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
        },
    }
    
    # Add proxy if provided (HTTP/HTTPS only)
    if proxy_url:
        options["proxy"] = {"server": proxy_url}
    
    return options


def get_browser_args() -> list:
    """Get browser launch arguments for anti-detection"""
    return [
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--disable-gpu",
        "--no-first-run",
        "--no-zygote",
        "--disable-background-networking",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-breakpad",
        "--disable-component-extensions-with-background-pages",
        "--disable-features=TranslateUI,BlinkGenPropertyTrees",
        "--disable-ipc-flooding-protection",
        "--disable-renderer-backgrounding",
        "--enable-features=NetworkService,NetworkServiceInProcess",
        "--force-color-profile=srgb",
        "--hide-scrollbars",
        "--metrics-recording-only",
        "--mute-audio",
        "--no-default-browser-check",
        "--no-sandbox",
        "--disable-setuid-sandbox",
    ]

