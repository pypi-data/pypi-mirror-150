import os
import json
import html
import base64
from chromdroid.webdriver.common.by import By
from chromdroid.webdriver.remote.command import Command
from chromdroid.webdriver.remote.web_element import WebElement
from chromdroid.webdriver.common.exception import NoSuchElementException, NoSuchPageSourceException
from chromdroid.webdriver.remote.remote_connection import RemoteConnection


class WebDriver(RemoteConnection):

    def __init__(self, gui=True, accept_time_out=60, recv_time_out=60):
        super(WebDriver, self).__init__(accept_time_out=accept_time_out)
        self.encode_req = lambda data, encode=True: (
            "%s\n" % data).encode() if encode else "%s\n" % data
        self.gui = gui
        self.dataStartSocket = self.encode_req({
            "command": Command.INIT,
            "host": self.host,
            "port": self.port
        }, False)
        if self.gui:
            os.system(self.command(
                "start", "com.luanon.chromium/com.luanon.chromium.MainActivity", self.dataStartSocket))
        else:
            os.system(self.command("startservice",
                      "com.luanon.chromium/.MainService", self.dataStartSocket))
        try:
            self.client_accept = self.accept()[0]
            self.client_accept.settimeout(recv_time_out)
        except TimeoutError:
            self.exception(TimeoutError, "Could not connect chrome webdriver")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    #----------utils----------#

    def command(self, action, name, data=""):
        # adb shell am start -n "com.luanon.chromium/com.luanon.chromium.MainActivity" -d "{'command': 'init', 'host': '127.0.0.1', 'port': 5000}"
        #  > /dev/null
        return "am %s -n %s -d '%s' > /dev/null" % (action, name, data)

    def check_result(self, commnad, recv):
        try:
            data = json.loads(recv)
        except:
            return {'result': None}
        if commnad == data.get("command", None):
            if 'encode' in data:
                result = base64.b64decode(data.get("result", None)).decode()
            else:
                result = data.get("result", None)
            if result:
                result = " ".join(result.split())  # remove \t \n characters
                try:
                    return {**data, **{"result": eval(result)}}
                except Exception:
                    if result == "null" or result == "undefined":
                        return {**data, **{"result": None}}
                    elif result == "true" or result == "false":
                        return {**data, **{"result": eval(result.capitalize())}}
                    else:
                        return {**data, **{"result": result}}
            else:  # empty or None or ?
                return {**data, **{"result": None}}

    def decode(self, data):
        try:
            return html.unescape(data.decode("unicode-escape").encode("latin1").decode("utf8"))
        except Exception:
            try:
                return data.decode("unicode-escape").encode("latin1").decode("utf8")
            except Exception:
                return data

    def exception(self, type_, msg=""):
        print("< %s :: %s >" % (type_.__name__, msg))
        exit()

    def execute(self, command, **kwargs):
        data = self.encode_req({
            "command": command,
            **kwargs
        })
        try:
            self.client_accept.send(data)
        except:
            print('DISCONNECT VỚI APP, VUI LÒNG TẮT APP ĐI VÀ CHẠY LẠI TOOL')
            exit(0)
            return {'result': None}
        recv = self.recv_all()
        if recv == 'continue':
            return {'result': None}
        return self.check_result(command, recv)

    def recv_all(self):
        """
            byte or string faster?
            byte faster 0.2 - 1 second
        """
        result = b""
        length = b""
        try:
            while True:
                data = self.client_accept.recv(1)
                if not data.decode().isdigit():
                    result += data
                    break
                length += data
            length = int(length.decode())
        except Exception as e:
            s = repr(e)
            if 'invalid literal for int() with base' in s:
                # os.system(self.command(
                #     "start", "com.luanon.chromium/com.luanon.chromium.MainActivity", self.dataStartSocket))
                print(
                    'DISCONNECT VỚI APP CHROMIUM, VUI LÒNG TẮT APP ĐI VÀ CHẠY LẠI TOOL')
                exit(0)
                return 'continue'
            length = 0
        if length == 0:
            # os.system(self.command(
            #     "start", "com.luanon.chromium/com.luanon.chromium.MainActivity", self.dataStartSocket))
            print('DISCONNECT VỚI APP CHROMIUM, VUI LÒNG TẮT APP ĐI VÀ CHẠY LẠI TOOL')
            exit(0)
            return 'continue'

        while len(result) < length:
            result += self.client_accept.recv(self.max_recv)
        return self.decode(result)

    #----------function----------#

    def close(self):
        return self.execute(Command.CLOSE)["result"]

    @property
    def current_url(self):
        return self.execute(Command.CURRENT_URL)["result"]

    def execute_script(self, script):
        return self.execute(Command.EXECUTE_SCRIPT, script=script)["result"]

    def find_element_by_id(self, id_):
        return self.find_element(by=By.ID, value=id_)

    def find_element_by_xpath(self, xpath):
        return self.find_element(by=By.XPATH, value=xpath)

    def find_element_by_link_text(self, link_text):
        return self.find_element(by=By.LINK_TEXT, value=link_text)

    def find_element_by_partial_link_text(self, partial_link_text):
        return self.find_element(by=By.PARTIAL_LINK_TEXT, value=partial_link_text)

    def find_element_by_name(self, name):
        return self.find_element(by=By.NAME, value=name)

    def find_element_by_tag_name(self, tag_name):
        return self.find_element(by=By.TAG_NAME, value=tag_name)

    def find_element_by_class_name(self, class_name):
        return self.find_element(by=By.CLASS_NAME, value=class_name)

    def find_element_by_css_selector(self, css_selector):
        return self.find_element(by=By.CSS_SELECTOR, value=css_selector)

    def find_elements_by_id(self, id_):
        return self.find_elements(by=By.ID, value=id_)

    def find_elements_by_xpath(self, xpath):
        return self.find_elements(by=By.XPATH, value=xpath)

    def find_elements_by_link_text(self, link_text):
        return self.find_elements(by=By.LINK_TEXT, value=link_text)

    def find_elements_by_partial_link_text(self, partial_link_text):
        return self.find_elements(by=By.PARTIAL_LINK_TEXT, value=partial_link_text)

    def find_elements_by_name(self, name):
        return self.find_elements(by=By.NAME, value=name)

    def find_elements_by_tag_name(self, tag_name):
        return self.find_elements(by=By.TAG_NAME, value=tag_name)

    def find_elements_by_class_name(self, class_name):
        return self.find_elements(by=By.CLASS_NAME, value=class_name)

    def find_elements_by_css_selector(self, css_selector):
        return self.find_elements(by=By.CSS_SELECTOR, value=css_selector)

    def find_element(self, by, value):
        element = self.execute(Command.FIND_ELEMENT, by=by, value=value)
        if not element["result"]:
            return None
        return WebElement(self.execute, element)

    def find_elements(self, by, value):
        elements = self.execute(Command.FIND_ELEMENTS, by=by, value=value)
        result = []
        for element in elements["result"]:
            data = {**elements, **{"command": Command.FIND_ELEMENT, "element_path": "%s[%s]" % (
                elements["element_path"], element[0]), "result": element[1]}}
            result.append(WebElement(self.execute, data))
        return result

    def get(self, url):
        return self.execute(Command.GET, url=url)["result"]

    @property
    def page_source(self):
        page_source = self.execute(Command.PAGE_SOURCE)
        if not page_source:
            self.exception(NoSuchPageSourceException,
                           "If you get this error please report me on github")
        # its base64 so decode later
        return page_source['result']

    @property
    def title(self):
        return self.execute(Command.TITLE)["result"]

    def get_cookie(self, name, domain: str or None = ""):
        return self.execute(Command.GET_COOKIE, domain=domain, keys=name)["result"]

    def setCookie(self, name, value, domain: str or None = ""):
        return self.execute(Command.SET_COOKIE, domain=domain, keys=name, value=value)["result"]
