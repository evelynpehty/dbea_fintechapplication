<template>
    <div class="container">
          <div class="row" style="margin-top:20px">
              <h2 class="title">Customer Profile</h2>
          </div>
      </div>
  </template>
  
  <script>
  
    export default {
        name: "CustomerProfile",
        data(){
            return{
                details: [],
            }
        },
        created(){
            var headerObj = this.$store.state.headerObj
            headerObj["serviceName"] = "getCustomerDetails"           
            var header = JSON.stringify(headerObj); 

            this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
                var data = response.data.Content.ServiceResponse
                var errorcode = data.ServiceRespHeader.GlobalErrorID
                if(errorcode == "010000"){
                    console.log(data.DepositoryList.Depository)
                    this.details = data.DepositoryList.Depository
                }
                else{
                    this.modalActive = true
                    this.modalMessage = data.ServiceRespHeader.ErrorDetails
                    this.success = false;
                }

            }).catch((error)=>{
                this.modalActive = true
                this.modalMessage = error
            }).finally(()=>{
                this.loading = false
            })
        },
        methods:{
            
        }
  
    }
  </script>
  
  <style>
  
  </style>