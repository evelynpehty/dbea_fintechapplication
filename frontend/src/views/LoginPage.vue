<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
    <section class="vh-100" style="background-color: #CCD8DB;">
      <div class="container h-100">
        <div class="row d-flex flex-wrap justify-content-center align-items-center h-100">
          <div class="col col-xl-10">
            <div class="card p-3" style="border-radius: 1rem;">
    
              <div class="row g-0">
    
                <div class="col-md-6 col-lg-5 d-none d-md-block my-auto">
                  <img
                    src="../assets/logo.png"
                    alt="login"
                    class="img-fluid" style="border-radius: 1rem 0 0 1rem;"
                  />
                </div>
    
                <div class="col-md-6 col-lg-7 d-flex align-items-center">
                  <div class="card-body p-4 p-lg-3 text-black">
    
                    <form @submit.prevent v-on:submit="login">
                      <div class="form-outline mb-4">
                        <label class="form-label" for="userid">UserID</label>
                        <input type="userid" placeholder="Enter Username" class="form-control form-control-lg input-border-color" id="userid" v-model="headerObj.userID" required :disabled="success == true" />
                      </div>
    
                      <div class="form-outline mb-4">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" placeholder="Enter Password..." class="form-control form-control-lg input-border-color" id="password" v-model="headerObj.PIN" :disabled="success == true" required/>
                      </div>

                      <div v-if="success" class="form-outline mb-4">
                        <label for="otp" class="form-label">OTP</label>
                        <input type="otp" placeholder="Enter OTP..." class="form-control form-control-lg input-border-color" id="otp" v-model="headerObj.OTP" required/>
                      </div>
    
                      <div v-if="success" class="d-grid mb-2">
                        <button type="button" @click="login" class="btn btn-success p-2">Login</button>
                      </div>

                      <div v-else class="d-grid mb-2">
                        <button type="button" @click="requestOTP" class="btn btn-success p-2">Get OTP</button>
                      </div>

                    </form>    
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
</template>

<script>
    import Loading from "../components/Loading";
    import Modal from "../components/Modal";
    
    export default {
        name: "LoginPage",
        data() {
            return {
            headerObj:{
                userID: null,
                PIN: "",
                OTP: ""
            },
            
            loading: null,
            modalMessage: null,
            modalActive: null,

            success:false
            };
        },
        components: {
           Loading, Modal
        },
        methods: {
          closeModal() {
          this.modalActive = !this.modalActive;
        },
          requestOTP(){
            this.headerObj["serviceName"] = "requestOTP"
            
            var header = JSON.stringify(this.headerObj);
            this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
               
                var errorcode = response.data.Content.ServiceResponse.ServiceRespHeader.GlobalErrorID
                if(errorcode == "010000")
                {
                    this.success = true;
                }else{
                    this.modalActive = true
                    this.modalMessage = response.data.Content.ServiceResponse.ServiceRespHeader.ErrorDetails
                    this.success = false;
                }
            }).catch((error)=>{
                console.log(error.data)
            })
          },
          login(){
            this.headerObj["serviceName"] = "loginCustomer"
            var header = JSON.stringify(this.headerObj);
            this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header).then((response)=>{
               var data = response.data.Content.ServiceResponse
               var errorcode = data.ServiceRespHeader.GlobalErrorID
               if(errorcode == "010000")
               {    
                    this.$store.commit("setHeaderObj", this.headerObj)
                   this.$router.push({name:"UserMain"})
               }else{
                   this.modalActive = true
                   this.modalMessage = "Invalid OTP, Please try again"
                   this.success = false;
               }
           }).catch((error)=>{
               console.log(error.data)
           })
          }
        }
    }
    </script>
    


    