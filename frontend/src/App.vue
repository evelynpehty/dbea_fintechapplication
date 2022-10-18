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
font-family: "ShareFontRegular";
src: url("assets/fonts/share.regular.ttf");
}

@font-face {
font-family: "ShareFontItalic";
src: url("assets/fonts/share.italic.ttf");
}

@font-face {
font-family: "ShareFontBold";
src: url("assets/fonts/share.bold.ttf");
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'ShareFontBold', Arial, sans-serif !important;
  color: #000080;
}
thead{
    background-color: #000080
}
th{
    color:white
}


div {
  font-family: 'ShareFontRegular', Arial, Helvetica, sans-serif;
}

body {
  padding-top: 4.5rem;
}


.btn-success {
  background-color: #000080 !important;
  border-color: #000080 !important;
}

.btn-outline-success {
  color: #000080 !important;
  border: 1px solid #000080 !important
}

.btn-outline-success:hover {
  color: white !important;
  background-color: #000080 !important;
}

.input-group-text {
  background-color: #afafef !important;
  color: #000080 !important;
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
  background: #000080 !important;
}

.multiselect__option--highlight {
  background: #EAE6E4 !important;
  color: black !important;
}

.multiselect__tag-icon:after {
    color: white !important;
}

</style>
