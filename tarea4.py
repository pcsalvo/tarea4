import requests
import xml.etree.ElementTree as ET

from time import sleep

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class LoadData():

    def __init__(self):
        self.CHL = []
        self.MNE = []
        self.ATG = []
        self.VUT = []
        self.MRT = []
        self.DZA = []
        self.charge_data()
    
    def charge_data(self):
        self.chl = self.load_data("CHL")
        self.mne = self.load_data("MNE")
        self.atg = self.load_data("ATG")
        self.vut = self.load_data("VUT")
        self.mrt = self.load_data("MRT")
        self.dza = self.load_data("DZA")
        self.download_data("CHL")
        self.download_data("MNE")
        self.download_data("ATG")
        self.download_data("VUT")
        self.download_data("MRT")
        self.download_data("DZA")
    
    def load_data(self, model):
        data = requests.get("http://tarea-4.2021-1.tallerdeintegracion.cl/gho_{}.xml".format(model))
        data = data.text
        return ET.fromstring(data)

    def download_data(self, model):
        if model == "CHL":
            use = self.chl
        elif model == "MNE":
            use = self.mne
        elif model == "ATG":
            use = self.atg
        elif model == "VUT":
            use = self.vut
        elif model == "MRT":
            use = self.mrt
        elif model == "DZA":
            use = self.dza

        for item in use.findall("./Fact"):
            info = {}
            info['GHO'] = "-"
            info['COUNTRY'] = "-"
            info['SEX'] = "-"
            info['YEAR'] = "-"
            info['GHECAUSES'] = "-"
            info['AGEGROUP'] = "-"
            info['Display'] = "-"
            info['Numeric'] = "-"
            info['High'] = "-"
            info['Low'] = "-"

            for element in item.findall("./GHO"):
                if element.text:
                    info['GHO'] = element.text

            for element in item.findall("./COUNTRY"):
                if element.text:
                    info['COUNTRY'] = element.text

            for element in item.findall("./SEX"):
                if element.text:
                    info['SEX'] = element.text

            for element in item.findall("./YEAR"):
                if element.text:
                    info['YEAR'] = element.text

            for element in item.findall("./GHECAUSES"):
                if element.text:
                    info['GHECAUSES'] = element.text

            for element in item.findall("./AGEGROUP"):
                if element.text:
                    info['AGEGROUP'] = element.text

            for element in item.findall("./Display"):
                if element.text:
                    info['Display'] = element.text

            for element in item.findall("./Numeric"):
                if element.text:
                    info['Numeric'] = element.text
                    
            for element in item.findall("./High"):
                if element.text:
                    info['High'] = element.text

            for element in item.findall("./Low"):
                if element.text:
                    info['Low'] = element.text
        
            if model == "CHL":
                self.CHL.append(info)
            elif model == "MNE":
                self.MNE.append(info)
            elif model == "ATG":
                self.ATG.append(info)
            elif model == "VUT":
                self.VUT.append(info)
            elif model == "MRT":
                self.MRT.append(info)
            elif model == "DZA":
                self.DZA.append(info)
    
    def print_data(self):
        return {
            "CHL": self.CHL,
            "MNE": self.MNE,
            "ATG": self.ATG,
            "VUT": self.VUT,
            "MRT": self.MRT,
            "DZA": self.DZA
        }


class PublishSheet():

    def __init__(self):
        self.data = None
        scope = [
            "https://www.googleapis.com/auth/spreadsheets", 
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
            ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("taller-tarea-4-316813-8f4da57c3e60.json", scope)
        client = gspread.authorize(creds)
        self.my_work = client.open("Tarea 4")

        self.reset_data("Chile")
        self.reset_data("Montenegro")
        self.reset_data("Antigua y Barbuda")
        self.reset_data("Vanuatu")
        self.reset_data("Mauritania")
        self.reset_data("Argelia")

        self.chl = self.my_work.worksheet("Chile")
        self.mne = self.my_work.worksheet("Montenegro")
        self.atg = self.my_work.worksheet("Antigua y Barbuda")
        self.vut = self.my_work.worksheet("Vanuatu")
        self.mrt = self.my_work.worksheet("Mauritania")
        self.dza = self.my_work.worksheet("Argelia")

        self.prepare()
    
    def prepare(self):
        self.load_data()
        sleep(10)
        self.fill_sheets(self.chl, self.data["CHL"])
        sleep(10)
        self.fill_sheets(self.mne, self.data["MNE"])
        sleep(10)
        self.fill_sheets(self.atg, self.data["ATG"])
        sleep(10)
        self.fill_sheets(self.vut, self.data["VUT"])
        sleep(10)
        self.fill_sheets(self.mrt, self.data["MRT"])
        sleep(10)
        self.fill_sheets(self.dza, self.data["DZA"])
        sleep(10)

    def reset_data(self, country):
        sheet1 = self.my_work.worksheet(country)
        self.my_work.del_worksheet(sheet1)
        self.my_work.add_worksheet(title=country, rows="1000", cols="20")

    def fill_sheets(self, sheet, data):
        total_info = []
        line1 = ['GHO','COUNTRY', 'SEX', 'YEAR', 
        'GHECAUSES', 'AGEGROUP', 'Display', 'Numeric', 'Low', 'High']
        total_info.append(line1)
        line = [
            [data[i]['GHO'], 
            data[i]['COUNTRY'], 
            data[i]['SEX'],
            data[i]['YEAR'],
            data[i]['GHECAUSES'],
            data[i]['AGEGROUP'],
            data[i]['Display'],
            data[i]['Numeric'],
            data[i]['Low'],
            data[i]['High']] for i in range(len(data))
        ]
        total_info += line

        sheet.update("A1:J{}".format(str(len(total_info))), total_info)

    def load_data(self):
        my_data = LoadData()
        self.data = my_data.print_data()


if __name__ == "__main__":
    PublishSheet()