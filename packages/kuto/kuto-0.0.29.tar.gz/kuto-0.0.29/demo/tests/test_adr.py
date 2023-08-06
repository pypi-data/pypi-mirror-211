import kuto


class HomePage(kuto.Page):
    """首页"""
    ad = kuto.Elem(resourceId='com.qizhidao.clientapp:id/bottom_btn')
    my = kuto.Elem(text='我的')


class MyPage(kuto.Page):
    """我的页"""
    setting = kuto.Elem(resourceId='com.qizhidao.clientapp:id/me_top_bar_setting_iv')


class TestSetting(kuto.Case):
    """设置页测试"""

    def start(self):
        self.home_page = HomePage(self.driver)
        self.my_page = MyPage(self.driver)

    def test_1(self):
        """进入设置页"""
        self.home_page.ad.click_exists(timeout=5)
        self.home_page.my.click()
        self.my_page.setting.click()


if __name__ == '__main__':
    kuto.main(did='UJK0220521066836', pkg='com.qizhidao.clientapp')

