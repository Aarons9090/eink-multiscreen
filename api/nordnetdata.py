from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display
import time


def get_account_data():
    CONFIG = dotenv_values("api/.env")
    username = CONFIG["username"]
    password = CONFIG["password"]

    display = Display(visible=0, size=(1600,1200))
    display.start()
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    driver.get('https://www.nordnet.fi/kirjaudu?redirect_to=%2Fyleisnakyma')
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "#cookie-accept-all-secondary").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        "#main-content > div > div > div.Card__StyledCard-sc-1e5czjc-0.fiKbAx.styles__StyledCard-sc-18kw6md-2.dVZQCj > div > div > div.Flexbox__StyledFlexbox-sc-1ob4g1e-0.dHQEge > div:nth-child(1) > span > button > span > span").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        "#main-content > div > div > div.Card__StyledCard-sc-1e5czjc-0.fiKbAx.styles__StyledCard-sc-18kw6md-2.dVZQCj > div > div > div.Flexbox__StyledFlexbox-sc-1ob4g1e-0.dHQEge > div:nth-child(1) > span > button > span > span").click()
    time.sleep(1)

    # username
    driver.find_element(By.CSS_SELECTOR,
                        "#main-content > div > div > div.Card__StyledCard-sc-1e5czjc-0.fiKbAx.styles__StyledCard-sc-18kw6md-2.dVZQCj > div > div > div.Flexbox__StyledFlexbox-sc-1ob4g1e-0.eCdrRF.styles__StyledFlexboxItem-sc-18kw6md-3.eMlxoG > form > div.FormField__Wrapper-sc-ydn0fr-0.ctYtKf.style__StyledInput-sc-optwx8-2.jEiWeT > label > span > span > div > input"
                        ).send_keys(username)
    time.sleep(1)

    # password
    driver.find_element(By.CSS_SELECTOR,
                        "#main-content > div > div > div.Card__StyledCard-sc-1e5czjc-0.fiKbAx.styles__StyledCard-sc-18kw6md-2.dVZQCj > div > div > div.Flexbox__StyledFlexbox-sc-1ob4g1e-0.eCdrRF.styles__StyledFlexboxItem-sc-18kw6md-3.eMlxoG > form > div:nth-child(2) > label > span > span > div > input"
                        ).send_keys(password)
    time.sleep(1)
    # login
    driver.find_element(By.CSS_SELECTOR,
                        "#main-content > div > div > div.Card__StyledCard-sc-1e5czjc-0.fiKbAx.styles__StyledCard-sc-18kw6md-2.dVZQCj > div > div > div.Flexbox__StyledFlexbox-sc-1ob4g1e-0.eCdrRF.styles__StyledFlexboxItem-sc-18kw6md-3.eMlxoG > form > div.Box__StyledDiv-sc-1bfv3i9-0.jkmbat > button"
                        ).click()

    time.sleep(7)

    # click 5y
    driver.find_element(By.CSS_SELECTOR,
                        "#main-content > div > div.page-overview__StyledBackground-sc-14oq34i-0.ikOARW > div > div > div > div > div.CssGrid__RawCssGridItem-sc-bu5cxy-1.CssGrid___StyledRawCssGridItem-sc-bu5cxy-2.bxeRgc.gAoEdt > div > div > div > div > div > div.CssGrid__RawCssGridItem-sc-bu5cxy-1.CssGrid___StyledRawCssGridItem-sc-bu5cxy-2.bxeRgc.lcShDN > div > div > div.Box__StyledDiv-sc-1bfv3i9-0.iVlgoS > div > div:nth-child(7) > button > span > span"
                        ).click()

    time.sleep(1)
    capital = driver.find_element(By.CSS_SELECTOR,
                                  "#main-content > div > div.page-overview__StyledBackground-sc-14oq34i-0.ikOARW > div > div > div > div > div.CssGrid__RawCssGridItem-sc-bu5cxy-1.CssGrid___StyledRawCssGridItem-sc-bu5cxy-2.bxeRgc.gAoEdt > div > div > div > div > div > div.CssGrid__RawCssGridItem-sc-bu5cxy-1.CssGrid___StyledRawCssGridItem-sc-bu5cxy-2.bxeRgc.qnyTu > div > div > span"
                                  ).text
    today_change = driver.find_element(By.CSS_SELECTOR,
                                       "#main-content > div > div.page-overview__StyledBackground-sc-14oq34i-0.ikOARW > div > div > div > div > div.CssGrid__RawCssGridItem-sc-bu5cxy-1.CssGrid___StyledRawCssGridItem-sc-bu5cxy-2.bxeRgc.gAoEdt > div > div > div > div > div > div.CssGrid__RawCssGridItem-sc-bu5cxy-1.CssGrid___StyledRawCssGridItem-sc-bu5cxy-2.bxeRgc.diAowE > div > div > span"
                                       ).text
    today_change_euros = str(today_change).split("%")[1]
    max_change = driver.find_element(By.CSS_SELECTOR,
                                     "#main-content > div > div.page-overview__StyledBackground-sc-14oq34i-0.ikOARW > div > div > div > div > div.CssGrid__RawCssGridItem-sc-bu5cxy-1.CssGrid___StyledRawCssGridItem-sc-bu5cxy-2.bxeRgc.gAoEdt > div > div > div > div > div > div.CssGrid__RawCssGridItem-sc-bu5cxy-1.CssGrid___StyledRawCssGridItem-sc-bu5cxy-2.bxeRgc.lcShDN > div > div > div.Box__StyledDiv-sc-1bfv3i9-0.dAEdOQ.Header__StyledBox-sc-1npdi92-1.kVorBO > div.Flexbox__StyledFlexbox-sc-1ob4g1e-0.vMAWR > div.Flexbox__StyledFlexbox-sc-1ob4g1e-0.kWkSsH > span > div > div > span:nth-child(2)"
                                     ).text
    max_change_euros = str(max_change).split("EUR")[0].strip()

    return {
       "capital":  capital,
       "today_change": today_change_euros,
       "max_change":  max_change_euros
    }

