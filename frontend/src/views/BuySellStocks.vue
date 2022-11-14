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
    <div class="alert alert-danger mb-5" role="alert">
      <h4>Please check your inputs</h4>
      <ul>
        <li class="m-0" v-for="e in errors" :key="e">{{e}}</li>
      </ul>
    </div>
  </div>
    
  <div class="card border-0 shadow p-3 mb-5 bg-white rounded">
    <div class="card-body">
        <form @submit.prevent v-on:submit="checkForm">

          <div class="row">
            <div class="col-6">
              <div class="mb-3">
                <label for="buyorsell" class="form-label">Buy or Sell</label>
                <select class="form-select form-select-md input-border-color" v-model="buyorsell" required>
                  <option value="buy">Buy</option>
                  <option value="sell">Sell</option>
                </select>
              </div>
            </div>
            <div class="col-6 mb-3">
                <label for="buyorsell" class="form-label">Order Type</label>
                <select class="form-select form-select-md input-border-color" v-model="ordertype" required>
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
                <input type="number" class="form-control form-control-md input-border-color" id="limitprice" v-model="limitprice" required>
            </div>
            <div class="col mb-3">
              <label for="expirationtype" class="form-label">Expiration Type</label>
              <select class="form-select form-select-md input-border-color" v-model="expirationtype" required>
                <option value="Good-til-day">Good till day</option>
                <option value="Good-til-date">Good till date</option>
                <option value="Good-til-cancel">Good till cancel</option>
                </select>
            </div>
            <div v-if="expirationtype === 'Good-til-date' && ordertype === 'Limit'" class="col mb-3">
                <div class="col mb-3">
                  <label for="maturitydate" class="form-label">Maturity Date</label>
                  <input type="date" class="form-control form-control-md input-border-color" id="maturitydate" v-model="maturitydate" required>
                </div>
            </div>
          </div>

          <div class="row">
            <div class="col-6 mb-3">
                <label for="quantity" class="form-label">Quantity</label>
                <input type="number" class="form-control form-control-md input-border-color" id="quantity" v-model="quantity" required>
            </div>
            <div class="col-6 mb-3">
                <label for="buyorsell" class="form-label">Settlement Account</label>
                <select class="form-select form-select-md input-border-color" v-model="settlementaccount" required>
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
    
    //get all customer account to be loaded into settlement account fields
    var headerObj = this.$store.state.headerObj
    headerObj["serviceName"] = "getCustomerAccounts"           
    var header = JSON.stringify(headerObj); 

    this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
      var data = response.data.Content.ServiceResponse
      var errorcode = data.ServiceRespHeader.GlobalErrorID

      //if successful
      if(errorcode == "010000")
      {
        var allaccount_arr = data.AccountList.account
        for(var account_item of allaccount_arr){
          if(account_item.currentStatus == "Open" && account_item.productID == "101") //101 = CASA Account
          {
            this.customeraccount_arr.push(account_item)   
          }
        }    
      }

      //if error
      else{
          this.modalActive = true
          this.modalMessage = data.ServiceRespHeader.ErrorDetails
          this.loading=false
        }

    }).catch(error => {
      this.modalActive = true
      this.btnActive=false;
      this.modalMessage = error

    }).finally(() => {   
      //get stocks symbol to be populateed into stock symbol field - if buy
      var headerObj = this.$store.state.headerObj    
      headerObj["serviceName"] = "getStockSymbols"           
      var header = JSON.stringify(headerObj); 

      this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
        var data = response.data.Content.ServiceResponse
        var errorcode = data.ServiceRespHeader.GlobalErrorID

        // if api call sucessful
        if(errorcode == "010000")
        {
          this.stocksymbols_arr = data.StockSymbolList.StockSymbol
          console.log(this.stocksymbols_arr)
        }

        // if api call unsucessful
        else
        {
          this.modalActive = true
          this.modalMessage = data.ServiceRespHeader.ErrorDetails
          this.loading=false
        }
      }).catch(error => {
          this.modalActive = true
          this.btnActive=false;
          this.modalMessage = error

      }).finally(() => {
        //get customer stocks to be populateed into stock symbol field - if sell
        var headerObj = this.$store.state.headerObj
        headerObj["serviceName"] = "getCustomerStocks"           
        var header = JSON.stringify(headerObj); 
        
        this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
          var data = response.data.Content.ServiceResponse
          var errorcode = data.ServiceRespHeader.GlobalErrorID
          
          //if api call successful 
          if(errorcode == "010000")
          {
            var stock_arr = data.DepositoryList.Depository
            if(Array.isArray(stock_arr)){
                this.customerStocksArr = stock_arr
            }
            else{
                this.customerStocksArr.push(stock_arr)
            }   
          }

          //if api call unsuccessfull, display 
          else
          {
            this.modalActive = true
            this.modalMessage = data.ServiceRespHeader.ErrorDetails
            this.loading=false
          }

        }).catch((error)=>{
            this.modalActive = true
            this.btnActive=false;
            this.modalMessage = error

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
      this.$router.push({name:"ViewCustomerStocks"})
    },

    checkForm(){
      this.errors = [];
      if(this.stocksymbol == null){
        this.errors.push("Please select a stock")
      }
      
      if(this.maturitydate != null & new Date(this.maturitydate) < new Date()){
        console.log(this.maturitydate)
        this.errors.push("Invalid date")
      }

      if((this.errors).length == 0){
        this.PlaceOrder()
      }
    },

    //if sell
    checkSufficientStocks(){
      this.loading = true
      var owned = this.customerStocksArr.filter(stock => stock.symbol === this.stocksymbol.symbol)
      owned = owned[0].quantity

      // if sufficient stocks
      if(owned >= this.quantity)
      {
        var headerObj = this.$store.state.headerObj   
        var contentObj = {
          Content:{

          }
        }

        contentObj.Content["settlementAccount"] = this.settlementaccount
        contentObj.Content["symbol"] = this.stocksymbol.symbol
        contentObj.Content["buyOrSell"] = this.buyorsell
        contentObj.Content["quantity"] = this.quantity

        if(this.ordertype=="Market"){
          headerObj["serviceName"] = "placeMarketOrder"   
        }

        else{
          headerObj["serviceName"] = "placeLimitOrder"   
          contentObj.Content["limitPrice"] = this.limitprice
          contentObj.Content["expirationType"] = this.expirationtype

          if(this.expirationtype == "Good-til-date"){
            contentObj.Content["maturityDate"] = this.maturitydate
          }
        }

        var header = JSON.stringify(headerObj); 
        var content = JSON.stringify(contentObj); 

        this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+content).then((response)=>{
          var data = response.data.Content.ServiceResponse
          var errorcode = data.ServiceRespHeader.GlobalErrorID

          //if api call successful
          if(errorcode == "010000"){
              var orderid = data.StockOrder.orderID
              this.modalActive = true
              this.btnActive = true
              this.modalMessage = this.ordertype + " Order - "+ orderid + " has been successfully created! Would you like to make another transaction?"
          }
          
          //if api call unsuccessful
          else
          {
            this.modalActive = true
            this.btnActive=false;
            this.modalMessage = data.ServiceRespHeader.ErrorDetails
          }  

        }).catch((error)=>{
            this.modalActive = true
            this.btnActive=false;
            this.modalMessage = error
        }).finally(()=>{
            this.loading = false
        })
      }

      //if insufficient stocks
      else{
        this.loading = false;
        this.btnActive=false;
        this.modalMessage = "You do not own any of this company stock. You are unable to sell!"   
        this.modalActive = true 
      }
    },
    PlaceOrder() {
      // if buy
      if (this.buyorsell === 'buy') {
        this.loading = true

        var headerObj = this.$store.state.headerObj   
          var contentObj = {
            Content:{
              
            }
          }

          contentObj.Content["settlementAccount"] = this.settlementaccount
          contentObj.Content["symbol"] = this.stocksymbol.symbol
          contentObj.Content["buyOrSell"] = this.buyorsell
          contentObj.Content["quantity"] = this.quantity

          if(this.ordertype=="Market"){
            headerObj["serviceName"] = "placeMarketOrder"   
          }
          else{
            headerObj["serviceName"] = "placeLimitOrder"   
            contentObj.Content["limitPrice"] = this.limitprice
            contentObj.Content["expirationType"] = this.expirationtype
            if(this.expirationtype == "Good-til-date"){
              contentObj.Content["maturityDate"] = this.maturitydate
            }
          }

        var header = JSON.stringify(headerObj); 
        var content = JSON.stringify(contentObj); 

        this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+content).then((response)=>{
          var data = response.data.Content.ServiceResponse
          console.log(response)
          var errorcode = data.ServiceRespHeader.GlobalErrorID
          if(errorcode == "010000"){
              var orderid = data.StockOrder.orderID
              this.modalActive = true
              this.btnActive = true
              this.modalMessage = this.ordertype + " Order - "+ orderid + " has been successfully created! Would you like to make another transaction"
          }else{
              this.modalActive = true
              this.btnActive=false;
              this.modalMessage = data.ServiceRespHeader.ErrorDetails
          }   

        }).catch((error)=>{
            this.modalActive = true
            this.btnActive=false;
            this.modalMessage = error

        }).finally(()=>{
            this.loading = false
        })
      } 

      // if sell
      else 
      {
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