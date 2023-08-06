import html
import base64

from chromdroid.webdriver.common.by import By
from chromdroid.webdriver.remote.command import Command
from chromdroid.webdriver.common.exception import NoSuchElementException, NoSuchPageSourceException, InvalidElementStateException


class WebElement:

    def __init__(self, execute, element):
        self.execute = execute
        self.command = element["command"]
        self.by = element["by"]
        self.value = element["value"]
        self.result = element["result"]
        self.element_path = element["element_path"]

    def __repr__(self):
        return "WebElement(%s)" % self.result

    #----------utils----------#

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

    #----------function----------#

    def click(self):
        # i dont know
        return self.execute(self.command, request=Command.CLICK, element_path=self.element_path, by=self.by, value=self.value)["result"] or True

    def clear(self):
        # i dont know
        return self.execute(self.command, request=Command.CLEAR, element_path=self.element_path, by=self.by, value=self.value)["result"] or True

    def focus(self):
        # i dont know
        return self.execute(self.command, request=Command.FOCUS, element_path=self.element_path, by=self.by, value=self.value)["result"] or True

    def find_element_by_id(self, id_):
        return self.find_element(by=By.ID, value=id_)

    def find_element_by_name(self, name):
        return self.find_element(by=By.NAME, value=name)

    def find_element_by_xpath(self, xpath):
        return self.find_element(by=By.XPATH, value=xpath)

    def find_element_by_link_text(self, link_text):
        return self.find_element(by=By.LINK_TEXT, value=link_text)

    def find_element_by_partial_link_text(self, partial_link_text):
        return self.find_element(by=By.PARTIAL_LINK_TEXT, value=partial_link_text)

    def find_element_by_tag_name(self, tag_name):
        return self.find_element(by=By.TAG_NAME, value=tag_name)

    def find_element_by_class_name(self, class_name):
        return self.find_element(by=By.CLASS_NAME, value=class_name)

    def find_element_by_css_selector(self, css_selector):
        return self.find_element(by=By.CSS_SELECTOR, value=css_selector)

    def find_elements_by_id(self, id_):
        return self.find_elements(by=By.ID, value=id_)

    def find_elements_by_name(self, name):
        return self.find_elements(by=By.NAME, value=name)

    def find_elements_by_xpath(self, xpath):
        return self.find_elements(by=By.XPATH, value=xpath)

    def find_elements_by_link_text(self, link_text):
        return self.find_elements(by=By.LINK_TEXT, value=link_text)

    def find_elements_by_partial_link_text(self, partial_link_text):
        return self.find_elements(by=By.PARTIAL_LINK_TEXT, value=partial_link_text)

    def find_elements_by_tag_name(self, tag_name):
        return self.find_elements(by=By.TAG_NAME, value=tag_name)

    def find_elements_by_class_name(self, class_name):
        return self.find_elements(by=By.CLASS_NAME, value=class_name)

    def find_elements_by_css_selector(self, css_selector):
        return self.find_elements(by=By.CSS_SELECTOR, value=css_selector)

    def find_element(self, by, value):
        element = self.execute(
            Command.FIND_ELEMENT, element_path=self.element_path, by=by, value=value)
        if not element["result"]:
            self.exception(NoSuchElementException,
                           "No element match with by=By.%s value=%s" % (by, value))
        return WebElement(self.execute, element)

    def find_elements(self, by, value):
        elements = self.execute(
            Command.FIND_ELEMENTS, element_path=self.element_path, by=by, value=value)
        result = []
        for element in elements["result"]:
            data = {**elements, **{"command": Command.FIND_ELEMENT, "element_path": "%s[%s]" % (
                elements["element_path"], element[0]), "result": element[1]}}
            result.append(WebElement(self.execute, data))
        return result

    def get_attribute(self, name):
        if name == "class":
            name = "className"
        # i dont know
        return self.execute(self.command, request=Command.GET_ATTRIBUTE, keys=name, element_path=self.element_path, by=self.by, value=self.value)["result"] or ""

    @property
    def is_disabled(self):
        # i dont know
        return self.execute(self.command, request=Command.IS_DISABLED, element_path=self.element_path, by=self.by, value=self.value)["result"] or ""

    @property
    def is_readonly(self):
        # i dont know
        return self.execute(self.command, request=Command.IS_READ_ONLY, element_path=self.element_path, by=self.by, value=self.value)["result"] or False

    def send_keys(self, keys):
        if isinstance(keys, str):
            if self.is_readonly:
                self.exception(InvalidElementStateException,
                               "Element is read-only: %s" % self.result)
            self.focus()
            # i dont know
            return self.execute(self.command, request=Command.SEND_KEYS, keys=keys, element_path=self.element_path, by=self.by, value=self.value)["result"] or True

    def set_value(self, keys):
        if isinstance(keys, str):
            # i dont know
            return self.execute(self.command, request=Command.SET_VALUE, keys=keys, element_path=self.element_path, by=self.by, value=self.value)["result"] or True

    def set_disabled(self, value):
        if value:
            # i dont know
            return self.execute(self.command, request=Command.SET_DISABLED, keys="true", element_path=self.element_path, by=self.by, value=self.value)["result"] or True
        else:
            # i dont know
            return self.execute(self.command, request=Command.SET_DISABLED, keys="false", element_path=self.element_path, by=self.by, value=self.value)["result"] or True
