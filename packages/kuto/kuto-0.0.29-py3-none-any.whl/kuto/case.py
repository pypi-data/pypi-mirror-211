import json
import time
from typing import Union
from urllib import parse

from kuto.core.android.driver import AndroidDriver
from kuto.core.android.element import AdrElem
from kuto.core.api.request import HttpReq
from kuto.core.ios.driver import IosDriver
from kuto.core.ios.element import IosElem
from kuto.utils.config import config
from kuto.utils.log import logger
from kuto.utils.exceptions import (
    HostIsNull
)
from kuto.core.web.driver import PlayWrightDriver
from kuto.core.web.element import WebElem


class Elem:
    _driver = None

    def __new__(cls, *args, **kwargs):
        platform = config.get_common("platform")
        if platform == "web":
            return WebElem(cls._driver, *args, **kwargs)
        elif platform == "android":
            return AdrElem(cls._driver, *args, **kwargs)
        elif platform == "ios":
            return IosElem(cls._driver, *args, **kwargs)
        else:
            raise KeyError("platform仅支持web、android、ios")

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self._driver = instance.driver
        return self


class Page(object):
    """页面基类，用于pom模式封装"""

    def __init__(self, driver: Union[AndroidDriver, IosDriver]):
        self.driver = driver

    @staticmethod
    def sleep(n):
        """休眠"""
        logger.info(f"休眠 {n} 秒")
        time.sleep(n)


class Case(HttpReq):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    driver: Union[AndroidDriver, IosDriver, PlayWrightDriver] = None

    # ---------------------初始化-------------------------------
    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        cls().end_class()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        self.start_time = time.time()
        platform = config.get_common("platform")
        if platform == "android":
            device_id = config.get_app("device_id")
            pkg_name = config.get_app("pkg_name")
            self.driver = AndroidDriver(device_id, pkg_name)
        elif platform == "ios":
            device_id = config.get_app("device_id")
            pkg_name = config.get_app("pkg_name")
            self.driver = IosDriver(device_id, pkg_name)
        elif platform == "web":
            browserName = config.get_web("browser_name")
            headless = config.get_web("headless")
            state = config.get_web("state")
            if state:
                state_json = json.loads(state)
                self.driver = PlayWrightDriver(browserName=browserName, headless=headless, state=state_json)
            else:
                self.driver = PlayWrightDriver(browserName=browserName, headless=headless)
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            self.driver.start_app()
        self.start()

    def teardown_method(self):
        self.end()
        if isinstance(self.driver, PlayWrightDriver) == "web":
            self.driver.close()
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            self.driver.stop_app()
        take_time = time.time() - self.start_time
        logger.debug("[run_time]: {:.2f} s".format(take_time))

    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.debug(f"sleep: {n}s")
        time.sleep(n)

    def open(self, url=None):
        """浏览器打开页面"""
        # 拼接域名
        if url is None:
            base_url = config.get_web("base_url")
            if not base_url:
                raise HostIsNull('base_url is null')
            url = base_url
        else:
            if "http" not in url:
                base_url = config.get_web("base_url")
                if not base_url:
                    raise HostIsNull('base_url is null')
                url = parse.urljoin(base_url, url)
        # 访问页面
        self.driver.visit(url)
        # 设置cookies
        cookies = config.get_web("cookies")
        if cookies:
            self.driver.set_cookies(cookies)

    def new_page(self, locator: WebElem):
        """切换到新页签"""
        self.driver.switch_tab(locator)

    def screenshot(self, name: str):
        """截图"""
        self.driver.screenshot(name)

