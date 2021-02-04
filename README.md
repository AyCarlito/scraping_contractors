# Defence Contractor Automated Scraping

This program makes use of the beautiful soup and smtp libraries. The purpose is to scrape the US Department of Defence website to retrirve contracts given out on the current day. Content is parsed based on sentences which include a US state name, reducing redundant. information and providing company name and contract value.

SMTP libary is used to alllow for the text file of parsed data to be sent to specified email addresses.