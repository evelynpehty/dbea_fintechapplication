<template>
  <UserNavigation v-if="show==1" />
  <MainNavigation v-else />
  <router-view></router-view>
  
</template>

<script>


import MainNavigation from "./components/MainNavigation";
import UserNavigation from "./components/UserNavigation.vue";
export default {
  name: 'App',
  components: {
    MainNavigation,
    UserNavigation
},
computed:{
  show(){
    if(this.$store.state.headerObj.userID){
      return 1
    }
      return 0
  }
}
}
</script>

<style>
@font-face {
font-family: "ProductSansRegular";
src: url("assets/fonts/Product-Sans-Regular.ttf");
}

@font-face {
font-family: "ProductSansBold";
src: url("assets/fonts/Product-Sans-Bold.ttf");
}

@font-face {
font-family: "ProductSansItalic";
src: url("assets/fonts/Product-Sans-Italic.ttf");
}

@font-face {
font-family: "ProductSansBoldItalic";
src: url("assets/fonts/Product-Sans-Bold-Italic.ttf");
}

:root {
  --purple: #6018F1;
  --light-purple: #EBE4FD;
  --blue : #5FD4E1;
  --white: #ffffff;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'ProductSansBold', Arial, sans-serif !important;
  color: var(--purple);
}
thead{
    background-color: var(--purple)
}
th{
    color:white
}


div {
  font-family: 'ProductSansRegular', Arial, Helvetica, sans-serif;
}

body {
  padding-top: 4.5rem;
}


.btn-success {
  background-color: var(--purple) !important;
  border-color: var(--purple) !important;
}

.btn-outline-success {
  color: var(--purple) !important;
  border: 1px solid var(--purple) !important
}

.btn-outline-success:hover {
  color: white !important;
  background-color: var(--purple) !important;
}

.input-group-text {
  background-color: #afafef !important;
  color: var(--purple) !important;
}

.input-border-color {
  border: 1px solid #afafef !important;
}

.input-border-color:focus {
  outline: none !important;
  border:1px solid #afafef !important;
  box-shadow: 0 0 10px #afafef !important;
}

.multiselect__tags {
  border: 1px solid #afafef !important;
}

.multiselect__tag {
  background: var(--purple) !important;
}

.multiselect__option--highlight {
  background: #EAE6E4 !important;
  color: black !important;
}

.multiselect__tag-icon:after {
    color: white !important;
}

</style>
