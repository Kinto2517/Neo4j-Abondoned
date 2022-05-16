# -*- coding: utf-8 -*-
import os
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from ParsingUniverse import db
from ParsingUniverse.models import Sorgu, PDFFile


def dersadiBul(filename):
    s1 = convert(filename, pages=[1, 1])
    if s1.find("ARAŞTIRMA PROBLEMLERİ") != -1:
        dersadi = s1[s1.find("ARAŞTIRMA PROBLEMLERİ"):s1.find("ARAŞTIRMA PROBLEMLERİ") + 23]
        return dersadi
    elif s1.find("BİTİRME PROJESİ") != -1:
        dersadi = s1[s1.find("BİTİRME PROJESİ"):s1.find("BİTİRME PROJESİ") + 15]
        return dersadi
    elif s1.find("LİSANS TEZİ") != -1:
        dersadi = s1[s1.find("LİSANS TEZİ"):s1.find("LİSANS TEZİ") + 11]
        return dersadi
    elif s1.find("YÜKSEK LİSANS TEZİ") != -1:
        dersadi = s1[s1.find("YÜKSEK LİSANS TEZİ"):s1.find("YÜKSEK LİSANS TEZİ") + 11]
        return dersadi
    else:
        return "Ders bulunamadi"


def isimBul(filename):
    s1 = convert(filename, pages=[1, 1])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()
    firstNames = []
    lastNames = []
    for i in range(10, 14, 1):
        if Lines[i][0] != -1:
            try:
                if Lines[i][1].isupper() and Lines[i][2].isupper():
                    Lines[i].strip()
                    arr = Lines[i].split()
                    if len(arr) == 3:
                        firstNames.append(arr[0])

                        lastNames.append(arr[-1])
                    elif len(arr) == 2:
                        firstNames.append(arr[0])
                        lastNames.append(arr[-1])
            except:
                print("")

    a = ", ".join(firstNames)

    return a


def soyisimBul(filename):
    s1 = convert(filename, pages=[1, 1])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()
    firstNames = []
    lastNames = []
    for i in range(10, 19, 1):
        try:
            if Lines[i][1].isupper() and Lines[i][2].isupper():
                Lines[i].strip()
                arr = Lines[i].split()
                if len(arr) == 3:
                    firstNames.append(arr[0])
                    firstNames.append(arr[1])
                    lastNames.append(arr[-1])
                elif len(arr) == 2:
                    firstNames.append(arr[0])
                    lastNames.append(arr[-1])
        except:
            print()
    a = ", ".join(lastNames)

    return a


def ogrNoBul(filename):
    s1 = convert(filename, pages=[2, 3, 4])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()

    ogrNo = []
    ogrTuru = []
    count = 0

    for line in Lines:
        count += 1
        line.strip()
        if line.find("Öğrenci No:") != -1:
            ogrNo.append(line[12:21])
            if line[17] == '1':
                ogrTuru.append("1. Öğretim")
            else:
                ogrTuru.append("2. Öğretim")

    a = ", ".join(ogrNo)

    return a


def ogrTuruBul(filename):
    s1 = convert(filename, pages=[2, 3, 4])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()

    ogrNo = []
    ogrTuru = []
    count = 0

    for line in Lines:
        count += 1
        line.strip()
        if line.find("Öğrenci No:") != -1:
            ogrNo.append(line[12:21])
            if line[17] == '1':
                ogrTuru.append("1. Öğretim")
            else:
                ogrTuru.append("2. Öğretim")

    a = ", ".join(ogrTuru)

    return a


def teslimBul(filename):
    s1 = convert(filename, pages=[1, 1])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()
        count = 0

        for line in Lines:
            count += 1
            line.strip()
            if line.find("Tezin Savunulduğu Tarih:") != -1:
                if line[28:30] == '09' or line[28:30] == '10' or line[28:30] == '11' or line[28:30] == '12' or line[
                                                                                                               28:30] == '01':
                    return "Güz"
                else:
                    return "Bahar"


