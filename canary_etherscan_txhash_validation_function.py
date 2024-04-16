
# This is the CBV for the Investigation Remodel function for Canary Application created by Seanchester Cro Reyes Rosario

class InvestigationRemodel(UpdateView):# CBV Generic Pocket Update
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    model = Investigation
    

    template_name = "investigations/detail.html"
    fields = ['title','description', 'if_NFT','transaction_hash']
    proxy = model.objects.all()


    def get_context_data(self, **kwargs):
        context = super(InvestigationRemodel, self).get_context_data(**kwargs)
        investigations = Investigation.objects.filter(id=self.kwargs['pk'])
        qs = Investigation.objects.filter(investigation_owner=self.request.user)
        current_investigation_transaction_hash = investigations.first().transaction_hash
        etherscanapiykey = ETHERSCANAPIKEY

        # (Transaction Receipt Status) Status 1 = Success  / status 0 = Failed / status NULL = Not a real transaction
        transaction_response = requests.get('https://api.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash='+current_investigation_transaction_hash+'&apikey='+etherscanapiykey)
        transaction_validation_data = transaction_response.json()
        transaction_validation_status = transaction_validation_data['result'] 
        # print(transaction_validation_status['status'])
        
        # (Contract Execution Status) isError0 = successful transaction / isError1 = failed transaction
        execution_transaction_response = requests.get('https://api.etherscan.io/api?module=transaction&action=getstatus&txhash='+current_investigation_transaction_hash+'&apikey='+etherscanapiykey)
        execution_transaction_validation_data = execution_transaction_response.json()

        # if it is a failed transaction, the error message is stored here
        execution_transaction_validation_data_error_description = execution_transaction_validation_data['result']
        
        # Current ETH PRICE
        last_eth_price_response = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice&apikey='+etherscanapiykey)
        last_eth_price_data = last_eth_price_response.json()
        last_eth_price_data_result = last_eth_price_data['result'] 

        # Total ETH Node Count
        total_node_count_response = requests.get('https://api.etherscan.io/api?module=stats&action=nodecount&apikey='+etherscanapiykey)
        total_node_count_response_data = total_node_count_response.json()
        total_node_count_response_data_result = total_node_count_response_data['result']

        if transaction_validation_status['status'] == "0":
            transaction_hash_input_color_code = '#FF9191'
            transaction_hash_input_message = " This is a Failed but Valid Ethereum transaction hash"
        elif transaction_validation_status['status'] == "1":
            transaction_hash_input_color_code = '#98FF91'
            transaction_hash_input_message = " This is a Successful and Valid Ethereum transaction hash"
        else:
            transaction_hash_input_color_code = '#BEBEBE'
            transaction_hash_input_message = " This is a not a valid Ethereum transaction hash or is a pre Byzantium Fork transaction "
        context.update({
            'failed_txhash_error_description':execution_transaction_validation_data_error_description['errDescription'],
            'transaction_hash_input_message':transaction_hash_input_message,
            'transaction_hash_input_color_code':transaction_hash_input_color_code,
            'etherscanapiykey':etherscanapiykey,
            'investigations_txhash':current_investigation_transaction_hash,
            'investigations':investigations,
            'qs':qs,
            'investigation_owner_id': investigations.first().investigation_owner.id,
            'investigation_id': investigations.first().id,
          
          })
        return context


    def form_valid(self, form):
        # print the clean form to confirm
  
        return super().form_valid(form)
    
    def get_success_url(self):
       investigations = Investigation.objects.filter(id=self.kwargs['pk'])
       investigationsone = investigations.first().id
       messages.success(self.request, "Investigation Updated")

       return "/investigations/" + str(investigationsone)

