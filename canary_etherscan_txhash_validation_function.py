
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

        # Status 1 = Success  / status 0 = Failed / status NULL = Not a real transaction
        transaction_response = requests.get('https://api.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash='+current_investigation_transaction_hash+'&apikey='+etherscanapiykey)
        transaction_validation_data = transaction_response.json()
        transaction_validation_status = transaction_validation_data['result'] 
        print(transaction_validation_status['status'])
        if transaction_validation_status['status'] == "0":
            transaction_hash_input_color_code = '#FF9191'
            transaction_hash_input_message = " This is a Failed but Valid Ethereum transaction hash"
        elif transaction_validation_status['status'] == "1":
            transaction_hash_input_color_code = '#98FF91'
            transaction_hash_input_message = " This is a Successful and Valid Ethereum transaction hash"
        else:
            transaction_hash_input_color_code = '#BEBEBE'
            transaction_hash_input_message = " This is a not a valid Ethereum transaction hash"
        context.update({
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

