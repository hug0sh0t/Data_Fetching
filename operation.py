

class MarketData():

    def index(request,  *args, **kwargs): #   CRYPTO DATA with 10 seconds interval API request for data refresh
        if not request.user.is_authenticated:
            raise Http404

        # FEAR AND GREED INTEGRATION
        fng_response = requests.get('https://api.alternative.me/fng/')
        fng_data = fng_response.json()

        # COINMARKETCAP SPOT PRICE API

        global_latest_url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
        latest_cryptoquote_url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'f25522e3-f957-44bf-882c-12f70f33d361',
        }

        session = Session()
        session.headers.update(headers)

        try:
            # Latest Global APIendpoint
            response = session.get(global_latest_url, params={'convert':'USD'})
            cmc_latest_global_data = response.json()

            # Price Quote Latest APIendpoint
            #BTC
            btc_quote_response = session.get(latest_cryptoquote_url, params={'symbol':'BTC','convert':'USD'})
            btc_cmc_latest_quote = btc_quote_response.json()

            #ETH
            eth_quote_response = session.get(latest_cryptoquote_url, params={'symbol':'ETH','convert':'USD'})
            eth_cmc_latest_quote = eth_quote_response.json()

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        context={
            
            "cmc": cmc_latest_global_data,
            "btc_cmcquote": btc_cmc_latest_quote,
            "eth_cmcquote": eth_cmc_latest_quote,
            "fng_data": fng_data,
        }    

        return render(request, "pages/marketdata.html", context, status=200)
