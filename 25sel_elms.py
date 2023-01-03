import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# pytest -v --driver Chrome --driver-path C:/Users/Artesk/chromedriver_win32/chromedriver.exe 25sel_elms.py


@pytest.fixture(autouse=True)
def open_page_precondition():
    pytest.driver = webdriver.Chrome('C:/Users/Artesk/chromedriver_win32/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('kalistratov.arte@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('123')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # # Переходим на страницу Мои питомцы
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    yield
    pytest.driver.quit()



def test_all_pets_here():
    # неявное ожидание отображения кнопки 'Добавить питомца'
    element = WebDriverWait(pytest.driver, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn-outline-success')))
    # Карточки всех питомцев
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Находим элемент, отражающий количество питомцев, в карточке пользователя
    pets_qty_displayed = pytest.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text.split(": ")[1]
    # Сравниваем количество карточек питомцев со статистикой пользователя
    assert pets_qty_displayed == f'{len(all_pets)}\nДрузей'


def test_half_pets_have_photo():
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Находим элементы, куда должны загружаться фото питомцев
    img_placeholders = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    # Проходимся по всем элементам, где должно быть загружено фото питомца
    images = 0
    for i in range(len(all_pets)):
        # Если фото найдено, увеличиваем счетчик  на 1
        if img_placeholders[i].get_attribute('src') != '':
            images += 1
    # Сравниваем количество фотографий с количеством карточек питомцев, разделенным пополам
    assert images >= len(all_pets) / 2


def test_all_pets_full_info():
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Находим элементы, содержащие имя, породу, возраст питомца
    pet_params = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td')
    # Проходимся по всем элементам, где может встретиться имя, порода, возраст питомца,
    # удостоверяемся в отсутствии пустых строк
    for i in range(len(all_pets)):
        assert pet_params[i].text != ''


def test_duplicate_names():
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Находим все элементы, содержащие имена питомцев
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    # Проходимся по всем карточкам и сравниваем, совпадают ли данные питомца
    # со всеми оставшимися питомцами до конца списка
    for i in range(len(all_pets) - 1):
        for j in range(i + 1, len(all_pets)):
            assert names[i].text != names[j].text


def test_duplicate_pets():
    # неявное ожидание карточек всех питомцев
    pytest.driver.implicitly_wait(10)
    myDynamicElement = pytest.driver.find_elements(By.TAG_NAME, 'tr')
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    # Создаем пустой список, куда будем добавлять свойства (имя, порода, возраст) всех питомцев
    all_pets_props = []
    # Создаем список свойств отдельного питомца
    pet_props = []
    # Перебираем карточки всех животных
    for i in range(1, len(all_pets)):
        # проходимся по элементам, где содержатся свойства отдельного питомца
        for j in range(1, 4):
            pet_props_element = pytest.driver.find_element(By.XPATH,
                                                           f'//*[@id="all_my_pets"]/table/tbody/tr[{i}]/td[{j}]')
            # добавляем найденные свойства в список для каждого питомца
            pet_props.append(pet_props_element.text)
            # Списки свойств всех питомцев добавляем в общий список
    for k in range(0, len(pet_props), 3):
        all_pets_props.append([pet_props[k], pet_props[k + 1], pet_props[k + 2]])
    # Перебираем общий список
    for l in range((len(all_pets_props) - 1)):
        for m in range(l + 1, len(all_pets_props)):
            assert all_pets_props[l] != all_pets_props[m]
