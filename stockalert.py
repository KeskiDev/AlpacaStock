import alpaca_trade_api as tradeapi
import datetime
import time
import json
import requests

api = tradeapi.REST('api key','secret key', base_url='https://api.alpaca.markets')
discord_webhook_url = "discord url here"

companiesLastQuote = {}

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
        currentBid = lastQuote.bidprice
        
        companyInList = companiesLastQuote.get(companySymbol)
        
        if companyInList:
            previousQuote = companiesLastQuote[companySymbol]

            if(currentBid > previousQuote):

                msg = "SELL? - {} - ${} - up (+{})"
                difference = currentBid - previousQuote
                theDifference = format(difference, '.2f')

                results.append(msg.format(companySymbol, currentBid, theDifference))
                #print(msg.format(companySymbol, currentBid, difference))
                
                Message = {
                    "content": msg.format(companySymbol, currentBid, theDifference)
                }
                requests.post(discord_webhook_url, data=Message)
                companiesLastQuote[companySymbol] = currentBid
            elif(currentBid < previousQuote):
                msg = "BUY? - {} - ${} - down (-{})"
                difference = previousQuote - currentBid
                theDifference = format(difference, '.2f')
                
                results.append(msg.format(companySymbol, currentBid, theDifference))

                Message = {
                    "content": msg.format(companySymbol, currentBid, theDifference)
                }
                requests.post(discord_webhook_url, data=Message)

                companiesLastQuote[companySymbol] = currentBid
            else:
                companiesLastQuote[companySymbol] = currentBid
        else:
            companiesLastQuote[companySymbol] = currentBid
    
    

#def saveToFile(data):
    #save the result list to a file

def runAnalysis():
    count = 0
    while True:
        market = api.get_clock()
        print(count)
        count += 1
        if market.is_open:
            stockChecker()
            time.sleep(1800)
            #900 seconds = 15 minutes
            #1800 seconds = 30 minutes
            #3600 seconds = 1 hour
        else:
            #wait an hour before checking again
            #figure out what api is using for time and then just make next check when the market opens
            time.sleep(1800)

    #get the aggs for a company for a specified time frame --
    #don't know what I'll use this for quite yet
    #apple = api.polygon.historic_agg_v2('AAPL',1, 'day', _from='2020-11-01', to='2020-11-17')

    # for bite in apple:
    #     print(bite.high)




#run the program
runAnalysis()