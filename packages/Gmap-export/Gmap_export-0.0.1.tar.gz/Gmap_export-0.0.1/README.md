from Gmap_data import Google_map


Google_url = "https://www.google.com/maps/search/dentist+new+york/@40.7403671,-74.0224996,13z/data=!3m1!4b1?entry=ttu"
Data_csv = "C://Users//EDITOR//Desktop//Infinity datasoft/data"
Crome_driver = "c://chromedriver.exe"

Google_map.scrap_map(Google_url,Data_csv,Crome_driver)