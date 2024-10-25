from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


class ChromeDriverLoader:

    def __init__(self,
                 userAgent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, "
                                  "like Gecko) Chrome/61.0.3163.100 Safari/537.36") -> None:
        super().__init__()

        self.__userAgent = userAgent

    def get_driver(self) -> WebDriver:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("lang=ko_KR")
        options.add_argument(
            f"user-agent={self.__userAgent}")

        driver = webdriver.Chrome(options=options)

        return driver
