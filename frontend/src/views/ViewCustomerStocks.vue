<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
    
    <div class="container">
        <div class="row" style="margin-top:20px">
            <h2 class="title">My Holdings ({{customerStocksArr.length}})</h2>
            <h5 class="title mt-4">Portfolio Value:</h5>
            <h2 class="title"><amt>${{totalHoldingValue}}</amt></h2>
        </div>
        <div class="row">
            <h5 class="mb-4 col-sm-4"><display :style="'color: ' + (cumulative >= 0 ? 'green' : 'red')">${{cumulative.toFixed(2)}}</display><faded class="mx-2">Cumulative P/L</faded></h5>
            <h5 class="mb-4 col-sm-4"><display :style="'color: ' + (total_stockpnl >= 0 ? 'green' : 'red')">{{total_stockpnl.toFixed(2)}}%</display><faded class="mx-2">All Time</faded></h5>
            <h5 class="mb-4 col-sm-4"><display :style="'color: ' + (percentageChange >= 0 ? 'green' : 'red')">{{percentageChange.toFixed(2)}}%</display><faded class="mx-2">1D Change</faded></h5>
            <!-- <h5 class="title my-4 col-sm-6" >Total Invested: <amt>${{totalPurchasedValue}}</amt></h5> -->
        </div>
        <div class="col-12 mb-4">
                <div class="p-4 border rounded bg-light">
                    <h5>Current Asset Distribution</h5>
                    <Bar
                    :chart-options="chartOptions"
                    :chart-data="chartData"
                    :chart-id="chartId"
                    :dataset-id-key="datasetIdKey"
                    :plugins="plugins"
                    :css-classes="cssClasses"
                    :styles="styles"
                    :width="width"
                    :height="height"
                    />
                </div>
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
            <div class="row col-12 mx-auto " tyle="margin-top:20px">
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

            <div v-else class="row col-12 mx-auto" style="margin-top:20px">
                <table class="table table-bordered table-md">
                    <thead class="text-center">
                        <tr>
                        <th scope="col">Symbol</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Avg Cost</th>
                        <th scope="col">Current Price</th>
                        <th scope="col">Current Total Value</th>
                        <th scope="col">Profit/Loss</th>
                        <th scope="col">Profit/Loss (%)</th>
                        </tr>
                    </thead>
                    <tbody class="text-center">
                        <tr v-for="(value,key) in filterStocks" :key="key" >
                            <td><b>{{value.symbol}}</b></td>
                            <td>{{value.quantity}}</td>
                            <td>${{parseFloat(stock_computed[value.symbol].average_cost).toFixed(2)}}</td>
                            <td>${{parseFloat(value.marketPrice).toFixed(2)}}</td>
                            <td><value>${{parseFloat(value.marketPrice * value.quantity).toFixed(2)}}</value></td>
                            <td :style="'color: ' + (parseFloat( (value.marketPrice * stock_computed[value.symbol].total_qty) - (stock_computed[value.symbol].average_cost * stock_computed[value.symbol].total_qty)).toFixed(2) >= 0 ? 'green' : 'red')">${{parseFloat( (value.marketPrice * stock_computed[value.symbol].total_qty) - (stock_computed[value.symbol].average_cost * stock_computed[value.symbol].total_qty)).toFixed(2)}}</td>
                            <td :style="'color: ' + (((value.marketPrice * stock_computed[value.symbol].total_qty) - (stock_computed[value.symbol].average_cost * stock_computed[value.symbol].total_qty))/ (stock_computed[value.symbol].average_cost * stock_computed[value.symbol].total_qty) * 100 >= 0 ? 'green' : 'red')">{{parseFloat( ((value.marketPrice * stock_computed[value.symbol].total_qty) - (stock_computed[value.symbol].average_cost * stock_computed[value.symbol].total_qty))/ (stock_computed[value.symbol].average_cost * stock_computed[value.symbol].total_qty) * 100).toFixed(2)}}%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-lg-12 text-center my-4">
                <button type="redirect" class="btn btn-success p-2">
                    <a class="nav-link mx-2" href="/ManagePortfolio">Optimise Portfolio</a>
                </button>
            </div>
            
        </div>
    </div>

