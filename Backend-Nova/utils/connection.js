const mongoose = require("mongoose")

const connectToDb = ()=>{
    mongoose.connect(process.env.MONGODB_URL).then(()=>console.log("Connected to the database successfully"))
    .catch(error=>{
        console.log(error);
    })
}

module.exports= connectToDb;