<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
    
    <div class="container my-5">
        <div class="row">
            <h2 class="title">Stock News</h2>
        </div>

        <div class="row" style="margin-top:20px">
            <input type="text" class="form-control form-control-md input-border-color" placeholder="Search..." id="search" v-model="searchQuery">
        </div>

        <div class="row mt-5" v-if="filterNews.length == 0">
            <div class="col-md-3"></div>
            <div class="col-md-6 text-center">
                <h1 class="my-3">No Results</h1>
                <h4>for "{{searchQuery}}"</h4>
            </div>
            <div class="col-md-3"></div>
        </div>

        <div v-else class="row" style="margin-top:20px">
            <div  v-for="value, key in filterNews" :key=key class="card mx-2 mt-2" style="width: 18rem;">
                <img :src="value.image_url" class="card-img-top" alt="No Image"> 
                    <div class="card-body">
                        <span v-if="value.sentiment == 'Negative'" class="badge bg-danger">Negative</span>
                        <span v-if="value.sentiment == 'Positive'" class="badge bg-success">Positive</span>
                        <span v-if="value.sentiment == 'Neutral'" class="badge bg-warning text-dark">Neutral</span>
                        <p class="card-text">{{value.date}}</p>
                        <h5 class="card-title">{{value.title}}</h5>
                        <p class="card-text">{{value.text}}</p>    
                        <a :href="value.news_url" target="_blank" class="btn btn-primary">Read More</a>
                    </div>
                </div>
        </div>

    
        
    </div>

</template>
  
<script>
import Loading from "../components/Loading";
import Modal from "../components/Modal";
export default {
    name: "StockNews",
    components: {Loading, Modal},
    data() {
        return {
            loading: null,
            modalMessage: null,
            modalActive: null,

            news_array: [],
            stock_symbolArr:[],
            searchQuery: "",

            success:false
        };
    },
    created(){
        this.loading = true

        this.axios.get("https://stocknewsapi.com/api/v1/category?section=general&items=50&page=1&token=m5v7kngq4ezwt4vv4oauk0iulbda5so3lr0u3oit").then((response)=>{
            console.log(response.data.data)
            this.news_array = response.data.data
        }).catch((error)=>{
            this.modalActive = true
            this.modalMessage = error
        }).finally(()=>{
            this.loading = false
        })
    },
    methods: {
        
    },
    computed:{
        filterNews(){
            if(this.searchQuery !== ""){
                return this.news_array.filter((name)=>{
                    return Object.values(name).some((word) => String(word).toLowerCase().includes(this.searchQuery))
                })
            }else{
                return this.news_array
            }
        }
    }
}       

</script>

<style>


</style>