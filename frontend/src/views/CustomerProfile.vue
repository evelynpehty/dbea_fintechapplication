<template>
    <div class="container">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        <Loading v-show="loading" />
        <Modal v-if="modalActive" :modalMessage="modalMessage" :btnActive="btnActive" v-on:close-modal="closeModal" v-on:btn-yes="btnYes" v-on:btn-no="btnNo"/>

        <div class="row" style="margin-top:20px">
            <h2 class="title mb-4">Customer Profile</h2>

            <div class="col">
                <p class="fs-3">Hello {{givenName}}</p>
                <p class="fs-5">This is your profile page. You can change your details as needed here.</p>

                <button class="btn btn-primary mt-3 mb-5 py-2 px-3" @click="editProfile()">Edit profile</button>
            </div>
        </div>

        <div v-if="check_edit_btn" class="container-fluid">
            <div class="row">
                <!-- Display details -->
                <div class="col-xl-4 order-xl-2 mb-5">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col text-center">
                                    <p class="fs-4 mb-1">{{givenName}} {{familyName}}, {{getAge()}}</p>
                                    <p class="mb-4"><i class="fa-solid fa-map-pin"></i> {{country}}</p>
                                    <p class="fs-5"><i class="fa-solid fa-suitcase"></i> {{occupation}}</p>
                                    <p class="fs-5"><i class="fa-solid fa-flag"></i> {{details.profile.nationality}}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- My Account Card -->
                <div class="col-xl-8 order-xl-1">
                    <div class="card mb-4">
                        <div class="card-header bg-white border-0">
                        <div class="row align-items-center">
                            <div class="col">
                                <h3 class="m-3">My account</h3>
                            </div>
                        </div>
                        <div class="card-body">
                            <h6 class="heading-small text-muted mb-4">User Information</h6>
                            <div class="pl-lg-4">
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-id">User ID</label>
                                        <input type="text" id="input-id" class="form-control" placeholder="User ID" v-model=details.taxIdentifier disabled>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-pin">PIN</label>
                                        <input type="text" id="input-pin" class="form-control" placeholder="PIN" v-model=pin>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg mb-4">
                                        <label class="form-control-label" for="input-email">Email</label>
                                        <input type="text" id="input-email" class="form-control" placeholder="Email" v-model=emailAddress>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-fn">First name</label>
                                        <input type="text" id="input-fn" class="form-control" placeholder="First name" v-model=givenName>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-ln">Last name</label>
                                        <input type="text" id="input-ln" class="form-control" placeholder="Last name" v-model=familyName>
                                    </div>
                                </div>
                            </div>
                            
                            <hr class="my-4">
                            <!-- Address -->
                            <h6 class="heading-small text-muted mb-4">Contact Information</h6>
                            <div class="pl-lg-4">
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-address">Address</label>
                                        <input id="input-address" type="text" class="form-control" placeholder="Home Address"  v-model=streetAddress>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-postal">Postal code</label>
                                        <input type="text" id="input-postal" class="form-control" placeholder="Postal code" v-model=postalCode>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-city">City</label>
                                        <input type="text" id="input-city" class="form-control" placeholder="City" v-model=city>
                                    </div>
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-state">State</label>
                                        <input type="text" id="input-state" class="form-control" placeholder="State" v-model=state>
                                    </div>
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-country">Country</label>
                                        <input type="text" id="input-country" class="form-control" placeholder="Country" v-model=country>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-countrycode">Country code</label>
                                        <input type="text" id="input-countrycode" class="form-control" placeholder="Country code" v-model=countryCode>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-phone">Phone</label>
                                        <input type="text" id="input-phone" class="form-control" placeholder="Phone" v-model=mobileNumber>
                                    </div>
                                </div>
                            </div>
                            
                            <hr class="my-4">
                            <!-- Description -->
                            <h6 class="heading-small text-muted mb-4">About Me</h6>
                            <div class="pl-lg-4">
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-custID">Customer ID</label>
                                        <input type="text" id="input-custID" class="form-control" placeholder="Customer ID" v-model=details.customer.customerID disabled>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-nationality">Nationality</label>
                                        <input type="text" id="input-nationality" class="form-control" placeholder="Nationality" v-model=details.profile.nationality disabled>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-occupation">Occupation</label>
                                        <input type="text" id="input-occupation" class="form-control" placeholder="Occupation" v-model=occupation>
                                    </div>
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-dob">Date of birth</label>
                                        <input type="text" id="input-dob" class="form-control" placeholder="Date of birth" v-model=dateOfBirth>
                                    </div>
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-gender">Gender</label>
                                        <select class="form-select" id="input-gender" v-model="gender">
                                            <option v-for="(g, index) in genders" :key="index" :value="g.code">
                                                {{g.description}}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            
                        </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="text-center mb-5">
                <button class="btn btn-primary mx-3 px-5" type="button" @click="updateChanges()">Update Changes</button>
                <button class="btn btn-outline-danger" type="button" @click="backbtn()">Cancel</button>
            </div>
            
        </div>

        <div v-else class="container-fluid">
            <div class="row">
                <!-- Display details -->
                <div class="col-xl-4 order-xl-2 mb-5">
                    <div class="card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col text-center">
                                    <p class="fs-4 mb-1">{{givenName}} {{familyName}}, {{getAge()}}</p>
                                    <p class="mb-4"><i class="fa-solid fa-map-pin"></i> {{country}}</p>
                                    <p class="fs-5"><i class="fa-solid fa-suitcase"></i> {{occupation}}</p>
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
                            <div class="pl-lg-4">
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-id">User ID</label>
                                        <input type="text" id="input-id" class="form-control" placeholder="User ID" v-model=details.taxIdentifier disabled>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-email">Email</label>
                                        <input type="text" id="input-email" class="form-control" placeholder="Email" v-model=emailAddress disabled>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-fn">First name</label>
                                        <input type="text" id="input-fn" class="form-control" placeholder="First name" v-model=givenName disabled>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-ln">Last name</label>
                                        <input type="text" id="input-ln" class="form-control" placeholder="Last name" v-model=details.familyName disabled>
                                    </div>
                                </div>
                            </div>
                            
                            <hr class="my-4">
                            <!-- Address -->
                            <h6 class="heading-small text-muted mb-4">Contact Information</h6>
                            <div class="pl-lg-4">
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-address">Address</label>
                                        <input id="input-address" type="text" class="form-control" placeholder="Home Address" v-model=streetAddress disabled>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-postal">Postal code</label>
                                        <input type="text" id="input-postal" class="form-control" placeholder="Postal code" v-model=postalCode disabled>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-city">City</label>
                                        <input type="text" id="input-city" class="form-control" placeholder="City" v-model=city disabled>
                                    </div>
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-state">State</label>
                                        <input type="text" id="input-state" class="form-control" placeholder="State" v-model=state disabled>
                                    </div>
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-country">Country</label>
                                        <input type="text" id="input-country" class="form-control" placeholder="Country" v-model=country disabled>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-countrycode">Country code</label>
                                        <input type="text" id="input-countrycode" class="form-control" placeholder="Country code" v-model=countryCode disabled>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-phone">Phone</label>
                                        <input type="text" id="input-phone" class="form-control" placeholder="Phone" v-model=mobileNumber disabled>
                                    </div>
                                </div>
                            </div>
                            
                            <hr class="my-4">
                            <!-- Description -->
                            <h6 class="heading-small text-muted mb-4">About Me</h6>
                            <div class="pl-lg-4">
                                <div class="row">
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-custID">Customer ID</label>
                                        <input type="text" id="input-custID" class="form-control" placeholder="Customer ID" v-model=details.customer.customerID disabled>
                                    </div>
                                    <div class="col-lg-6 mb-4">
                                        <label class="form-control-label" for="input-nationality">Nationality</label>
                                        <input type="text" id="input-nationality" class="form-control" placeholder="Nationality" v-model=details.profile.nationality disabled>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-occupation">Occupation</label>
                                        <input type="text" id="input-occupation" class="form-control" placeholder="Occupation" v-model=occupation disabled>
                                    </div>
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-dob">Date of birth</label>
                                        <input type="text" id="input-dob" class="form-control" placeholder="Date of birth" v-model=dateOfBirth disabled>
                                    </div>
                                    <div class="col-lg-4 mb-4">
                                        <label class="form-control-label" for="input-gender">Gender</label>
                                        <input type="text" id="input-gender" class="form-control" placeholder="Gender" v-model=gender disabled>
                                    </div>
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
    import Modal from "/src/components/Modal";
    
    export default {
        name: "CustomerProfile",

        components: {
            Modal,
            Loading,
        },

        data(){
            return{
                details: [],
                familyName: '',
                givenName: '',
                dateOfBirth: '',
                gender: '',
                occupation: '',
                streetAddress: '',
                city: '',
                state: '',
                country: '',
                postalCode: '',
                emailAddress: '',
                countryCode: '',
                mobileNumber: '',

                genders: [{code:"F", description:'Female'}, 
                            {code:"M", description:'Male'}],

                age: 0,
                check_edit_btn: false,
                pin: '',
                account_pin: '',

                // Component item
                loading: null,
                modalMessage:null,
                modalActive: null,
                btnActive: true,
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

                    this.familyName = this.details.familyName
                    this.givenName = this.details.givenName
                    this.dateOfBirth = this.details.dateOfBirth
                    this.gender = this.details.profile.gender == 'F' ? 'Female' : 'Male'
                    this.occupation = this.details.profile.occupation
                    this.streetAddress = this.details.address.streetAddress1
                    this.city = this.details.address.city
                    this.state = this.details.address.state
                    this.country = this.details.address.country
                    this.postalCode = this.details.address.postalCode
                    this.emailAddress = this.details.profile.email
                    this.countryCode = this.details.cellphone.countryCode
                    this.mobileNumber = this.details.cellphone.phoneNumber

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
            closeModal() {
                this.modalActive = !this.modalActive;
            },

            btnYes() {
                this.closeModal()
            },

            btnNo(){
                this.modalActive = !this.modalActive;
                this.$router.go(this.$router.currentRoute)
            },

            backbtn(){
                this.$router.go(this.$router.currentRoute)
            },

            getAge(){
                var dob = this.dateOfBirth
                var today = new Date();
                var dob_array = dob.split('-')

                var age = today.getFullYear() - dob_array[0];
                
                var m = today.getMonth() - dob_array[1];
                if (m < 0 || (m === 0 && today.getDate() < dob_array[2])) {
                    this.age--;
                }
                return age
            },

            editProfile(){
                this.check_edit_btn = true

                if(this.gender == "Female"){
                    this.gender = "F"
                }
                else{
                    this.gender = "M"
                }
            },

            updateChanges(){
                var headerObj = this.$store.state.headerObj
                headerObj["serviceName"] = "updateCustomerDetails"           
                var header = JSON.stringify(headerObj); 

                this.account_pin = headerObj["PIN"]
                // console.log(headerObj)

                var contentObj = {
                    Content:{}
                }
                
                contentObj.Content["familyName"] = this.familyName
                contentObj.Content["givenName"] = this.givenName
                contentObj.Content["dateOfBirth"] = this.dateOfBirth
                contentObj.Content["gender"] = this.gender
                contentObj.Content["occupation"] = this.occupation
                contentObj.Content["streetAddress"] = this.streetAddress
                contentObj.Content["city"] = this.city
                contentObj.Content["state"] = this.state
                contentObj.Content["country"] = this.country
                contentObj.Content["postalCode"] = this.postalCode
                contentObj.Content["emailAddress"] = this.emailAddress
                contentObj.Content["countryCode"] = this.countryCode
                contentObj.Content["mobileNumber"] = this.mobileNumber

                var content = JSON.stringify(contentObj);

                // if none of the contentobj.content is empty
                if(contentObj.Content["familyName"] !== "" && contentObj.Content["givenName"] !== "" && contentObj.Content["dateOfBirth"] !== "" && 
                    contentObj.Content["gender"] !== "" && contentObj.Content["occupation"] !== "" && contentObj.Content["streetAddress"] !== "" &&
                    contentObj.Content["city"] !== "" && contentObj.Content["state"] !== "" && contentObj.Content["country"] !== "" && 
                    contentObj.Content["postalCode"] !== "" && contentObj.Content["emailAddress"] !== "" && contentObj.Content["countryCode"] !== "" &&
                    contentObj.Content["mobileNumber"] !== "" && this.account_pin == this.pin){

                    this.axios.post("http://tbankonline.com/SMUtBank_API/Gateway?Header="+header+"&Content="+content).then((response)=>{
                        var data = response.data.Content.ServiceResponse
                        var errorcode = data.ServiceRespHeader.GlobalErrorID
                        if(errorcode == "010000"){
                            console.log(data)
                            this.modalActive = true
                            this.btnActive = true
                            this.modalMessage = "Profile updated successfully!"

                            this.$router.go(this.$router.currentRoute)
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
                    
                }
                else{
                    this.modalActive = true
                    this.modalMessage = "Invalid update. Please check your inputs again."
                    this.success = false;
                }
            },
        },
  
    }
  </script>
  
  <style>
  @media (min-width: 992px) {
        .pl-lg-4 {
            padding-left: 1.5rem !important;
        }
    }
  </style>