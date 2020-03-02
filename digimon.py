from bs4 import BeautifulSoup
import requests

urldigi = 'http://digidb.io/digimon-list/'
datadigi = requests.get(urldigi)
soup = BeautifulSoup(datadigi.content, 'html.parser')
nameFields = soup.find_all('th')
# print(datasoupdigi)

col = []
for data in nameFields:
    col.append(data.text)
    # print(i, data.text)
col.insert(1, 'image')
# print([col])

datasoupcol = soup.find('tbody')
row = []
for data in datasoupcol:
    tampung = data.find_all('td')
    hasil = []
    for data2 in tampung: 
        hasil.append(data2.text.strip())
    row.append(hasil)
# print(row)

dataimgsoup = soup.find('tbody')
img = []
for i in dataimgsoup.find_all('img'):
    img.append(i['src'])
# print(img)

for i in range(len(img)):
    row[i].insert(1, img[i])
# print(row)

# Zip keys and Values
dictdigi = []
for i in row:
    dictdigi.append(dict(zip(col, i)))
# print(dictdigi)

# Tuple Zip keys and values
dictdigituple = []
for i in dictdigi:
    dictdigivalue = tuple(i.values())
    dictdigituple.append(dictdigivalue)


# Export to XLSX
import xlsxwriter

book = xlsxwriter.Workbook('D:/Purwadhika Code/contohdata/digi.xlsx')
sheet = book.add_worksheet('Digimon')

for i in range(len(col)):
    sheet.write(0, i, col[i])

for i in range(len(row)):
    for j in range(len(row[0])):
        sheet.write(i+1, j, row[i][j])
book.close()

# baris = 0
# for Id, Image, Digimon, Stage, Type, Attribute, Memory, Equip, HP, SP, Atk, Def, Int, Spd in row:
#     sheet.write(baris, 0, 'Id')
#     sheet.write(baris, 1, 'Image')
#     sheet.write(baris, 2, 'Digimon')
#     sheet.write(baris, 3, 'Stage')
#     sheet.write(baris, 4, 'Type')
#     sheet.write(baris, 5, 'Attribute')
#     sheet.write(baris, 6, 'Memory')
#     sheet.write(baris, 7, 'Equip')
#     sheet.write(baris, 8, 'HP')
#     sheet.write(baris, 9, 'SP')
#     sheet.write(baris, 10, 'Atk')
#     sheet.write(baris, 11, 'Def')
#     sheet.write(baris, 12, 'Int')
#     sheet.write(baris, 13, 'Spd')
# book.close()

# baris = 1
# for Id, Image, Digimon, Stage, Type, Attribute, Memory, Equip, HP, SP, Atk, Def, Int, Spd in row:
#     sheet.write(baris, 0, Id)
#     sheet.write(baris, 1, Image)
#     sheet.write(baris, 2, Digimon)
#     sheet.write(baris, 3, Stage)
#     sheet.write(baris, 4, Type)
#     sheet.write(baris, 5, Attribute)
#     sheet.write(baris, 6, Memory)
#     sheet.write(baris, 7, Equip)
#     sheet.write(baris, 8, HP)
#     sheet.write(baris, 9, SP)
#     sheet.write(baris, 10, Atk)
#     sheet.write(baris, 11, Def)
#     sheet.write(baris, 12, Int)
#     sheet.write(baris, 13, Spd)
#     baris+=1
# book.close()

# Export to CSV
import csv
with open('D:/Purwadhika Code/contohdata/digi.csv', 'w', newline='') as mycsv:
    writercsv = csv.DictWriter(mycsv, delimiter=',', fieldnames=[
        '#','image', 'Digimon', 'Stage', 'Type', 'Attribute', 
        'Memory', 'Equip Slots', 'HP', 'SP', 'Atk', 'Def', 'Int', 'Spd'])
    writercsv.writeheader()
    writercsv.writerows(dictdigi)

# Export to JSON
import json
with open('D:/Purwadhika Code/contohdata/digi.json', 'w') as wrjson:
    json.dump(dictdigi, wrjson)

# Export to MongoDB
import pymongo
# urldb = 'mongodb://localhost:27017'
# mongoku = pymongo.MongoClient(urldb)
# dbku = mongoku['Digimon']
# colku = dbku['Digimon']
# send = colku.insert_many(dictdigi)

# Export to MYSQL
import mysql.connector

dbku = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = '',
    database = 'digimon'
)
cursor = dbku.cursor()
querytabel = 'create table digimon(Id int not null auto_increment, Image varchar(100), Digimon text, Stage text, Type text, Attribute text, Memory int, Equip int, HP int, SP int, Atk int, Def int, Intelligence bigint, Spd int, primary key (Id))'
queryku = 'insert into digimon values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
cursor.executemany(queryku, row)
dbku.commit()

