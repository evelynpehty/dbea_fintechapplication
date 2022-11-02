# dbea_fintechapplication
 
## backend
1. cd backend
2. python -m pip install Flask
3. python -m pip install yFinance
4. python -m pip install Flask-Cors
5. python -m pip install PyPortfolioOpt
6. python -m pip install pandas-datareader
7. python api.py

## frontend
1. cd frontend
2. npm install
3. npm install vue-multiselect@next
4. npm run serve

## login credentials [in case you forget your account credentials, you can use mine)
- userid: evelynpeh
- pin: 123123
- otp: 999999


## things to note
every tbank api require a Header as input 

for example: 
- headerObj = {'Header': 
                  {
                  'serviceName': serviceName,
                  'userID': userID,
                  'PIN': PIN,
                  'OTP': OTP
                  }
               }

Since userid, pin, otp does not change, these value has been coded to stored globally once they login 
the headerObj variable can be access globally by:
-  var headerObj = this.$store.state.headerObj
-  to change the servicename: headerObj["serviceName"] = "getCustomerStocks"           
