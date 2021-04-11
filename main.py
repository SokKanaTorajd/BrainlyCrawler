from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, ElementNotInteractableException
from time import sleep
from database import dbBrainly

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

    except ElementNotInteractableException:
        print('tidak ada popup')
        pass

def get_info(driver, url):
    driver.get(url)
    sleep(3)
    check_pop_up(driver)
    # MAPEL
    subject_elem = "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/article/div/div/div[1]/div/div[2]/ul/li[2]/a"
    subject_name = driver.find_element_by_xpath(subject_elem).text
    # Text Pertanyaan
    text_elem = "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/article/div/div/div[2]/div/div/h1"
    text = driver.find_element_by_xpath(text_elem).text
    # Status
    button_style = 'span.sg-button__text'
    content = driver.find_element_by_id('question-sg-layout-container')
    span_text = content.find_element_by_css_selector(button_style).text

    if 'LIHAT JAWABAN' in span_text:
        status = True
    else:
        status = False

    data = {
        'url': url,
        'subjects': subject_name,
        'text_soal': text,
        'status': status
        }

    return data

def get_subject_links(driver):
    driver.implicitly_wait(10)
    xpath_indo = '/html/body/div[5]/div/div[1]/div[2]/div[2]'
    driver.find_element_by_xpath(xpath_indo).click()

    xpath_load = '//*[@id="loadMore"]'
    for i in range(10):
        driver.find_element_by_xpath(xpath_load).click()
        sleep(3)
        print('load ke {}'.format(i))

    xpath_queue = '/html/body/div[5]/div/div[2]/div/div'
    for q in range(50):
        driver.find_element_by_xpath(xpath_queue + '/div[{}]'.format(q+1))
        xpath_answer = '/html/body/div[5]/div/div[2]/div/div/div[{}]/div/div/div/div[2]/div[2]/button/a'.format(q+1)
        href = driver.find_element_by_xpath(xpath_answer).get_attribute('href')
        db.insert_url('bindo', href)
        sleep(3)
        print('data dimasukkan')


if __name__ == '__main__':
    db = dbBrainly()
    driver = get_browser()

    # # GET URL
    # url = 'https://id.brainly.vip/unanswered'
    # driver.get(url)
    # get_subject_links(driver)

    # GET INFO FROM URL
    data = db.get_all_urls('bindo')
    for url in data:
        try:
            u = url['url']
            collected = get_info(driver, u)
            db.insert_info('info', collected)
            print('info inserted')
            sleep(3)

        except NoSuchElementException:
            print('url error')
            pass

    # TEST GET INFO
    # url = ['https://brainly.co.id/tugas/40229022', 'https://brainly.co.id/tugas/40139379']
    # for u in url:
    #     collected = get_info(driver, u)
    #     sleep(5)

    # driver.close()

