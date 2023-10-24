from datetime import datetime

today = datetime.today()
today_format = today.strftime("%d_%m_%Y-%I_%M_%S")
print(str(today_format))
