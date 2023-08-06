from je_web_runner import get_webdriver_manager

if __name__ == "__main__":
    driver_wrapper = get_webdriver_manager("firefox")
    driver = driver_wrapper.current_webdriver
    driver.get("http://www.python.org")
    print(driver.title)
    driver_wrapper.quit()
