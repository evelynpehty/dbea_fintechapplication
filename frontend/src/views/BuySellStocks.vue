<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>
  
    <div class="container-fluid">
      <div class="row" style="margin-top:80px">
        <h2 class="title">Buy or Sell Stocks</h2>
        <p class="title">Please fill in the required fields to buy or sell stocks</p>
      </div>
      <br>
  
      <div v-if="errors.length != 0">
        <div class="alert alert-danger alert-dismissible fade show mb-5" role="alert">
          <h4>Please check your inputs</h4>
          <ul>
            <li class="m-0" v-for="e in errors" :key="e">{{e}}</li>
          </ul>
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
      </div>
   
      <div class="card border-0 shadow p-3 mb-5 bg-white rounded">
        <div class="card-body">
          <form @submit.prevent v-on:submit="checkForm">

            <div class="row">
              <div class="col-6">
                <div class="mb-3">
                  <label for="buyorsell" class="form-label">Buy or Sell</label>
                  <select class="form-select form-select-sm" v-model="buyorsell">
                    <option value="buy">Buy</option>
                    <option value="sell">Sell</option>
                  </select>
                </div>
              </div>
              <div class="col-6 mb-3">
                  <label for="buyorsell" class="form-label">Order Type</label>
                  <select class="form-select form-select-sm" v-model="ordertype">
                    <option value="Market">Market</option>
                    <option value="Limit">Limit</option>
                  </select>
              </div>
            </div>

            <div v-if="buyorsell=='buy'" class="row">
              <div class="col mb-3">
                <label for="symbol" class="form-label">Stock Symbols</label>
                <VueMultiselect
                  v-model="stocksymbol"
                  :options="stocksymbols_arr"
                  :close-on-select="true"
                  :clear-on-select="false"
                  placeholder="Select one"
                  label="symbol"
                  track-by="symbol"
                />
              </div>
            </div>
            <div v-if="buyorsell=='sell'" class="row">
              <div class="col mb-3">
                <label for="symbol" class="form-label">Stock Symbols</label>
                <VueMultiselect
                  v-model="stocksymbol"
                  :options="customerStocksArr"
                  :close-on-select="true"
                  :clear-on-select="false"
                  placeholder="Select one"
                  label="symbol"
                  track-by="symbol"
                />
              </div>
            </div>

            <div class="row" v-if="ordertype == 'Limit'">
              <div class="col mb-3">
                  <label for="limitprice" class="form-label">Limit Price</label>
                  <input type="number" class="form-control form-control-md input-border-color" id="limitprice" v-model="limitprice">
              </div>
              <div class="col mb-3">
                <label for="expirationtype" class="form-label">Expiration Type</label>
                <select class="form-select form-select-sm" v-model="expirationtype">
                  <option value="Good-til-day">Good till day</option>
                  <option value="Good-til-date">Good till date</option>
                  <option value="Good-til-cancel">Good till cancel</option>
                  </select>
              </div>
              <div v-if="expirationtype === 'Good-til-date' && ordertype === 'Limit'" class="col mb-3">
                  <div class="col mb-3">
                    <label for="maturitydate" class="form-label">Maturity Date</label>
                    <input type="date" class="form-control form-control-md input-border-color" id="maturitydate" v-model="maturitydate">
                  </div>
              </div>
            </div>

            <div class="row">
              <div class="col-6 mb-3">
                  <label for="quantity" class="form-label">Quantity</label>
                  <input type="number" class="form-control form-control-md input-border-color" id="quantity" v-model="quantity">
              </div>
              <div class="col-6 mb-3">
                  <label for="buyorsell" class="form-label">Settlment Account</label>
                  <select class="form-select form-select-sm" v-model="settlementaccount">
                    <option v-for="value, key in this.customeraccount_arr" :key="key" :value="value.accountID">
                      {{value.accountID}} - {{value.currency+value.balance}}
                    </option>
                  </select>
                </div>
            </div>
          
            <div class="d-grid mb-2">
              <button type="submit" class="btn btn-success p-2">Submit</button>
            </div>
        </form>
        </div>
      </div>    
    </div>
  </template>
  
  <script>
  import Modal from "/src/components/Modal";
  import Loading from "/src/components/Loading";
  import VueMultiselect from 'vue-multiselect'
  
  export default {
    name: "BuySellStocks",
  
    components: {
      Modal,
      Loading,
      VueMultiselect
    },
  
    data () {
      return {
        // Customer Account
        customeraccount_arr:[],
        stocksymbols_arr:[],
        customerStocksArr: [],
  
        //Buy or Sell
        buyorsell:null,
        ordertype: null, //market or limit
        quantity: null,
        settlementaccount: null,
        stocksymbol:null,
        limitprice: null,
        expirationtype: null,
        maturitydate:null,
  
        total_price:null,
        account_balance:null,
        // Component item
        loading: null,
        modalMessage:null,
        modalActive: null,
        btnActive: true,
      
        // Errors
        errors: [],
      }
    },
    created() {
      this.loading = true
      
      var headerObj = this.$store.state.headerObj
      headerObj["serviceName"] = "getCustomerAccounts"           
      var header = JSON.stringify(headerObj); 

      this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
        var data = response.data.Content.ServiceResponse
        var errorcode = data.ServiceRespHeader.GlobalErrorID

        if(errorcode == "010000")
        {
            var allaccount_arr = data.AccountList.account
            for(var account_item of allaccount_arr){
              if(account_item.currentStatus == "Open" && account_item.productID == "101"){
                this.customeraccount_arr.push(account_item)
              
              }
            }
            console.log(this.customeraccount_arr)
        }else{
            this.modalActive = true
            this.modalMessage = data.ServiceRespHeader.ErrorDetails
            this.loading=false
          }
      }).catch(error => {
        console.log(error)
      }).finally(() => {    
          var headerObj = this.$store.state.headerObj    
          headerObj["serviceName"] = "getStockSymbols"           
          var header = JSON.stringify(headerObj); 

          this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
          var data = response.data.Content.ServiceResponse
          var errorcode = data.ServiceRespHeader.GlobalErrorID

          if(errorcode == "010000")
          {
              this.stocksymbols_arr = data.StockSymbolList.StockSymbol
              console.log(this.stocksymbols_arr)
          }else{
              this.modalActive = true
              this.modalMessage = data.ServiceRespHeader.ErrorDetails
              this.loading=false
            }
          }).catch(error => {
            console.log(error)
          }).finally(() => {
            var headerObj = this.$store.state.headerObj
            headerObj["serviceName"] = "getCustomerStocks"           
            var header = JSON.stringify(headerObj); 
            
            this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
                var data = response.data.Content.ServiceResponse
                var errorcode = data.ServiceRespHeader.GlobalErrorID
                if(errorcode == "010000")
                {
                    var stock_arr = data.DepositoryList.Depository
                    if(Array.isArray(stock_arr)){
                        this.customerStocksArr = stock_arr
                    }else{
                        this.customerStocksArr.push(stock_arr)
                    }
                    
                }else{
                    this.modalActive = true
                    this.modalMessage = data.ServiceRespHeader.ErrorDetails
                    this.loading=false
                }
            }).catch((error)=>{
                console.log(error)
            }).finally(()=>{
                this.loading = false
            })
          })
      })
    }, 
  
    methods: {
      
      closeModal() {
        this.modalActive = !this.modalActive;
      },
  
      btnYes() {
        this.closeModal()
        this.$router.go(this.$router.currentRoute)
      },
  
      btnNo(){
        //this.$router.push({name:"ViewAllJobs"})
      },
  
      checkForm(){
        this.errors = [];
        if((this.errors).length == 0){
          this.PlaceOrder()
        }
      },
  
      resetField() {
        //this.JobRoleName = "";
        //this.JobRoleDesc = "";
        //this.SelectedSkills = ""
      },

      //if sell
      checkSufficientStocks(){
        this.loading = true
        console.log(this.customerStocksArr)
        console.log(this.stocksymbol.symbol)

        var owned = this.customerStocksArr.filter(stock => stock.symbol === this.stocksymbol.symbol)

        //var owned = this.customerStocksArr.filter(stock => stock.symbol === this.stocksymbol)
        console.log(owned)
        owned = owned[0].quantity

        if(owned >= this.quantity){

          var headerObj = this.$store.state.headerObj   
              var contentObj = {}

              contentObj["settlementAccount"] = this.settlementaccount
              contentObj["symbol"] = this.stocksymbol.symbol
              contentObj["buyOrSell"] = this.buyorsell
              contentObj["quantity"] = this.quantity

              if(this.ordertype=="Market"){
                headerObj["serviceName"] = "placeMarketOrder"   
              }
              else{
                headerObj["serviceName"] = "placeMarketOrder"   
                contentObj["limitprice"] = this.settlementaccount
                contentObj["expirationType"] = this.expirationtype
                contentObj["maturityDate"] = this.maturitydate
              }

              var header = JSON.stringify(headerObj); 
              var content = JSON.stringify(contentObj); 

              this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+content).then((response)=>{
                  var data = response.data.Content.ServiceResponse
                  var errorcode = data.ServiceRespHeader.GlobalErrorID
                  if(errorcode == "010000"){
                      var orderid = data.StockOrder.orderID
                      this.modalActive = true
                      this.modalMessage = this.ordertype + " Order - "+ orderid + " has been successfully created!"
                  }else{
                      this.modalActive = true
                      this.btnActive=false;
                      this.modalMessage = data.ServiceRespHeader.ErrorDetails
                  }     
                }).catch((error)=>{
                   console.log(error)
                }).finally(()=>{
                    this.loading = false
                })
        }else{
          this.loading = false;
          this.btnActive=false;
          this.modalMessage = "You only have " + owned + " stocks. That is insufficient!"   
          this.modalActive = true
              
        }
      },

      //if buy
      checkSufficientFunds(){
          this.loading = true
        
          var headerObj = this.$store.state.headerObj    
          headerObj["serviceName"] = "getStockPrice"           
          var header = JSON.stringify(headerObj); 

          var contentObj = {
            "symbol" : this.stocksymbol.symbol
          }
          var content = JSON.stringify(contentObj); 

          this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+content).then(response=> {
            var data = response.data.Content.ServiceResponse
            var errorcode = data.ServiceRespHeader.GlobalErrorID
            if(errorcode == "010000"){
              if (this.ordertype === 'Market') {
                  this.total_price = data.Stock_Details.price * this.quantity
                } else {
                  this.to = data.Stock_Details.price * this.limitprice
                }
            }     
            var account_balance = this.customeraccount_arr.filter(account => account.accountID === this.settlementaccount)       
            this.account_balance = account_balance[0].balance

          }).catch((error)=>{
              console.log(error)
          }).finally(()=>{
            if(this.account_balance >= this.total_price){
              var headerObj = this.$store.state.headerObj   
              var contentObj = {}

              contentObj["settlementAccount"] = this.settlementaccount
              contentObj["symbol"] = this.stocksymbol.symbol
              contentObj["buyOrSell"] = this.buyorsell
              contentObj["quantity"] = this.quantity

              if(this.ordertype=="Market"){
                headerObj["serviceName"] = "placeMarketOrder"   
              }
              else{
                headerObj["serviceName"] = "placeMarketOrder"   
                contentObj["limitprice"] = this.settlementaccount
                contentObj["expirationType"] = this.expirationtype
                contentObj["maturityDate"] = this.maturitydate
              }

              var header = JSON.stringify(headerObj); 
              var content = JSON.stringify(contentObj); 

              this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+content).then((response)=>{
                  var data = response.data.Content.ServiceResponse
                  var errorcode = data.ServiceRespHeader.GlobalErrorID
                  if(errorcode == "010000"){
                      var orderid = data.StockOrder.orderID
                      this.modalActive = true
                      this.modalMessage = this.ordertype + " Order - "+ orderid + " has been successfully created!"
                  }else{
                      this.modalActive = true
                      this.btnActive=false;
                      this.modalMessage = data.ServiceRespHeader.ErrorDetails
                  }     
                }).catch((error)=>{
                   console.log(error)
                }).finally(()=>{
                    this.loading = false
                })
            }else{
              this.loading = false;
              this.modalActive = true
              this.btnActive=false;
              this.modalMessage = "Insufficient fund!"    
            }  
          })
      },
  
      PlaceOrder() {
        if (this.buyorsell === 'buy') {
            // Check for sufficient funds
            this.checkSufficientFunds()
        } else {
            // Check for sufficient stocks
            this.checkSufficientStocks()
        }
      }
  
    } 
}
    

  </script>

  
  <style src="vue-multiselect/dist/vue-multiselect.css"></style>
  
  <style lang="scss" scoped>
  h2 {
     margin: 0px !important;
  }
  
  .title {
    text-align: center;
  }
  </style>