from bs4 import BeautifulSoup
import requests

def ekstrak():
    try:
        content = requests.get("https://www.bmkg.go.id")
    except Exception :
        return None
    if content.status_code == 200 :
        soup = BeautifulSoup(content.text, "html.parser")

        result = soup.find("span", {"class" : "waktu"})
        result = result.text.split(", ")
        waktu = result[1]
        tanggal = result[0]

        result = soup.find("div", {"class" : "col-md-6 col-xs-6 gempabumi-detail no-padding"})
        result = result.findChildren("li")

        i = 0
        magnitudo = None
        kedalaman = None
        lokasi = None
        dirasakan = None

        for res in result :
            if i == 1 :
                magnitudo = res.text
            elif i == 2 :
                kedalaman = res.text
            elif i == 3 :
                koordinat = res.text.split(" - ")
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4 :
                lokasi = res.text
            elif i == 5 :
                dirasakan = res.text
            i = i + 1


        hasil = dict()
        hasil["tanggal"] = tanggal
        hasil["waktu"] = waktu
        hasil["magnitudo"] = magnitudo
        hasil["kedalaman"] = kedalaman
        hasil["koordinat"] = {"ls":ls,"bt":bt}
        hasil["lokasi"] = lokasi
        hasil["dirasakan"] = dirasakan
        return hasil
    else :
        return None


def showdata(result) :
    if result is None :
        print("Tidak ada data Gempa")
        return
    print(f"Tanggal = {result['tanggal']}")
    print(f"Waktu = {result['waktu']}")
    print(f"magnitudo = {result['magnitudo']}")
    print(f"kedalaman = {result['kedalaman']}")
    print(f"koordinat = LS = {result['koordinat'] ['ls']},BT= {result['koordinat']['bt']}")
    print(f"lokasi = {result['lokasi']}")
    print(f"dirasakan = {result['dirasakan']}")





if __name__ == "__main__":
    print("Latest earthquake information")
    result = ekstrak()
    showdata(result)
