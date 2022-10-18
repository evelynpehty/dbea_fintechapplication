<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
    <div class="container">
        <div class="row" style="margin-top:20px">
            <h2 class="title">My Stocks</h2>
        </div>
        <div class="row">
            <table class="table table-striped">
                <thead>
                    <tr>
                    <th scope="col">#</th>
                    <th scope="col">Symbol</th>
                    <th scope="col">Quantity</th>
                    <th scope="col">Price</th>
                    <th scope="col">Trading Date</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(value,key) in customerStocksArr" :key="key" >
                        <td>{{ key+1 }}</td>
                        <td>{{value.symbol}}</td>
                        <td>{{value.quantity}}</td>
                        <td>{{value.price}}</td>
                        <td>{{value.tradingDate}}</td>
                    </tr>
                </tbody>
            </table>
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
                        this.customerStocksArr = stock_arr
                    }else{
                        this.customerStocksArr.push(stock_arr)
                    }
                    
                }else{
                    this.modalActive = true
                    this.modalMessage = data.ServiceRespHeader.ErrorDetails
                    this.success = false;
                }
            }).catch((error)=>{
                console.log(error)
            }).finally(()=>{
                this.loading = false
            })
        },
        methods: {
            closeModal() {
            this.modalActive = !this.modalActive;
        },
    }       
}
</script>

<style>

</style>