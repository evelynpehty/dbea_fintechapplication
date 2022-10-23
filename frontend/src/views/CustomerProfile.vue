<template>
    <div class="container">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        <Loading v-show="loading" />

        <div class="row" style="margin-top:20px">
            <h2 class="title mb-4">Customer Profile</h2>

            <div class="col">
                <p class="fs-3">Hello {{details.givenName}}</p>
                <p class="fs-5">This is your profile page. You can change your details as needed here.</p>

                <button class="btn btn-primary mb-5">Edit profile</button>
            </div>

        </div>

        <div class="container-fluid">
            <div class="row">
                <!-- Display details -->
                <div class="col-xl-4 order-xl-2 mb-5">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col text-center">
                                    <p class="fs-4 mb-1">{{details.givenName}}, {{getAge()}}</p>
                                    <p class="mb-4"><i class="fa-solid fa-map-pin"></i> {{details.address.country}}</p>
                                    <p class="fs-5"><i class="fa-solid fa-suitcase"></i> {{details.profile.occupation}}</p>
                                    <p class="fs-5"><i class="fa-solid fa-flag"></i> {{details.profile.nationality}}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- My Account Card -->
                <div class="col-xl-8 order-xl-1">
                    <div class="card mb-5">
                        <div class="card-header bg-white border-0">
                        <div class="row align-items-center">
                            <div class="col">
                                <h3 class="m-3">My account</h3>
                            </div>
                        </div>
                        <div class="card-body">
                            <h6 class="heading-small text-muted mb-4">User Information</h6>
                            <div class="row">
                                <div class="col-lg-6 mb-4">
                                    <label class="form-control-label" for="input-id">User ID</label>
                                    <input type="text" id="input-id" class="form-control" placeholder="User ID" :value=details.taxIdentifier disabled>
                                </div>
                                <div class="col-lg-6 mb-4">
                                    <label class="form-control-label" for="input-email">Email</label>
                                    <input type="text" id="input-email" class="form-control" placeholder="Email" :value=details.profile.email disabled>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-6 mb-4">
                                    <label class="form-control-label" for="input-fn">First name</label>
                                    <input type="text" id="input-fn" class="form-control" placeholder="First name" :value=details.givenName disabled>
                                </div>
                                <div class="col-lg-6 mb-4">
                                    <label class="form-control-label" for="input-ln">Last name</label>
                                    <input type="text" id="input-ln" class="form-control" placeholder="First name" :value=details.familyName disabled>
                                </div>
                            </div>
                            <hr class="my-4">
                            <!-- Address -->
                            <h6 class="heading-small text-muted mb-4">Contact Information</h6>
                            <div class="row">
                                <div class="col-md mb-4">
                                    <label class="form-control-label" for="input-address">Address</label>
                                    <input id="input-address" type="text" class="form-control" placeholder="Home Address"  :value=details.address.streetAddress1 disabled>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-4 mb-4">
                                    <label class="form-control-label" for="input-city">City</label>
                                    <input type="text" id="input-city" class="form-control" placeholder="City" :value=details.address.city disabled>
                                </div>
                                <div class="col-lg-4 mb-4">
                                    <label class="form-control-label" for="input-country">Country</label>
                                    <input type="text" id="input-country" class="form-control" placeholder="Country" :value=details.address.country disabled>
                                </div>
                                <div class="col-lg-4 mb-4">
                                    <label class="form-control-label" for="input-postal">Postal code</label>
                                    <input type="text" id="input-postal" class="form-control" placeholder="Postal code" :value=details.address.postalCode disabled>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-6 mb-4">
                                    <label class="form-control-label" for="input-countrycode">Country code</label>
                                    <input type="text" id="input-countrycode" class="form-control" placeholder="Country code" :value=details.cellphone.countryCode disabled>
                                </div>
                                <div class="col-lg-6 mb-4">
                                    <label class="form-control-label" for="input-phone">Phone</label>
                                    <input type="text" id="input-phone" class="form-control" placeholder="Phone" :value=details.cellphone.phoneNumber disabled>
                                </div>
                            </div>
                            <hr class="my-4">
                            <!-- Description -->
                            <h6 class="heading-small text-muted mb-4">About Me</h6>
                            <div class="row">
                                <div class="col-lg-6 mb-4">
                                    <label class="form-control-label" for="input-custID">Customer ID</label>
                                    <input type="text" id="input-custID" class="form-control" placeholder="Customer ID" :value=details.customer.customerID disabled>
                                </div>
                                <div class="col-lg-6 mb-4">
                                    <label class="form-control-label" for="input-nationality">Nationality</label>
                                    <input type="text" id="input-nationality" class="form-control" placeholder="Nationality" :value=details.profile.nationality disabled>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-4 mb-4">
                                    <label class="form-control-label" for="input-occupation">Occupation</label>
                                    <input type="text" id="input-occupation" class="form-control" placeholder="Occupation" :value=details.profile.occupation disabled>
                                </div>
                                <div class="col-lg-4 mb-4">
                                    <label class="form-control-label" for="input-dob">Date of birth</label>
                                    <input type="text" id="input-dob" class="form-control" placeholder="Date of birth" :value=details.dateOfBirth disabled>
                                </div>
                                <div class="col-lg-4 mb-4">
                                    <label class="form-control-label" for="input-gender">Gender</label>
                                    <input type="text" id="input-gender" class="form-control" placeholder="Gender" :value=details.profile.gender disabled>
                                </div>
                            </div>
                        </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        
          
      </div>
  </template>
  
  <script>
    import Loading from "/src/components/Loading";
    export default {
        name: "CustomerProfile",

        components: {
        Loading,
        },

        data(){
            return{
                details: [],
                age: 0,
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
                    console.log(data.CDMCustomer)
                    this.details = data.CDMCustomer
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
            getAge(){
                var dob = this.details.dateOfBirth
                var today = new Date();
                var dob_array = dob.split('-')

                var age = today.getFullYear() - dob_array[0];
                
                var m = today.getMonth() - dob_array[1];
                if (m < 0 || (m === 0 && today.getDate() < dob_array[2])) {
                    this.age--;
                }
                return age
            },
        },
  
    }
  </script>
  
  <style>
  
  </style>