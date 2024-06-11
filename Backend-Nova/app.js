const express = require("express")
const dotenv= require("dotenv")
const app = express();
dotenv.config()


const port = process.env.PORT || 4000
app.listen(port, ()=>{
    console.log("The server running on port", port);
})