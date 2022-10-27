<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>

    <div class="container-fluid ">
        <div class="row" style="margin-top:40px">
            <h2 class="title">You have selected {{this.portfolioType[this.portfolioID - 1]}} Portfolio</h2>
            <p class="title">Based on your risk appetite, we have curated a new and balanced portfolio for you!</p>
        </div>

        <div class="row g-3">
            <div class="col-12 col-md-6">
                <div class="p-3 border rounded bg-light">
                    <h4>Current Overview</h4>
                    
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

            tempSuggestedPortofolio: [],

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
        // console.log(header)

        this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response) => {

            // Retrieve Customer's Stock
            var data = response.data.Content.ServiceResponse
            var errorcode = data.ServiceRespHeader.GlobalErrorID
            
            var stock_symbols = []
            var stock_quantity = []
            var stock_price = []  

            if(errorcode == "010000")
            {
                var stock_arr = data.DepositoryList.Depository
                if(Array.isArray(stock_arr)) 
                {
                    for(var s of stock_arr){
                        //display stocks with quantity that is not 0 
                        if(s.quantity !=0 ){
                            this.customerStocksArr.push(s)
                            stock_symbols.push(s.symbol)
                            stock_quantity.push(s.quantity)
                            stock_price.push(s.price)
                        }
                    }
                    this.chartData.labels = stock_symbols
                    this.chartData.datasets[0].data = stock_quantity
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

        }).catch((error) => {
            this.modalActive = true
            this.modalMessage = error
        }).finally(() => {
            this.loading = false
            // Retrieve Suggested Portfolio
            // this.axios.post("http://localhost:5000/getlowestriskportfolio")
        })
    },

    methods: {
        closeModal() {
            this.modalActive = !this.modalActive;
        }
    }
}
</script>

<style lang="scss" scoped>
.title {
    text-align: center;
}

</style>