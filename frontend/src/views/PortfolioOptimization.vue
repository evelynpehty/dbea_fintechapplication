<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
    <div class="container">
        <div class="row">
 
        </div>
    </div>
  </template>
  
  <script>
import Loading from "../components/Loading";
import Modal from "../components/Modal";
export default {
        name: "PortfolioOptimization",
        components: {Loading, Modal},
        data() {
            return {
                loading: null,
                modalMessage: null,
                modalActive: null,

                results: null,

                success:false
            };
        },
        created(){
            this.loading = true

            var json = {
                    "start_date":"2017-01-01",
                    "end_date": "2021-12-31",
                    "tickers": ["AAPL","TSLA"],
                    "total_portfolio_value": 30000
                    }
            
            this.axios.post("http://localhost:5000/getoptimizeportfolio", json).then((response)=>{
                console.log(response.data.response)
                
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