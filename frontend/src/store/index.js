import { createStore } from 'vuex'

import createPersistedState from "vuex-persistedstate";

export default createStore({
  plugins: [createPersistedState(
    {storage: window.sessionStorage}
  )],
  state: {
    headerObj:{
        userID: null,
        PIN: null,
        OTP:null
    }
    
  },
  mutations:{
    reset(state){
      state.headerObj.PIN = null
      state.headerObj.OTP =null
      state.headerObj.userID=null
    },
    setHeaderObj(state, data) {     
      state.headerObj.userID = data["userID"];
      state.headerObj.PIN = data["PIN"];
      state.headerObj.OTP = data["OTP"];
    },
  },
  actions: {
   

  },
  modules: {

  }
})
