const express = require("express")
const dotenv= require("dotenv");
const connectToDb = require("./utils/connection");
const swaggerUi = require("swagger-ui-express")
const swaggerDocument = require("./swagger.json");
const userRoute = require("./routes/userRoutes");
const app = express();
app.use(express.json())
dotenv.config()

connectToDb()
const port = process.env.PORT || 4000
app.listen(port, ()=>{
    console.log("The server running on port", port);
})


app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument))
app.use("/api/v1/users", userRoute)





