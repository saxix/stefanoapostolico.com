from time import sleep
from selenium import webdriver

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference("permissions.default.subdocument", 2)
firefox_profile.set_preference("permissions.default.script", 2)
firefox_profile.set_preference("javascript.enabled", False)
firefox_profile.set_preference("layout.css.filters.enabled", True)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',
                                          'false')

driver = webdriver.Firefox(firefox_profile)
#driver.get('http://google.com/search?q=nelson+mandela')

driver.get("http://search.yahoo.com/search?p=nelson+mandela")

sleep(100)
driver.close()
