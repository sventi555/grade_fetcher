from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from getpass import getpass


def find(field_type, field, wait):
    if field_type == 'id':
        return wait.until(EC.visibility_of_element_located((By.ID, field)))
    elif field_type == 'xpath':
        return wait.until(EC.visibility_of_element_located((By.XPATH, field)))
    elif field_type == 'link_text':
        return wait.until(EC.visibility_of_element_located((By.LINK_TEXT, field)))
    elif field_type == 'name':
        return wait.until(EC.visibility_of_element_located((By.NAME, field)))


def main():
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    print('going to quest')
    driver.get('https://quest.pecs.uwaterloo.ca/psp/SS/ACADEMIC/SA/?cmd=login&languageCd=ENG')
    assert 'Quest' in driver.title

    print('going to login page')
    sign_in = find('link_text', 'Sign in', wait)
    sign_in.click()

    print('signing in')
    username = find('id', 'username', wait)
    password = find('id', 'password', wait)
    login_button = find('name', '_eventId_proceed', wait)

    username.clear()
    username.send_keys(input('enter your username: '))

    password.clear()
    password.send_keys(getpass('enter your password: '))

    login_button.click()

    assert 'Student Center' in driver.title

    print('going to my academics')
    frame = find('xpath', '//iframe', wait)
    driver.switch_to.frame(frame)
    my_academics = find('id', 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR1', wait)
    my_academics.click()

    term_table = find('xpath', "//table[@id='SSR_DUMMY_RECV1$scroll$0']/tbody", wait)
    term_rows = term_table.find_elements_by_xpath('tr[position()>2]')
    num_terms = len(term_rows)

    print(f'Select the term you want to view (0...{num_terms - 1})')
    for i in range(num_terms):
        label = term_rows[i].find_element_by_id(f'TERM_CAR${i}').text
        print(f'{i}: ' + label)

    selected_term = input('Enter a valid option: ')

    radio_input = find('id', f'SSR_DUMMY_RECV1$sels${selected_term}$$0', wait)
    radio_input.click()

    cont_button = find('id', 'UW_DRVD_SSS_SCT_SSR_PB_GO', wait)
    cont_button.click()

    grades_table = find('id', 'TERM_CLASSES$scroll$0', wait)
    grade_rows = grades_table.find_elements_by_xpath('.//table/tbody/tr[position()>1]')
    num_grades = len(grade_rows)

    print('\n')
    for i in range(num_grades):
        label = wait.until(EC.visibility_of_element_located((By.ID, f'CLS_LINK$span${i}')))
        mark = wait.until(EC.visibility_of_element_located((By.ID, f'STDNT_ENRL_SSV1_CRSE_GRADE_OFF${i}')))

        print(label.text + ' - ' + mark.text)
        print('----------------------')


if __name__ == "__main__":
    main()






