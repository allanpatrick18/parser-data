const PORT = 8000
const axios = require('axios');
const url = 'https://postman-echo.com/get?foo1=bar1&foo2=bar2'
const express = require('express')
const cors = require('cors')

const app = express()
app.use(cors())

app.get('/', (req, res)=> {
  res.json("test web")
})

app.get('/echo', (req, res)=>{
axios.get(url)
  .then(function (response) {
    console.log(response.data);
    res.json(response.data)
  }).catch(function (error) {
    console.log(error);
  })
})



app.listen(PORT, () => {
  console.log(`The app  is listening on port ${PORT}`)
})