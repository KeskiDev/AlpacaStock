import alpaca_trade_api as tradeapi

api = tradeapi.REST('api key goes here','secret key goes here', base_url='https://api.alpaca.markets')
account = api.get_account()
watchListId = 0
companiesLastQuote = {}

#get all my watchlists
watchLists = api.get_watchlists()
print(watchLists)
#only have one so use that one
watchListId = watchLists[0].id

#get my primary watchList
watchListCompanies = api.get_watchlist(watchListId)


for company in watchListCompanies.assets:
    companySymbol = company['symbol']
    lastQuote = api.get_last_quote(companySymbol)
    currentBid = lastQuote.bidprice
    #print(lastQuote.bidprice)
    companyInList = companiesLastQuote.get(companySymbol)
    
    if companyInList:
        previousQuote = companiesLastQuote[companySymbol]
        if(currentBid > previousQuote):
            print(f"now might be a good time to sell: {companySymbol} @ {currentBid} price before: {previousQuote}")
            companiesLastQuote[companySymbol] = currentBid
        elif(currentBid < previousQuote):
            print(f"now might be a good time to buy: {companySymbol} @ {currentBid} price before: {previousQuote}")
        else:
            companiesLastQuote[companySymbol] = currentBid
    else:
        companiesLastQuote[companySymbol] = currentBid

    # if(len(companiesLastQuote) > 0):
    #     previousQuote = companiesLastQuote[companySymbol]
    #     print(previousQuote)
    # else:
    #     companiesLastQuote[companySymbol] = lastQuote.bidprice

print(companiesLastQuote)


#get the aggs for a company for a specified time frame --
#don't know what I'll use this for quite yet
#apple = api.polygon.historic_agg_v2('AAPL',1, 'day', _from='2020-11-01', to='2020-11-17')

# for bite in apple:
#     print(bite.high)




#every 15 minutes go through the list of stocks in watch list (get_last_quote)

#get the previous last quote and compare the price

#if price difference is ___x____ notify me through discord

#save the most recent last quote price



#eventually make it so multiple people could use this
