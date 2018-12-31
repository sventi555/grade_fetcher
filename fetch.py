from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    print('going to quest')
    driver.get('https://quest.pecs.uwaterloo.ca/psp/SS/ACADEMIC/SA/?cmd=login&languageCd=ENG')
    assert 'Quest' in driver.title

    print('going to login page')
    sign_in = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Sign in')))
    sign_in.click()

    print('signing in')
    username = wait.until(EC.visibility_of_element_located((By.ID, 'username')))
    password = wait.until(EC.visibility_of_element_located((By.ID, 'password')))
    login_button = wait.until(EC.visibility_of_element_located((By.NAME, '_eventId_proceed')))

    username.clear()
    username.send_keys(input('enter your username: '))

    password.clear()
    password.send_keys(input('enter your password: '))

    login_button.click()

    assert 'Student Center' in driver.title

    print('going to my academics')
    frame = wait.until(EC.visibility_of_element_located((By.XPATH, '//iframe')))
    driver.switch_to.frame(frame)
    my_academics = wait.until(EC.visibility_of_element_located((By.ID, 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR1')))
    my_academics.click()

    print('selecting term')
    radio_input = wait.until(EC.visibility_of_element_located((By.ID, 'SSR_DUMMY_RECV1$sels$1$$0')))
    radio_input.click()

    cont_button = wait.until(EC.visibility_of_element_located((By.ID, 'UW_DRVD_SSS_SCT_SSR_PB_GO')))
    cont_button.click()

    print('\n')
    for i in range(5):
        label = wait.until(EC.visibility_of_element_located((By.ID, f'CLS_LINK$span${i}')))
        mark = wait.until(EC.visibility_of_element_located((By.ID, f'STDNT_ENRL_SSV1_CRSE_GRADE_OFF${i}')))

        print(label.text + ' - ' + mark.text)
        print(' - ')


if __name__ == "__main__":
    main()






