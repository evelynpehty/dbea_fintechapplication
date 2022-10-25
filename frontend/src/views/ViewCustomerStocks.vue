<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
    
    <div class="container">
        <div class="row" style="margin-top:20px">
            <h2 class="title">My Holdings ({{customerStocksArr.length}})</h2>
            <h5 class="title my-4">Portfolio Value: <amt>${{totalHoldingValue}}</amt></h5>
        </div>

        <div class="row mt-5" v-if="customerStocksArr.length == 0">
            <div class="col-md-3"></div>
            <div class="col-md-6 text-center">
                <h1 class="my-3">No Stocks</h1>
                <button class="btn btn-success" @click="PurchaseStock" type="button">Purchase Stocks Now</button>
            </div>
            <div class="col-md-3"></div>
        </div>

        <div v-else>
            <div class="row" tyle="margin-top:20px">
                <input type="text" class="form-control form-control-md input-border-color" placeholder="Search..." id="search" v-model="searchQuery"/>
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
                        <th scope="col">Symbol</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Current Price</th>
                        <th scope="col">Total Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(value,key) in filterStocks" :key="key" >
                            <td><b>{{value.symbol}}</b></td>
                            <td>{{value.quantity}}</td>
                            <td>${{parseFloat(value.price).toFixed(2)}}</td>
                            <td>${{parseFloat(value.price * value.quantity).toFixed(2)}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</template>
  
<script>
import Loading from "../components/Loading";
import Modal from "../components/Modal";
export default {
    name: "ViewCustomerStocks",
    components: {Loading, Modal},
    data() {
        return {
            loading: null,
            modalMessage: null,
            modalActive: null,

            customerStocksArr: [],
            searchQuery: "",

            success:false
        };
    },
    created(){
        this.loading = true

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
                    for(var s of stock_arr){
                        //append stocks with quantity that is not 0 to customerStocksArr
                        if(s.quantity !=0 ){
                            this.customerStocksArr.push(s)
                        }
                    }
                }else{
                    if(stock_arr.quantity != 0)
                    {
                        this.customerStocksArr.push(stock_arr)
                    }                        
                }
                
            }else{
                this.modalActive = true
                this.modalMessage = data.ServiceRespHeader.ErrorDetails
                this.success = false;
            }

        }).catch((error)=>{
            this.modalActive = true
            this.modalMessage = error
        }).finally(()=>{
            this.loading = false
        });

        

    },
    methods: {
        closeModal() {
            this.modalActive = !this.modalActive;
        },
        PurchaseStock() {
            this.$router.push({ name: "BuySellStocks"});
        },
    },
    computed:{
        filterStocks(){
            if(this.searchQuery !== ""){
                return this.customerStocksArr.filter((name)=>{
                    return Object.values(name).some((word) => String(word).toLowerCase().includes(this.searchQuery.toLowerCase()))
                })
            }else{
                return this.customerStocksArr
            }
        },
        totalHoldingValue(){
            var total = 0
            total = this.customerStocksArr.reduce((acc, item) => acc + parseFloat(item.price * item.quantity), 0)
            return total.toFixed(2)
            }
    }
}   

</script>

<style ang="scss" scoped>

h5 {
  font-family: 'ProductSansBold', Arial, sans-serif !important;
  color: black;
}

amt{
    color: var(--purple);
}

</style>