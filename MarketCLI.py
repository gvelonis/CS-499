##!/usr/bin/python3

from lib.MarketDbIfc import MarketDbIfc
from pprint import pprint

# MAIN
if __name__ == '__main__':
    # initialize MongoIfc instance
    marketdb = MarketDbIfc('MarketCLI', 'MarketCLI')

    action = ""
    # main menu loop
    while action != "q":

        # print menu
        print("\nWhat would you like to do?\n")
        print("i - Insert stock from file")
        print("pv - Print volume of given Ticker")
        print("u - Update volume of given Ticker")
        print("d - Delete data for given Ticker")
        print("hilo - Find the number of stocks with a 50-Day Simple moving average between given high and low values")
        print("ind - Print list of companies in given industry")
        print("sec - Print list of total outstanding shares for all companies in a given sector, grouped by industry")
        print("q - Quit")

        action = input("\nEnter choice: ")

        if action == "i":
            if marketdb.import_stock("data/testStock.json"):
                print("Import successful.\n")
            else:
                print("Import failed.\n")

        elif action == "pv":
            ticker = input("Enter ticker to read volume of: ")
            for doc in marketdb.read_volume(ticker):
                pprint(doc)

        elif action == "u":
            ticker = input("Enter Ticker to update: ")
            volume = input("Enter new value for Volume ")
            if marketdb.update_volume(ticker, volume):
                print("Update successful.\n")
            else:
                print("Update failed.\n")

        elif action == "d":
            ticker = input("Enter ticker to delete: ")
            if marketdb.delete_stock(ticker):
                print("Ticker deleted successfully\n")
            else:
                print("Ticker deletion failed\n")

        elif action == "hilo":
            low = float(input("Enter low 50-day simple moving average value: "))
            high = float(input("Enter high 50-day simple moving average value: "))
            print(marketdb.read_hilo(high, low))

        elif action == "ind":
            industry = input("Enter Industry to search for: ")
            for doc in marketdb.read_industry(industry):
                pprint(doc)

        elif action == "sec":
            sector = input("Enter Sector to query: ")
            for doc in marketdb.read_sectors(sector):
                pprint(doc)

        elif action == "q":
            break

        else:
            print("Invalid input, try again")

    print("Thank you, Come again")
