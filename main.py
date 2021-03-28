from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep


def get_browser():
    opts = Options()
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    driver = Chrome(executable_path='chromedriver.exe', options=opts)
    
    return driver

def check_pop_up(driver):
    pop_up_elem = '/html/body/div[2]/div/div[3]'
    driver.implicitly_wait(15)
    try:
        driver.find_element_by_xpath(pop_up_elem).click()
        print('udah di close')

    except NoSuchElementException:
        print('tidak muncul')
        pass

def get_info(driver, url):
    driver.get(url)
    check_pop_up(driver)
    button_style = 'span.sg-button__text'
    content = driver.find_element_by_id('question-sg-layout-container')
    span_text = content.find_element_by_css_selector(button_style).text
    # print(span_text)
    return span_text

def get_subject_links(driver):
    driver.implicitly_wait(10)
    xpath_indo = '/html/body/div[5]/div/div[1]/div[2]/div[2]'
    driver.find_element_by_xpath(xpath_indo).click()

    xpath_load = '//*[@id="loadMore"]'
    for i in range(10):
        driver.find_element_by_xpath(xpath_load).click()
        sleep(3)
        print('load ke {}'.format(i))
        i+=1

    xpath_queue = '/html/body/div[5]/div/div[2]/div/div'
    queue = driver.find_elements_by_xpath(xpath_queue)
    # print(len(queue))
    for q in range(len(queue)):
        driver.find_element_by_xpath(xpath_queue + '/div[{}]'.format(q+1))
        xpath_answer = '/html/body/div[5]/div/div[2]/div/div/div[{}]/div/div/div/div[2]/div[2]/button/a'.format(q+1)
    #     href = driver.find_element_by_xpath(xpath_answer).get_attribute('href')
    #     sleep(3)
    #     print(href)

# /html/body/div[5]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/button/a
# /html/body/div[5]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/button/a

if __name__ == '__main__':
    driver = get_browser()
    url = 'https://id.brainly.vip/unanswered'
    driver.get(url)
    get_subject_links(driver)

    # driver.close()

