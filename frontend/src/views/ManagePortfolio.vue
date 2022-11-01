<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
    <div class="container-fluid ">
        <div class="row" style="margin-top:40px">
            <h2 class="title">Select your Preferred Portfolio Type</h2>
            <p class="title">Based on your risk profile, please select your preferred portfolio type based on your risk appetite.</p>
        </div>

        <div class="row justify-content-center">
            <div class="col-md-10 col-xl-8">
                <!-- Lowest Risk Portfolio -->
                <div class="row gy-3 mb-5">
                    <div class="col-sm-6 col-md-4">
                        <div class="rounded p-3 border bg-light" @click="btnNext(1)">
                            <img src="../assets/portfolio.png" alt="portfolio" class="p-md-3 img-fluid"/>
                            <h3 class="text-center">Lowest Risk</h3>
                        </div>
                    </div>

                    <!-- Balanced Portfolio -->
                    <div class="col-sm-6 col-md-4">
                        <div class="rounded p-3 border bg-light" @click="btnNext(2)">
                            <img src="../assets/portfolio.png" alt="portfolio" class="p-md-3 img-fluid"/>
                            <h3 class="text-center">Balanced</h3>
                        </div>
                    </div>

                    <!-- Highest Return Portfolio -->
                    <!-- <div class="col-sm-6 col-md-4">
                        <div class="rounded p-3 border bg-light" @click="btnNext(3)">
                            <img src="../assets/portfolio.png" alt="portfolio" class="p-md-3 img-fluid"/>
                            <h3 class="text-center">Highest Return</h3>
                        </div>
                    </div> -->
                </div>
            </div>
        </div>
        
    </div>
  </template>
  
<script>
import Loading from "../components/Loading";
import Modal from "../components/Modal";
export default {
    name: "ManagePortfolio",

    components: {
        Loading, 
        Modal
    },

    data() {
        return {
            loading: null,
            modalMessage: null,
            modalActive: null,

            results: null,

            success:false
        };
    },

    methods: {
        closeModal() {
            this.modalActive = !this.modalActive;
        },

        btnNext(id) {
            this.$router.push({name:"PortfolioEvaluation", params: { portfolioid: id } })
        }
    }       
}
</script>

<style lang="scss" scoped>
h3 {
    margin: 0px !important;
}
.title {
    text-align: center;
}

.bg-light:hover {
    background-color: var(--light-purple) !important;
    -webkit-transition: background-color 0.5s;
}
</style>