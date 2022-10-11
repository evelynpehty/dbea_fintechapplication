<template>
    <Loading v-show="loading" />
    <Modal v-if="modalActive" :modalMessage="modalMessage" v-on:close-modal="closeModal"/>
  </template>
  
  <script>
import Loading from "../components/Loading";
import Modal from "../components/Modal";
export default {
        name: "LoginPage",
        components: {Loading, Modal},
        data() {
            return {
                loading: null,
                modalMessage: null,
                modalActive: null,

                success:false
            };
        },
        created(){
    
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