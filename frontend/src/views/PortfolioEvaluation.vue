<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>

    <div class="container-fluid ">
        <div class="row" style="margin-top:40px">
            <h2 class="title">You have selected {{this.portfolioType[this.portfolioID - 1]}} Portfolio</h2>
            <p class="title">Based on your risk appetite, we have curated a new and balanced portfolio for you!</p>
        </div>
        <div class="row justify-content-center">
            <div class="col-xl-8">
                <div class="row g-3">
                    <div class="col-12 col-md-6">
                        <div class="p-3 border rounded bg-light">
                            <h4>Current Overview</h4>
                            <h6>Total Market Value
                                <!-- To break a new line in title attribute, use &#10; -->
                                <span 
                                    class="icon" 
                                    title="Place information here">
                                    <font-awesome-icon icon="fa-solid fa-circle-info" /> : 
                                </span>                        
                                <span>${{totalAmount}}</span>
                            </h6>
                        </div>
                    </div>

                    <div class="col-12 col-md-6">
                        <div class="p-3 border rounded bg-light">
                            <h4>Current Holdings</h4>
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

                    <div class="col-12">
                        <div class="p-3 border rounded bg-light">
                            <h4>Suggested Portfolio</h4>
                            <p>
                                <a class="btn btn-success" data-bs-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">
                                    Read More
                                </a>
                            </p>
                            <div class="collapse mb-3" id="collapseExample">
                                <div class="card card-body">
                                    Some placeholder content for the collapse component. This panel is hidden by default but revealed when the user activates the relevant trigger.
                                </div>
                            </div>

                            <h6>Start Date: <span>{{this.start_date}}</span></h6>
                            <h6>End Date: <span>{{this.end_date}}</span></h6>
                            <h6>Volatility
                                <!-- To break a new line in title attribute, use &#10; -->
                                <span 
                                    class="icon" 
                                    title="Volatility is the rate at which the price of a stock increases or decreases over a particular period.&#10;The higher the percentage, the more volatile your portfolio is, and vice versa.">
                                    <font-awesome-icon icon="fa-solid fa-circle-info" /> : 
                                </span>                        
                                <span>{{parseFloat(this.annual_volatility * 100).toFixed(2)}}%</span>
                            </h6>
                            <h6>Expected Annual Returns
                                <!-- To break a new line in title attribute, use &#10; -->
                                <span 
                                    class="icon" 
                                    title="The expected annual return is the profit or loss that an investor anticipates on an investment.">
                                    <font-awesome-icon icon="fa-solid fa-circle-info" /> : 
                                </span>
                                <span>{{parseFloat(this.expected_annual_return * 100).toFixed(2)}}%</span>
                            </h6>
                            <h6>Risk Adjusted Returns
                                <!-- To break a new line in title attribute, use &#10; -->
                                <span 
                                    class="icon" 
                                    title="Risk-adjusted return is a calculation of the return (or potential return) on an investment&#10;such as a stock or corporate bond when compared to cash or equivalents.&#10;&#10;RAR Ratio between 1 and 2 is considered good.&#10;A ratio between 2 and 3 is very good, and any result higher than 3 is excellent.">
                                    <font-awesome-icon icon="fa-solid fa-circle-info" /> : 
                                </span>
                                <span>{{parseFloat(this.sharpe_ratio).toFixed(2)}}</span>
                            </h6>
                        </div>

                        <table class="table table-bordered table-md">
                            <thead>
                                <tr>
                                <th scope="col">#</th>
                                <th scope="col">Symbol</th>
                                <th scope="col">Market Price</th>
                                <th scope="col">Last Price</th>
                                <th scope="col">Current Quantity</th>
                                <th scope="col">New Quantity</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(value,key) in this.customerStocksArr" :key="key" >
                                    <td>{{ key + 1 }}</td>
                                    <td>{{value.symbol}}</td>
                                    <td>${{value.price}}</td>
                                    <td>${{value.marketPrice}}</td>
                                    <td>{{value.quantity}}</td>
                                    <td>{{value.newQuantity}}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>

<script>
import Loading from "../components/Loading";
import Modal from "../components/Modal";
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, BarElement, CategoryScale, LinearScale)

