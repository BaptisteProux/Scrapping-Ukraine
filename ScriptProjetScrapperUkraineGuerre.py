import subprocess
import os


extension=".py"



def menu():
    print("Menu du projet OSINT guerre en Ukraine: Selectionner le script souhaité:")
    print("1: CsvEconomieStatistique.py")
    print("2: ExcelSupportTrackerKielInstitute.py")
    print("3: JsonCivilianLosesBellingcatAnalysis.py")
    print("4: MilitaryUnit.py")
    print("5: scrapperLiveuamapAllDays.py")
    print("6: ScrapperOryx.py")
    print("7: ScrapperTwitterUkraine.py")
    print("8: ScrapperWarSpotting.py")
    print("9: scrapperWikipedia.py")
    print("10: scrapperYoutube.py")
    print("11: scrapperPDFLocal.py")
    print("12: MapEventUkraine.py")
    print("13. Exit")
    print("PS: Vous pouvez aussi lancer ces scripts directement/manuellement")

def launcher(choice):
    if choice == 1:
        subprocess.run(["python", "CsvEconomieStatistique"+extension])
    elif choice == 2:
        subprocess.run(["python", "ExcelSupportTrackerKielInstitute"+extension])
    elif choice == 3:
        subprocess.run(["python", "JsonCivilianLosesBellingcatAnalysis"+extension])
    elif choice == 4:
        subprocess.run(["python", "MilitaryUnit"+extension])
    elif choice == 5:
        subprocess.run(["python", "scrapperLiveuamapAllDays"+extension])
    elif choice == 6:
        subprocess.run(["python", "ScrapperOryx"+extension])
    elif choice == 7:
        subprocess.run(["python", "ScrapperTwitterUkraine"+extension])
    elif choice == 8:
        subprocess.run(["python", "ScrapperWarSpotting"+extension])
    elif choice == 9:
        subprocess.run(["python", "scrapperWikipedia"+extension])
    elif choice == 10:
        subprocess.run(["python", "scrapperYoutube"+extension])
    elif choice == 11:
        subprocess.run(["python", "scrapperPDFLocal"+extension])
    elif choice == 12:
        subprocess.run(["python", "MapEventUkraine"+extension])
    elif choice == 13:
        exit()
    else:
        print("Choix invalide")

while True:
    menu()
    choice = int(input("Enter your selection: "))
    launcher(choice)