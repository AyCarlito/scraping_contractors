import requests
import datetime
import smtplib
from email.message import EmailMessage

from nltk import tokenize
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
branches = ["NAVY", "ARMY", "AIR FORCE", "DEFENSE LOGISTICS AGENCY"]
months = {
    1:"Jan", 
    2:"Feb",
    3:"Mar",
    4:"Apr",
    5:"May",
    6:"Jun",
    7:"Jul",
    8:"Aug",
    9:"Sep",
    10:"Oct",
    11:"Nov",
    12:"Dec"
    }

now = datetime.datetime.now()
formatted_date = "%s. %i, %i" % (months[now.month], now.day, now.year)
url = "https://www.defense.gov/Newsroom/Contracts/"
page = requests.get(url)


soup = BeautifulSoup(page.content, "html.parser")
dates = soup.find("div", {"id": "alist"})
contracts_url = dates.find("a")['href']
contracts_page = requests.get(contracts_url)

soup = BeautifulSoup(contracts_page.content, "html.parser")
contracts = soup.find_all("p")

extracted = []
for branch in contracts:
    branch_info = "".join(branch.find_all(text=True))
    if branch_info in branches:
        extracted.append("\n%s" % branch_info)
    tokens = tokenize.sent_tokenize(branch_info)
    if tokens:
        all_words = [word_tokenize(i) for i in tokens]
        for sentence in all_words:
            for word in sentence:
                if word in state_names:
                    index = [i for i, lst in enumerate(all_words) if word in lst][0]
                    extracted.append(tokens[index])


extracted = list(dict.fromkeys(extracted))

with open("contracts.txt", "w") as f:
    for item in extracted:
        f.write("%s\n" % item)

with open("contracts.txt", "r") as f:
    file_data = f.read()
    file_name = f.name


EMAIL_ADRESS = "<EMAIL ADDRESS>"
EMAIL_PASSWORD = "<EMAIL PASSWORD>"

msg = EmailMessage()
msg['Subject'] = "Defence Contractors"
msg['From'] = EMAIL_ADRESS
msg['To'] = '<RECIPIENT EMAIL ADDRESS>
msg.set_content("File Attached...")

msg.add_attachment(file_data, filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
