import requests
import time
import json
import datetime as dt
import csv

def formatDate(date):
    date = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
    return date.strftime('%d-%m-%Y')

def getSalary(salary):
    if salary:
        if salary['from'] and salary['to']:
            return f"{salary['from']} - {salary['to']} {salary['currency']}"
        elif salary['from']:
            return f"{salary['from']} {salary['currency']}"
    return None

def getPage(keyword, page = 0, country_code = 40):    
    params = {
        'text': f'NAME:{keyword}', # Job title keyword
        'area': country_code, # Kazakhstan
        'page': page, 
        'per_page': 100
    }
    
    
    req = requests.get('https://api.hh.ru/vacancies', params)
    if req.status_code == 200:
        data = req.content.decode() # Decode for cyrillic symbols
        req.close()
        return data
    else:
        req.close()
        return None

def exploreVacancies(keyword, max_pages = 20, time_sleep = 0.5, country_code = 40):
    try:
        for page in range(0, max_pages):
            data = getPage(keyword, page, country_code)
            if data is None:
                break
            data = json.loads(data)
            for item in data['items']:
                print(f"""
                    Title: {item['name']}, 
                    Salary: {getSalary(item['salary'])}, 
                    City: {item['area']['name']}, 
                    Job: {item['employer']['name']}, 
                    Publish Date: {formatDate(item['published_at'])}, 
                    Requirements: {item['snippet']['requirement']}, 
                    Responsibilites: {item['snippet']['responsibility']}, 
                    Schedule: {item['schedule']},
                    Experience: {item['experience']['name']}, 
                    Employment: {item['employment']['name']}, 
                    URL: {item['alternate_url']}
                    """)
                print('====================')
            time.sleep(time_sleep)
    except Exception as e:
        print('Something went wrong! Error: ', e)

def exportAsCSV(keyword, max_pages = 20, time_sleep = 0.5, country_code = 40):
    try:
        with open(f'data/{keyword}.csv', mode='w+', encoding='utf-8', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'salary', 'city', 'job', 'publish_date', 'requirements', 'responsibilities', 'schedule', 'experience', 'employment', 'url'])
            for page in range(0, max_pages):
                data = getPage(keyword, page, country_code)
                if data is None:
                    break
                data = json.loads(data)
                for item in data['items']:
                    writer.writerow([item['name'], getSalary(item['salary']), item['area']['name'], item['employer']['name'], formatDate(item['published_at']), item['snippet']['requirement'], item['snippet']['responsibility'], item['schedule'], item['experience']['name'], item['employment']['name'], item['alternate_url']])
            time.sleep(time_sleep)
    except Exception as e:
        print('Something went wrong! Error: ', e)

def main():
    country_codes = {
        "UA": 5,
        "AZ": 9,
        "BY": 16,
        "GE": 28,
        "KZ": 40,
        "KG": 48,
        "UZ": 97,
        "RU": 113,
        "Other": 1001
    }
    print("Head Hunter Vacancies Explorer: ")
    print("----------")
    # Ukraine: UA
    # Azerbaijan: AZ
    # Belarus: BY
    # Georgia: GE
    # Kazakhstan: KZ
    # Kyrgyzstan: KG
    # Uzbekistan: UZ
    # Russia: RU
    # Other: NA
    country = input('Enter a country code (ex.: KZ): ')
    if country not in country_codes:
        print('Try Again!')
        exit()
    else:
        country_code = country_codes[country]
    keyword = input('Enter a job keyword: ')
    exploreVacancies(keyword, country_code)
    exportAsCSV(keyword, country_code)
    print('Done!')

if __name__ == '__main__':
    main()