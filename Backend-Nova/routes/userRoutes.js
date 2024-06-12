const express = require('express');
const auth = require("../middleware/auth")
const admin = require("../middleware/admin")
const userControllers = require("../controllers/userControllers")
const userRoute = express.Router()
// userRoute.get("/authenticate", [auth,admin], userControllers.authentiated)
userRoute.post("/register", userControllers.signUp )
userRoute.post("/login", userControllers.login)
// userRoute.delete("/:id", userControllers.deleteUser)
// userRoute.put("/:id", userControllers.updateUser)
// userRoute.get("/getUsers", userControllers.getAllUsers)
module.exports = userRoute