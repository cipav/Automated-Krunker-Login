from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk, Label, Entry, Button
from selenium.common.exceptions import TimeoutException
import time

def accept_tos():
    try:
        accept_button = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        accept_button.click()
    except Exception as e:
        print("An error occurred while accepting TOS:", e)

def login_to_krunker():
    username = username_entry.get()
    password = password_entry.get()

    try:
        driver.get("https://krunker.io/social.html")
        
        accept_tos()

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[4]/div[2]/div[2]'))
        )
        
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="accName"]'))
        )
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="accPass"]'))
        )

        username_input = driver.find_element(By.XPATH, '//*[@id="accName"]')
        password_input = driver.find_element(By.XPATH, '//*[@id="accPass"]')
        username_input.send_keys(username)
        password_input.send_keys(password)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[11]/div[5]/div/div[4]/div'))
        )
        submit_button.click()

        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="success"]'))
        )
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[11]/div[5]'))
        )

        if success_message.is_displayed():
            print("Login successful!")
        elif error_message.is_displayed():
            error_text = error_message.text
            if "incorrect" in error_text.lower():
                print("Login failed: Incorrect username or password.")
            elif "blocked" in error_text.lower():
                print("Login failed: Your account is blocked.")
            else:
                print("Login failed: Unknown reason. Error message:", error_text)
        else:
            print("Login status unknown.")

    except TimeoutException:
        print("Login button or input fields not found.")
    except Exception as e:
        print("An error occurred during login:", e)
    finally:
        time.sleep(5)
        driver.quit()


window = Tk()
window.title("Krunker Login")

username_label = Label(window, text="Username:")
username_label.grid(row=0, column=0)
username_entry = Entry(window)
username_entry.grid(row=0, column=1)

password_label = Label(window, text="Password:")
password_label.grid(row=1, column=0)
password_entry = Entry(window, show="*")
password_entry.grid(row=1, column=1)

login_button = Button(window, text="Login", command=login_to_krunker)
login_button.grid(row=2, columnspan=2)

driver = webdriver.Chrome()

window.mainloop()