export default {
    name: "PortfolioEvaluation",

    components: {
        Loading, 
        Modal,
        Bar
    },

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
            // Static Colors
            loading: null,
            modalMessage: null,
            modalActive: null,

            customerStocksArr: [],
            stock_symbols: [],
            stock_quantity: [],
            stock_price: [],

            start_date: "",
            end_date: "",

            tempStockPrice: [],
            StockPrice: [],

            tempSuggestedPortfolio: [],
            SuggestedPortfolio: [],
            annual_volatility: null,
            expected_annual_return: null,
            sharpe_ratio: null,

            success: false,

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

            // Static Data
            portfolioType : ["Low Risk", "Balanced", "High Returns"],
            test: {
                "start_date":"2017-01-01",
                "end_date": "2021-12-31",
                "tickers":["AAPL", "TSLA"]  
            },

            // Parameters from Manage Portfolio Page
            portfolioID: this.$route.params.portfolioid,
        }
    },

    created() {
        this.loading = true
        var headerObj = this.$store.state.headerObj
        headerObj["serviceName"] = "getCustomerStocks"           
        var header = JSON.stringify(headerObj);

        this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response) => {

            // Retrieve Customer's Stock
            var data = response.data.Content.ServiceResponse
            var errorcode = data.ServiceRespHeader.GlobalErrorID

            if(errorcode == "010000")
            {
                var stock_arr = data.DepositoryList.Depository

                if(Array.isArray(stock_arr)) 
                {
                    for(var s of stock_arr){
                        //display stocks with quantity that is not 0  
                        if(s.quantity !=0 ){
                            this.customerStocksArr.push(s)
                            this.stock_symbols.push(s.symbol)
                            this.stock_quantity.push(s.quantity)
                            this.stock_price.push(s.price)
                        }
                    }
                    this.chartData.labels = this.stock_symbols
                    this.chartData.datasets[0].data = this.stock_quantity
                } else {
                    if(stock_arr.quantity != 0)
                    {
                        this.customerStocksArr.push(stock_arr)
                    }                        
                }
            } else {
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
                        this.customerStocksArr[r]["prevClose"] = responses[r].data.Content.ServiceResponse.Stock_Details.prevClose
                        this.customerStocksArr[r]["marketPrice"] = responses[r].data.Content.ServiceResponse.Stock_Details.price
                    }
                }
            })

            
        }).catch((error) => {
            this.modalActive = true
            this.modalMessage = error
        }).finally(() => {
            this.start_date = "2017-01-01"
            this.end_date = "2021-12-31"

            var jsonSuggestedPortfolio = {
                "start_date" : this.start_date,
                "end_date": this.end_date,
                "tickers" : this.stock_symbols
            }

            if (this.portfolioID == 1) {
                this.axios.post("http://localhost:5000/getlowestriskportfolio", jsonSuggestedPortfolio).then((response) => {
                this.tempSuggestedPortfolio = response.data.response
                }).catch(error => {
                    this.modalMessage = error.response.data.message 
                }).finally(() => {
                    this.SuggestedPortfolio = this.tempSuggestedPortfolio
                    this.annual_volatility = this.SuggestedPortfolio.performance.annual_volatility
                    this.expected_annual_return = this.SuggestedPortfolio.performance.expected_annual_return
                    this.sharpe_ratio = this.SuggestedPortfolio.performance.sharpe_ratio
                    this.cleaned_weights = this.SuggestedPortfolio.cleaned_weights
                    for (var x in this.customerStocksArr) {
                        this.customerStocksArr[x]["newQuantity"] = parseFloat((this.totalAmount * this.cleaned_weights[this.customerStocksArr[x].symbol]) / this.customerStocksArr[x].price ).toFixed(2)
                    }
                    this.loading = false
                })
            } else if (this.portfolioID == 2) {
                this.axios.post("http://localhost:5000/getoptimizeportfolio", jsonSuggestedPortfolio).then((response) => {
                this.tempSuggestedPortfolio = response.data.response
                }).catch(error => {
                    this.modalMessage = error.response.data.message 
                }).finally(() => {
                    this.SuggestedPortfolio = this.tempSuggestedPortfolio
                    this.annual_volatility = this.SuggestedPortfolio.performance.annual_volatility
                    this.expected_annual_return = this.SuggestedPortfolio.performance.expected_annual_return
                    this.sharpe_ratio = this.SuggestedPortfolio.performance.sharpe_ratio
                    this.cleaned_weights = this.SuggestedPortfolio.cleaned_weights
                    for (var x in this.customerStocksArr) {
                        this.customerStocksArr[x]["newQuantity"] = parseFloat((this.totalAmount * this.cleaned_weights[this.customerStocksArr[x].symbol]) / this.customerStocksArr[x].price ).toFixed(2)
                    }
                    this.loading = false
                })
            }
        })
    },

    computed: {
        totalAmount() {
            var total = 0
            for (var i in this.stock_price) {
                total += this.stock_price[i] * this.stock_quantity[i]
            }
            return parseFloat(total).toFixed(2)
        }
    },

    methods: {
        closeModal() {
            this.modalActive = !this.modalActive;
        }
    }
}
</script>

<style lang="scss" scoped>
span {
    color: black;
}

.icon {
    color: var(--purple);
}
.title {
    text-align: center;
}

</style>