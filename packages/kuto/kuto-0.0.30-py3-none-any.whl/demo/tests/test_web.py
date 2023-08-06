"""
@Author: kang.yang
@Date: 2023/5/16 14:37
"""
import kuto


class IndexPage(kuto.Page):
    """首页"""
    login = kuto.WebElem(text='登录/注册')
    patent = kuto.WebElem(text='查专利')


class LoginPage(kuto.Page):
    """登录页"""
    pwdLogin = kuto.WebElem(text='帐号密码登录')
    userInput = kuto.WebElem(placeholder='请输入手机号码')
    pwdInput = kuto.WebElem(placeholder='请输入密码')
    licenseBtn = kuto.WebElem(css="span.el-checkbox__inner", index=1)
    loginBtn = kuto.WebElem(text='立即登录')


class TestLogin(kuto.Case):
    """登录测试"""

    def start(self):
        self.index_page = IndexPage(self.driver)
        self.login_page = LoginPage(self.driver)

    def test_1(self):
        """账号密码登录"""
        self.open()
        self.index_page.login.click()
        self.login_page.pwdLogin.click()
        self.login_page.userInput.input('xxx')
        self.login_page.pwdInput.input('xxxx')
        self.login_page.licenseBtn.click()
        self.login_page.loginBtn.click()
        self.index_page.patent.assert_visible()


if __name__ == '__main__':
    # with open("state.json", "r") as f:
    #     state = json.loads(f.read())

    kuto.main(browser="chrome", host="https://www.qizhidao.com")
