import os
import pandas as pd


current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir,os.pardir)) #'C:\\Users\\Administrateur\\PycharmProjects\\mfinance'

package_dir = os.path.dirname(os.path.abspath(__file__))
#csv_path = os.path.join(package_dir, "ISIN_sectors_ma.csv")
available_names = ['AFMA', 'AFRIC INDUSTRIES SA', 'AFRIQUIA GAZ', 'AGMA', 'AKDITAL', 'ALLIANCES', 'ALUMINIUM DU MAROC', 'ARADEI CAPITAL', 'ATLANTASANAD', 'ATTIJARIWAFA BANK', 'AUTO HALL', 'AUTO NEJMA', 'BALIMA', 'BANK OF AFRICA', 'BCP', 'BMCI', 'CARTIER SAADA', 'CDM', 'CIH', 'CIMENTS DU MAROC', 'COLORADO', 'COSUMAR', 'CTM', 'DARI COUSPATE', 'DELATTRE LEVIVIER MAROC', 'DELTA HOLDING', 'DIAC SALAF', 'DISTY TECHNOLOGIES', 'DISWAY', 'DOUJA PROM ADDOHA', 'ENNAKL', 'EQDOM', 'FENIE BROSSETTE', 'HPS', 'IB MAROC.COM', 'IMMORENTE INVEST', 'INVOLYS', 'ITISSALAT AL-MAGHRIB', 'JET CONTRACTORS', 'LABEL VIE', 'LAFARGEHOLCIM MAR', 'LESIEUR CRISTAL', 'M2M Group', 'MAGHREB OXYGENE', 'MAGHREBAIL', 'MANAGEM', 'MAROC LEASING', 'MED PAPER', 'MICRODATA', 'MINIERE TOUISSIT', 'MUTANDIS SCA', 'OULMES', 'PROMOPHARM S.A.', 'REALISATIONS MECANIQUES', 'REBAB COMPANY', 'RES DAR SAADA', 'RISMA', 'S.M MONETIQUE', 'SALAFIN', 'SAMIR', 'SANLAM MAROC', 'SMI', 'SNEP', 'SOCIETE DES BOISSONS DU MAROC', 'SODEP-Marsa Maroc', 'SONASID', 'SOTHEMA', 'STOKVIS NORD AFRIQUE', 'STROC INDUSTRIE', 'TAQA MOROCCO', 'TGCC S.A', 'TIMAR', 'TOTALENERGIES MARKETING MAROC', 'UNIMER']

# List of available company names
#available_names = list(pd.read_csv(csv_path)["Instrument"])
"""
def download(name, start_date, end_date, period):
    # Check if the name is valid
    if name not in available_names:
        print("Invalid company name.")
        return

    # Check if the start date is prior to the oldest available date
    oldest_date = pd.Timestamp('2018-05-16')
    if pd.Timestamp(start_date) < oldest_date:
        print("Start date cannot be prior to 2018-05-16.")
        return

    # Load data from CSV
    filename = f"{name}.csv"
    try:
        data = pd.read_csv(os.path.join(current_dir,"data_stocks",filename))

    except FileNotFoundError:
        print(f"Data not found for {name}.")
        return

    # Filter data based on start and end dates
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]


    # Filter data based on period (currently only supports "1d")
    if period != "1d":
        print("Invalid period. Only '1d' is supported.")
        return

    # Print or return the resulting data
    return (data)  # Modify as per your requirement"""


def data(stock_name,start_date,end_date,period):
    if stock_name not in available_names:
        print("Invalid company name.")
        return
    if " " in stock_name:
        stock_name = stock_name.replace(" ","%20")
    stock_data = pd.read_csv(
        "https://raw.githubusercontent.com/alitalbi/ma_fi/master/data_stocks/" + stock_name + ".csv")
    # stock_data.set_index("Timestamp",inplace=True)
    stock_data = stock_data[(stock_data['Timestamp'] >= start_date) & (stock_data['Timestamp'] <= end_date)]

    return stock_data