</template>

<script>

import Loading from "../components/Loading";
import Modal from "../components/Modal";
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, BarElement, CategoryScale, LinearScale)

export default {
    name: "ViewCustomerStocks",
    components: {Loading, Modal, Bar},

    props: {
        chartId: {
            type: String,
            default: "bar-chart"
        },
        datasetIdKey: {
            type: String,
            default: "label"
        },
        width: {
            type: Number,
            default: 400
        },
        height: {
            type: Number,
            default: 200
        },
        cssClasses: {
            default: "",
            type: String
        },
        styles: {
            type: Object,
            default: () => {}
        },
        plugins: {
            type: Object,
            default: () => {}
        }
    },

    data() {
        return {
            loading: null,
            modalMessage: null,
            modalActive: null,

            customerStocksArr: [],
            stock_symbols: [],
            stock_quantity: [],
            stock_price: [],
            stockorder_arr:[],
            stock_indiv_arr:[],
            stock_total_cost:[],
            stock_total_qty:[],
            stock_average_cost:[],
            searchQuery: "",
            stock_computed: {
                // symbol:{
                //     total_cost: null,
                //     total_qty: null,
                //     average_cost:null
                // }
            },
            success:false,

            // Chart Data
            chartData: {
                labels: [],
                datasets: [ 
                    { 
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)', 'rgba(255, 159, 64, 0.2)', 'rgba(255, 205, 86, 0.2)', 'rgba(75, 192, 192, 0.2)',
                            'rgba(54, 162, 235, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(201, 203, 207, 0.2)', 'rgba(59, 60, 54, 0.2)',
                            'rgba(197, 29, 52, 0.2)', 'rgba(106, 93, 77, 0.2)', 'rgba(255, 35, 1, 0.2)', 'rgba(37, 41, 74, 0.2)',
                            'rgba(117, 92, 72, 0.2)', 'rgba(137, 58, 61, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132)', 'rgba(255, 159, 64)', 'rgba(255, 205, 86)', 'rgba(75, 192, 192)',
                            'rgba(54, 162, 235)', 'rgba(153, 102, 255)', 'rgba(201, 203, 207)', 'rgba(59, 60, 54)', 
                            'rgba(197, 29, 52)', 'rgba(106, 93, 77)', 'rgba(255, 35, 1)', 'rgba(37, 41, 74)',
                            'rgba(117, 92, 72)', 'rgba(137, 58, 61)',
                        ],
                        borderWidth: 1,
                        data: []
                    } 
                ]
            },

            chartOptions: {
                responsive: true
            },
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
                            this.stock_symbols.push(s.symbol)
                            this.stock_quantity.push(s.quantity)
                            this.stock_price.push(s.price)
                        }
                    }
                    this.chartData.labels = this.stock_symbols
                    this.chartData.datasets[0].data = this.stock_quantity

                }else{
                    if(stock_arr.quantity != 0)
                    {
                        this.customerStocksArr.push(stock_arr)
                    }                        
                }
                console.log(data)
                
            }else{
                this.modalActive = true
                this.modalMessage = data.ServiceRespHeader.ErrorDetails
                this.success = false;
            }

            // Get Stock Prices 
            headerObj["serviceName"] = "getStockPrice"           
            var header = JSON.stringify(headerObj);

            let promises = [];

            for (var symbol of this.stock_symbols) {
                var contentObj = {
                    Content:{
                        "symbol" : symbol
                    }
                }
                var content = JSON.stringify(contentObj);
                
                promises.push(this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+ content))
            }

            Promise.all(promises).then(responses => 
            {
                for(var r in responses) {
                    var errorcode = responses[r].data.Content.ServiceResponse.ServiceRespHeader.GlobalErrorID
                    if (errorcode == "010000"){
                        this.customerStocksArr[r]["marketPrice"] = responses[r].data.Content.ServiceResponse.Stock_Details.price
                        this.customerStocksArr[r]["prevClose"] = responses[r].data.Content.ServiceResponse.Stock_Details.prevClose
                    }
                }
            })
            
            // Get Stock Orders
            headerObj["serviceName"] = "getStockOrders"           
            var header2 = JSON.stringify(headerObj); 
            
            this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header2).then((response)=>{
                var data = response.data.Content.ServiceResponse
                var errorcode = data.ServiceRespHeader.GlobalErrorID
                // console.log(data)
                if(errorcode == "010000")
                {
                    this.stockorder_arr = data.StockOrderList.StockOrder
                    console.log(this.stockorder_arr)
                    for (var order of this.stockorder_arr){
                        console.log(order.stockSymbol)
                        for (var symbol of this.stock_symbols){
                            console.log(symbol)
                                if (order.stockSymbol == symbol & order.buy_or_sell != "sell" & order.order_status == "Filled"){
                                    // console.log(order.stockSymbol)
                                    if (this.stock_computed[symbol]){
                                        console.log(this.stock_computed)
                                        this.stock_computed[symbol].total_cost = parseFloat(this.stock_computed[symbol].total_cost) + parseFloat(order.price_at_execution)
                                        this.stock_computed[symbol].total_qty = String(parseInt(this.stock_computed[symbol].total_qty) + parseInt(order.quantity))
                                        this.stock_computed[symbol].average_cost = parseFloat((this.stock_computed[symbol].total_cost / this.stock_computed[symbol].total_qty))
                                    }
                                    else{
                                        this.stock_computed[symbol] =
                                        {
                                        total_cost: order.price_at_execution * order.quantity,
                                        total_qty: order.quantity,
                                        average_cost: parseFloat( (order.price_at_execution * order.quantity) / order.quantity)
                                        }
                                    }
                                }
                            }
                        }
                }
                else
                {
                    this.modalActive = true
                    this.modalMessage = data.ServiceRespHeader.ErrorDetails
                    this.loading=false
                }
            })
            
            
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
            total = this.customerStocksArr.reduce((acc, item) => acc + parseFloat(item.marketPrice * item.quantity), 0)
            return total.toFixed(2)
        },

        percentageChange(){
            var closed_price = this.customerStocksArr.reduce((acc, item) => acc + parseFloat(item.prevClose * item.quantity), 0)
            var totalHoldingValue = this.customerStocksArr.reduce((acc, item) => acc + parseFloat(item.marketPrice * item.quantity), 0)
            var change = ((totalHoldingValue - closed_price)/closed_price)*100
            return change
        },

        total_stockpnl(){
            var total_bought = this.stockorder_arr.reduce(function(acc, item){
                if (item.order_status =="Filled" & item.buy_or_sell == "buy") acc += parseFloat(item.price_at_execution * item.quantity); return acc}, 0);
            var total_sold = this.stockorder_arr.reduce(function(acc, item){
                if (item.order_status =="Filled" & item.buy_or_sell == "sell") acc += parseFloat(item.price_at_execution * item.quantity); return acc}, 0);
            var totalHoldingValue = this.customerStocksArr.reduce((acc, item) => acc + parseFloat(item.marketPrice * item.quantity), 0)
            var net_invested = total_bought - total_sold
            return ((totalHoldingValue - net_invested)/net_invested)*100
        },

        cumulative(){
            var total_bought = this.stockorder_arr.reduce(function(acc, item){
                if (item.order_status =="Filled" & item.buy_or_sell == "buy") acc += parseFloat(item.price_at_execution * item.quantity); return acc}, 0);
            var total_sold = this.stockorder_arr.reduce(function(acc, item){
                if (item.order_status =="Filled" & item.buy_or_sell == "sell") acc += parseFloat(item.price_at_execution * item.quantity); return acc}, 0);
            var totalHoldingValue = this.customerStocksArr.reduce((acc, item) => acc + parseFloat(item.marketPrice * item.quantity), 0)
            var net_invested = total_bought - total_sold
            return totalHoldingValue - net_invested
        },

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
    font-size: larger;
}

value{
    color: var(--purple);
    font-weight: 600;
}

faded {
    color: grey;
    font-size: small;
}
</style>