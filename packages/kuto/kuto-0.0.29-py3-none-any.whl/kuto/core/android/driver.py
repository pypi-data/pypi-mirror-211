import os
import re
import time
import subprocess

# import allure
import allure
import requests
import six
import uiautomator2 as u2

from kuto.core.android.common import check_device
from kuto.utils.exceptions import (
    ScreenFailException,
    PkgIsNull,
    DeviceNotFoundException)
from kuto.utils.log import logger
from kuto.testdata import get_int


class AndroidDriver(object):

    def __init__(self, device_id=None, pkg_name=None):
        self.pkg_name = pkg_name
        if not self.pkg_name:
            raise PkgIsNull('应用包名不能为空')
        self.device_id = device_id
        if not self.device_id:
            raise DeviceNotFoundException('设备id不能为空')

        logger.info(f'init android driver: {device_id}')
        if ':' not in device_id:
            self.device_id = check_device(device_id)
            self.d = u2.connect(self.device_id)
        else:
            self.d = u2.connect_adb_wifi(self.device_id)

        # check if atx is ready.
        self.d.healthcheck()

    @property
    def info(self):
        """连接信息"""
        logger.info(f"get info")
        return self.d.info

    @property
    def app_info(self, pkg_name=None):
        """获取指定应用信息"""
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"get app info: {pkg_name}")
        info = self.d.app_info(pkg_name)
        return info

    @property
    def device_info(self):
        """获取设备信息"""
        logger.info(f"get device info")
        info = self.d.device_info
        return info

    @property
    def page_content(self):
        """获取页面xml内容"""
        logger.info("get page content")
        return self.d.dump_hierarchy()

    def set_delay(self, before: float, after: float):
        """设置操作前置后置默认延时"""
        self.d.settings['operation_delay'] = (before, after)

    def uninstall_app(self, pkg_name=None):
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"uninstall: {pkg_name}")
        self.d.app_uninstall(pkg_name)

    @staticmethod
    def download_apk(src):
        """下载安装包"""
        if isinstance(src, six.string_types):
            if re.match(r"^https?://", src):
                logger.info(f'下载中: {src}')
                file_path = os.path.join(os.getcwd(), src.split('/')[-1])
                r = requests.get(src, stream=True)
                if r.status_code != 200:
                    raise IOError(
                        "Request URL {!r} status_code {}".format(src, r.status_code))
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                logger.info(f'下载成功: {file_path}')
                return file_path
            elif os.path.isfile(src):
                return src
            else:
                raise IOError("file {!r} not found".format(src))

    def install_app(self, apk_path, auth=True, new=True, pkg_name=None):
        """
        安装应用，push改成adb命令之后暂时无法支持远程手机调用
        @param pkg_name: 应用包名
        @param apk_path: 安装包链接，支持本地路径以及http路径
        @param auth: 是否进行授权
        @param new: 是否先卸载再安装
        """
        logger.info(f"install: {apk_path}")
        # 卸载
        if new is True:
            if pkg_name is None:
                pkg_name = self.pkg_name
            self.uninstall_app(pkg_name)

        # 下载
        source = self.download_apk(apk_path)

        # 把安装包push到手机上
        target = "/data/local/tmp/_tmp.apk"
        subprocess.check_call(f'adb -s {self.device_id} push {source} {target}', shell=True)

        # 安装
        cmd_list = ['pm', 'install', "-r", "-t", target]
        if auth is True:
            cmd_list.insert(4, '-g')
        logger.debug(f"{' '.join(cmd_list)}")
        cmd_str = f'adb -s {self.device_id} shell {" ".join(cmd_list)}'
        subprocess.check_call(cmd_str, shell=True)

        logger.info('install success')

        # 删除下载的安装包
        if 'http' in apk_path:
            os.remove(source)

    def start_app(self, pkg_name=None, stop=True):
        """启动应用
        @param pkg_name: 应用包名
        @param stop: 是否先关闭应用再启动
        """
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"start app: {pkg_name}")
        self.d.app_start(pkg_name, stop=stop, use_monkey=True)

    def stop_app(self, pkg_name=None):
        """停止指定应用"""
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"quit app: {pkg_name}")
        self.d.app_stop(pkg_name)

    def clear_app(self, pkg_name=None):
        """清除应用缓存"""
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"clear app: {pkg_name}")
        self.d.app_clear(pkg_name)

    def wait_app_running(self, pkg_name=None, front=True, timeout=20):
        """
        等待应用运行
        @param pkg_name: 应用包名
        @param front: 是否前台运行
        @param timeout: 等待时间
        @return: 应用pid
        """
        if not pkg_name:
            pkg_name = self.pkg_name
        pid = self.d.app_wait(pkg_name, front=front, timeout=timeout)
        if not pid:
            logger.info(f"{pkg_name} is not running")
        else:
            logger.info(f"{pkg_name} pid is {pid}")
        return pid

    def health_check(self):
        """检查设备连接状态"""
        logger.info("health check")
        self.d.healthcheck()

    def open_url(self, url):
        """
        通过url打开web页面或者app schema
        @param url: 页面url，https://www.baidu.com，taobao://taobao.com
        @return:
        """
        logger.info(f"open url or schema: {url}")
        self.d.open_url(url)

    def shell(self, cmd, timeout=60):
        """
        执行adb shell命令
        @param cmd: shell字符串或list，pwd，["ls", "-l"]
        @param timeout: 超时时间
        @return:
        """
        logger.info(f"exec adb shell: {cmd}")
        output, exit_code = self.d.shell(cmd, timeout=timeout)
        return output, exit_code

    def screenshot(self, file_name=None, with_time=True):
        """
        截图并保存到预定路径
        @param with_time: 是否带时间戳
        @param file_name: foo.png or fool
        @return:
        """
        if not file_name:
            raise ValueError("file_name should not be None.")

        try:
            # 把文件名处理成test.png的样式
            if "." in file_name:
                file_name = file_name.split(r".")[0]
            # 截图并保存到当前目录的images文件夹中
            relative_path = "screenshots"
            if os.path.exists(relative_path) is False:
                os.mkdir(relative_path)
            if with_time:
                time_str = time.strftime(f"%Y-%m-%d_%H_%M_%S_{get_int(min_size=1, max_size=1000)}")
                file_name = f"{time_str}_{file_name}.png"
            else:
                file_name = f'{file_name}.png'

            file_path = os.path.join(relative_path, file_name)
            logger.info(f"save to: {os.path.join(relative_path, file_name)}")
            self.d.screenshot(file_path)
            # 上传allure报告
            allure.attach.file(
                file_path,
                attachment_type=allure.attachment_type.PNG,
                name=f"{file_name}",
            )
            return file_path
        except Exception as e:
            raise ScreenFailException(f"screenshot fail: \n{str(e)}")

    def back(self):
        logger.info(f'back')
        self.d.press('back')

    def click(self, x, y):
        """点击坐标"""
        logger.info(f"click : {x},{y}")
        self.d.click(x, y)

    def click_alerts(self, alert_list: list):
        """点击弹窗"""
        logger.info(f"click alerts: {alert_list}")
        with self.d.watch_context() as ctx:
            for alert in alert_list:
                ctx.when(alert).click()
            ctx.wait_stable()

    def swipe(self, sx, sy, ex, ey):
        """滑动"""
        logger.info(f"from {sx},{sy} swipe to {ex},{ey}")
        self.d.swipe(sx, sy, ex, ey)

    def swipe_left(self, scale=0.9):
        """往左滑动"""
        logger.info("swipe left")
        self.d.swipe_ext("left", scale=scale)

    def swipe_right(self, scale=0.9):
        """往右滑动"""
        logger.info("swipe right")
        self.d.swipe_ext("right", scale=scale)

    def swipe_up(self, scale=0.8):
        """往上滑动"""
        logger.info("swipe up")
        self.d.swipe_ext("up", scale=scale)

    def swipe_down(self, scale=0.8):
        """往下滑动"""
        logger.info("swipe down")
        self.d.swipe_ext("down", scale=scale)

    def drag(self, sx, sy, ex, ey):
        """拖动"""
        logger.info(f"from {sx},{sy} drag to {ex},{ey}")
        self.d.drag(sx, sy, ex, ey)

    def set_text(self, text: str):
        """输入框内容"""
        logger.info(f'input: {text}')
        self.d.send_keys(text)


if __name__ == '__main__':
    pass



