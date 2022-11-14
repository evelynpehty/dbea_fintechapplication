<template>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <div class="container">
        <div class="row" style="margin-top:20px">
            <h2 class="title">My Stock Orders</h2>
        </div>

        <div class="row mt-5" v-if="stockorder_arr.length == 0">
            <div class="col-md-3"></div>
            <div class="col-md-6 text-center">
                <h1 class="my-3">No Results</h1>
            </div>
            <div class="col-md-3"></div>
        </div>
            
        <div v-else class="row" style="margin-top:20px">
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <a @click="filterstocks('Filled', 1)" :class="{'nav-link': true, active:1 == currentIndex, 'bg-light': true, 'text-dark': true}" aria-current="page" href="#">Filled</a>
                </li>
                <li class="nav-item">
                    <a @click="filterstocks('Unfilled', 2)" :class="{'nav-link': true, active:2 == currentIndex, 'bg-light': true, 'text-dark': true}" href="#">Unfilled</a>
                </li>
                <li class="nav-item">
                    <a @click="filterstocks('Open', 3)" :class="{'nav-link': true, active:3 == currentIndex, 'bg-light': true, 'text-dark': true}" href="#">Open</a>
                </li>
                <li class="nav-item">
                    <a @click="filterstocks('Cancelled', 4)" :class="{'nav-link': true, active:4 == currentIndex, 'bg-light': true, 'text-dark': true}" href="#">Cancelled</a>
                </li>
            </ul>

            <table v-if="filtered_arr.length != 0" class="table table-bordered table-md text-center">
                <thead>
                    <tr>
                    <th scope="col">Order ID</th>
                    <th scope="col">Order Date</th>
                    <th scope="col">Order Type</th>
                    <th scope="col">Symbol</th>
                    <th scope="col">Quantity</th>
                    <th scope="col">Buy/Sell</th>
                    <th scope="col">Price at Execution</th>
                    <th scope="col">Price at Order</th>
                    <th scope="col">Order Status</th>
                    <th v-if="currentstatus == 'Open'" scope="col">Cancel</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(value,key) in filtered_arr" :key="key" >
                        <td>{{value.orderID}}</td>
                        <td>{{value.order_date}}</td>
                        <td>{{value.orderType}}</td>
                        <td>{{value.stockSymbol}}</td>
                        <td>{{value.quantity}}</td>
                        <td>{{value.buy_or_sell}}</td>
                        <td>{{formatNumber(value.price_at_execution)}}</td>
                        <td>{{formatNumber(value.price_at_order)}}</td>
                        <td>{{value.order_status}}</td>
                        <td v-if="currentstatus == 'Open'"><font-awesome-icon v-if="value.order_status == 'Open'" @click="openModal(value.orderID)" class="mx-auto fa-2x" style="color: red" icon="fa-solid fa-xmark" /></td>
                    </tr>
                    
                </tbody>
                
            </table>
            <div class="row mt-5" v-else>
                <div class="col-md-3"></div>
                <div class="col-md-6 text-center">
                    <h1 class="my-3">No Results</h1>
                </div>
                <div class="col-md-3"></div>
            </div>
        </div>
        <ModalComponent v-if="modalActive" :modalMessage="modalMessage" :btnActive="modalBtn" @btn-yes="cancelOrder()" @btn-no="closeModal()" @close-modal="closeModal()"></ModalComponent>
    </div>
</template>

<script>
import ModalComponent from "../components/Modal.vue";
export default {
    name: "ViewStockOrder",
    components: {
        ModalComponent,
    },
    data(){
        return{
            stockorder_arr:[],
            currentOrderID: "",
            customer:{},
            modalActive:false,
            modalMessage: "",
            modalBtn: null,
            filtered_arr: [],
            currentIndex: 1,
            currentstatus: "Filled",
            reload: false

        }
    },
    created(){
        this.loading = true
        var headerObj = this.$store.state.headerObj    
        headerObj["serviceName"] = "getStockOrders"           
        var header = JSON.stringify(headerObj); 

        this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
            var data = response.data.Content.ServiceResponse
            var errorcode = data.ServiceRespHeader.GlobalErrorID
            console.log(data)
            if(errorcode == "010000")
            {
                this.stockorder_arr = data.StockOrderList.StockOrder
                console.log(this.stockorder_arr)
                this.filterstocks(this.currentstatus, this.currentIndex)
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
        })  
        
    },
    methods:{
        closeModal() {
            this.modalActive = false
            if(this.reload){
                location.reload()
            }
        },

        openModal(orderID) {
            this.reload = false
            this.modalBtn = true
            this.modalActive = true
            this.currentOrderID = orderID
            this.modalMessage = "Are you sure you want to cancel Order " + this.currentOrderID + "?"
        },

        cancelOrder(){
            this.loading = true
            var headerObj = this.$store.state.headerObj    
            headerObj["serviceName"] = "cancelStockOrder"           
            var header = JSON.stringify(headerObj); 

            var contentObj = {
                Content:{
                    "orderID" : this.currentOrderID
                }
            }
            var content = JSON.stringify(contentObj);

            this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+ content)
            .then((response)=>{
                var data = response.data.Content.ServiceResponse
                var errorcode = data.ServiceRespHeader.GlobalErrorID
                
                if(errorcode == "010000")
                {
                    console.log(data)
                    this.modalBtn = false
                    this.reload = true
                    this.modalMessage = "Stock Order:" + this.currentOrderID + " has been cancelled successfully."
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
            }) 
        },

        formatNumber(num) {
            return parseFloat(num).toFixed(2)
        },
        filterstocks(status, index){
            this.currentIndex = index
            this.currentstatus = status
            if(this.stockorder_arr){
                this.filtered_arr = this.stockorder_arr.filter((stock) => stock.order_status === status)
            }
        }
}

}
</script>

<style lang="scss" scoped>
    .active{
        background-color: #000080 !important;
        color: white !important;
    }
</style>