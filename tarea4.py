import requests
import xml.etree.ElementTree as ET


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
            info['GHO'] = None
            info['COUNTRY'] = None
            info['SEX'] = None
            info['YEAR'] = None
            info['GHECAUSES'] = None
            info['AGEGROUP'] = None
            info['Display'] = None
            info['Numeric'] = None
            info['High'] = None
            info['Low'] = None

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


if __name__ == "__main__":
    a = LoadData()
    a.print_data()
