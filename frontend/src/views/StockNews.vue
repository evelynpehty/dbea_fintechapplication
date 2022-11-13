<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
    
    <div class="container">
        <div class="row" style="margin-top:20px">
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
                        <span v-for="t in value.tickers" :key="t" class="badge bg-secondary">{{t}}</span>
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

                this.axios.get("https://stocknewsapi.com/api/v1/category?section=alltickers&items=50&page=1&token=ltdhlfezbea9ac653rwvancvjivq8xtasupfm4rc").then((response)=>{
                    console.log(response.data.data)
                    this.news_array = response.data.data
                }).catch((error)=>{
                    this.modalActive = true
                    this.modalMessage = error
                }).finally(()=>{
                    this.loading = false
                })

                /*for(var sym of this.stock_symbolArr){
                    promises.push(this.axios.get("https://newsapi.org/v2/everything?q="+sym+"&domains=bloomberg.com&apiKey=d404561ccf3a4c52b6b073b72be5f52a"))
                }

                Promise.all(promises).then(responses => 
                    {
                        var temp = []
                        for(var r of responses){
                            var article = r.data.articles   
                            if(article.length != 0){
                                for(var item of article){
                                    temp.push(item)
                                }
                            }
                                    
                        }
                        this.news_array = temp
                        this.loading = false
                        
                    }
                )*/
               
               /*this.axios.get("https://newsapi.org/v2/everything?q="+str_symbol+"&apiKey=d404561ccf3a4c52b6b073b72be5f52a").then((response)=>{
                    console.log(response)
                    this.news_array = response.data.articles

                }).catch((error)=>{
                    this.modalActive = true
                    this.modalMessage = error
                }).finally(()=>{
                    this.loading = false
                })*/

                
        
    

        /*this.axios.get("https://api.marketaux.com/v1/news/all?symbols=&filter_entities=true&language=en&api_token=7L3FbnqKmh7y1kTwaWgIKB2hWpO1moQV87oDEIh9").then((response)=>{
            console.log(response)
            this.news_array = response.data.data

        }).catch((error)=>{
            this.modalActive = true
            this.modalMessage = error
        }).finally(()=>{
            this.loading = false
        })*/
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