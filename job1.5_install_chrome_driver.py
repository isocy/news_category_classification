from webdriver_manager.chrome import ChromeDriverManager

with open('./chrome_driver_path.txt', 'w') as f:
    f.write(ChromeDriverManager().install())