def anahtarKelime(filename):
    s1 = convert(filename, pages=[8, 9, 10])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()
        c = 0
        i = -1
        carr = []
        for line in Lines:
            i = i + 1
            if line.find("Anahtar  kelimeler:") != -1 or line.find("Anahtar  Kelimeler:") != -1 or line.find(
                    "Anahtar Kelimeler:") != -1 or line.find("Anahtar kelimeler:") != -1:
                c = i

        for a in range(c, len(Lines) - 1):
            for b in range(0, len(Lines[a])):
                if Lines[a][b] == '.':
                    d = a
                    e = b

        for a in range(c, len(Lines) - 1):
            for b in range(0, len(Lines[a])):
                if Lines[a][b] != Lines[d][e]:
                    carr.append(Lines[a][b])
                else:
                    a_string = "".join(carr[19:])
                    values = ''.join(str(v) for v in a_string)
                    return values


def baslikBul(filename):
    s1 = convert(filename, pages=[1, 1])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()

        baslik = ""
        if filename == "a.pdf":
            for a in range(0, len(Lines)):
                if Lines[a].find("ARAŞTIRMA PROBLEMLERİ") != -1 or Lines[a].find("BİTİRME PROJESİ") != -1 or Lines[
                    a].find("YÜKSEK LİSANS TEZİ") != -1 or Lines[a].find("LİSANS TEZİ") != -1:
                    return Lines[a - 2]
        else:
            for a in range(0, len(Lines)):
                if Lines[a].find("ARAŞTIRMA PROBLEMLERİ") != -1 or Lines[a].find("BİTİRME PROJESİ") != -1 or Lines[
                    a].find("YÜKSEK LİSANS TEZİ") != -1 or Lines[a].find("LİSANS TEZİ") != -1:
                    return Lines[a + 2]


def juriBul(filename):
    s1 = convert(filename, pages=[1, 1])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()
        hepsi = []
        danisman = []
        juri = []
        for a in range(0, len(Lines)):
            if Lines[a].find("Doç") != -1 or Lines[a].find("Prof") != -1 or Lines[a].find("Dr") != -1:
                Lines[a].strip()
                hepsi.append(Lines[a].rstrip())
        danisman.append(hepsi[0])
        juri.append(hepsi[1])
        values = ''.join(str(v) for v in juri)
        juri.append(', ')
        juri.append(hepsi[2])
        values = ''.join(str(v) for v in juri)

        return values


def danismanBul(filename):
    s1 = convert(filename, pages=[1, 1])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()
        hepsi = []
        danisman = []
        juri = []
        for a in range(0, len(Lines)):
            if Lines[a].find("Doç") != -1 or Lines[a].find("Prof") != -1 or Lines[a].find("Dr") != -1:
                hepsi.append(Lines[a])
        danisman.append(hepsi[0])
        juri.append(hepsi[1:3])
        values = ''.join(str(v) for v in danisman)

        return values


def ozetBul(filename):
    s1 = convert(filename, pages=[9, 10, 11])
    with open('deneme1.txt', 'w', encoding="utf-8") as file:
        file.write(s1)

    with open('deneme1.txt', 'r', encoding="utf-8") as file:
        Lines = file.readlines()
        hepsi = []
        b = 0
        c = 0
        for a in range(0, len(Lines)):
            if Lines[a].find("ÖZET") != -1:
                b = a
            elif Lines[a].find("Anahtar  kelimeler:") != -1 or Lines[a].find("Anahtar  Kelimeler:") != -1 or Lines[
                a].find("Anahtar Kelimeler:") != -1 or Lines[a].find("Anahtar kelimeler:") != -1:
                c = a

        for d in range(b + 1, c - 1):
            hepsi.append(Lines[d])
    hepsi1 = "".join(hepsi)
    return hepsi1


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


def sorguBaslat():
    for filename in os.listdir(r"C:\Users\ersin\Desktop\flaskProject2\ParsingUniverse\static\yuklemeler"):
        if filename.endswith(".pdf"):
            pdfid = PDFFile.query.filter_by(name=filename).first()
            print(filename)
            yenid = Sorgu(ad=isimBul(filename), soyad=soyisimBul(filename),
                      ogrNo=ogrNoBul(filename), ogrTur=ogrTuruBul(filename),
                      dersAdi=dersadiBul(filename), donem=teslimBul(filename),
                      baslik=baslikBul(filename), keyword=anahtarKelime(filename),
                      danisman=danismanBul(filename), juri=juriBul(filename),
                      ozet=ozetBul(filename), pdf_id=pdfid.id)

            db.session.add(yenid)
            db.session.commit()
        else:
            continue

sorguBaslat()
