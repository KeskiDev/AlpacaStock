import alpaca_trade_api as tradeapi
import time
import json
import requests
import datetime
from datetime import timedelta
from pytz import timezone

api = tradeapi.REST('api key','secret key', base_url='https://api.alpaca.markets')
discord_webhook_url = "discord url here"

companiesLastQuote = {}
companiesOpeningPrices = {}
#add the high price for the week

def stockChecker():
    #account = api.get_account()
    watchListId = 0
    results = []
    #get all my watchlists
    watchLists = api.get_watchlists()
    #print(watchLists)
    #only have one so use that one
    watchListId = watchLists[0].id

    #get my primary watchList
    watchListCompanies = api.get_watchlist(watchListId)

    for company in watchListCompanies.assets:
        companySymbol = company['symbol']
        lastQuote = api.get_last_quote(companySymbol)
        #todo get the barset
        #get_barset(symbol) should give the opening price, top price, close price etc

        currentPrice = lastQuote.askprice
        
        companyInList = companiesLastQuote.get(companySymbol)

        if companiesOpeningPrices.get(companySymbol) is None:
            companyBar = api.get_barset(companySymbol, 'day', 1)
            companiesOpeningPrices[companySymbol] = companyBar[companySymbol][0].o

        companyOpeningPrice = companiesOpeningPrices[companySymbol]
        
        if companyInList:
            #previousQuote = companiesLastQuote[companySymbol]
            #dayChange = currentPrice - companyOpeningPrice

            daychange = 23.80-23.85
            

            print(daychange)


            # if(currentPrice > previousQuote):

            #     msg = "SELL? - {} - ${} - up (+{})"
            #     difference = currentPrice - previousQuote
            #     theDifference = format(difference, '.2f')

            #     results.append(msg.format(companySymbol, currentPrice, theDifference))
            #     #print(msg.format(companySymbol, currentBid, difference))
                
            #     Message = {
            #         "content": msg.format(companySymbol, currentPrice, theDifference)
            #     }
            #     requests.post(discord_webhook_url, data=Message)
            #     companiesLastQuote[companySymbol] = currentPrice
            # elif(currentPrice < previousQuote):
            #     msg = "BUY? - {} - ${} - down (-{})"
            #     difference = previousQuote - currentPrice
            #     theDifference = format(difference, '.2f')
                
            #     results.append(msg.format(companySymbol, currentPrice, theDifference))

            #     Message = {
            #         "content": msg.format(companySymbol, currentPrice, theDifference)
            #     }
            #     requests.post(discord_webhook_url, data=Message)

            #     companiesLastQuote[companySymbol] = currentPrice
            # else:
            #     companiesLastQuote[companySymbol] = currentPrice
        else:
            companiesLastQuote[companySymbol] = currentPrice
    
    

#def saveToFile(data):
    #save the result list to a file

def runAnalysis():
    count = 0


    apple = api.get_last_quote('AAPL')

    appleBarset = api.get_barset('AAPL', 'day', 1)

    daychange = apple.askprice - appleBarset['AAPL'][0].o

    print(f"ask = {apple.askprice} : opening = {appleBarset['AAPL'][0].o} :: day change {daychange}")
            
    if abs(daychange) > 1.00:
        print("more than $1 change")
    else:
        print("you didn't see anything")

    # while True:
    #     market = api.get_clock()
    #     print(count)
    #     count += 1
    #     if market.is_open:
    #         stockChecker()
    #         time.sleep(300)
    #         #900 seconds = 15 minutes
    #         #1800 seconds = 30 minutes
    #         #3600 seconds = 1 hour
    #     else:
    #         #wait an hour before checking again
    #         #check when the market opens
    #         secondsToNextOpen = market.next_open - market.timestamp
    #         print(f"{market.next_open} - in {secondsToNextOpen} seconds")


    #         time.sleep(secondsToNextOpen.total_seconds())


    #get the aggs for a company for a specified time frame --
    #don't know what I'll use this for quite yet
    #apple = api.polygon.historic_agg_v2('AAPL',1, 'day', _from='2020-11-01', to='2020-11-17')

    # for bite in apple:
    #     print(bite.high)




#run the program
runAnalysis()