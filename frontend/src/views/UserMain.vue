<template>
    <Loading v-show="loading" />

    <div class="container">
        <div class="row" style="margin-top:20px">
            <h2 class="title">Stocks Price</h2>
            <input type="text" class="form-control form-control-md input-border-color" placeholder="Search..." id="search" v-model="searchQuery">
        </div>
            
        <div class="row mt-5" v-if="filterStocks.length == 0">
            <div class="col-md-3"></div>
            <div class="col-md-6 text-center">
                <h1 class="my-3">No Results</h1>
                <h4>for "{{searchQuery}}"</h4>
            </div>
            <div class="col-md-3"></div>
        </div>
            
        <div v-else class="row" style="margin-top:20px">
            <table class="table table-bordered table-md">
                <thead>
                    <tr>
                    <th scope="col">#</th>
                    <th scope="col">Company</th>
                    <th scope="col">Symbol</th>
                    <th scope="col">Price</th>
                    <th scope="col">Volume</th>
                    <th scope="col">Previous Close</th>
                    <th scope="col">Percentage Change (%)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(value,key) in filterStocks" :key="key" >
                        <td>{{ key+1 }}</td>
                        <td>{{value.company}}</td>
                        <td>{{value.symbol}}</td>
                        <td>{{formatNumber(value.price)}}</td>
                        <td>{{value.volume}}</td>
                        <td>{{formatNumber(value.prevClose)}}</td>
                        <td :class="{positive: value.percentageChange >= 0, negative: value.percentageChange < 0}" >{{formatNumber(value.percentageChange)}}</td>
                    </tr>
                    
                </tbody>
                
            </table>
        </div>
    </div>
  </template>
  
  <script>
import Loading from "../components/Loading";
export default {
        name: "UserMain",
        components: {Loading},
        data() {
            return {
                stocksymbols_arr:[],
                stockprice_arr:[],
                searchQuery: "",

                loading: null,
                modalMessage: null,
                modalActive: null,

                success:false
            };
        },
        created(){
            this.loading = true
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
                }
                else
                {
                    this.modalActive = true
                    this.modalMessage = data.ServiceRespHeader.ErrorDetails
                    this.loading=false
                }
            }).catch((error)=>{
                this.modalActive = true
                this.modalMessage = error
            }).finally(()=>{
                headerObj["serviceName"] = "getStockPrice"           
                var header = JSON.stringify(headerObj); 
            
                let promises = [];    

                for(var stock_item of this.stocksymbols_arr){
                    var contentObj = {
                        Content:{
                            "symbol" : stock_item.symbol
                        }
                    }
                    var content = JSON.stringify(contentObj);
                  
                    promises.push(this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+ content))
                }

                Promise.all(promises).then(responses => 
                    {
                        console.log(responses)
                        for(var r of responses){
                            var errorcode = r.data.Content.ServiceResponse.ServiceRespHeader.GlobalErrorID
                            if (errorcode == "010000"){
                                this.stockprice_arr.push(r.data.Content.ServiceResponse.Stock_Details)
                            }   
                        }
                        this.loading = false
                        console.log(this.stockprice_arr)
                    }
                )
            })
        },
        methods:{
            formatNumber(num) {
                return parseFloat(num).toFixed(2)
            },
        },
        computed:{
            filterStocks(){
                if(this.searchQuery !== ""){
                    return this.stockprice_arr.filter((name)=>{
                        return Object.values(name).some((word) => String(word).toLowerCase().includes(this.searchQuery))
                    })
                }else{
                    return this.stockprice_arr
                }
            }
        }
    }
           

</script>

<style>

.positive {
  color: green;
}
.negative {
  color: red;
}

</style>