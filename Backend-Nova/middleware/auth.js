const jwt = require("jsonwebtoken")
require("dotenv").config()
const auth  =  async(req,res, next)=>{
    const token = req.header("Authorization");
    if(!token)return res.status(401).send("Not authorized")
   try {
    jwt.verify(token.split("Bearer ")[1], process.env.SECRET , (error, decodedToken)=>{
        if(error)throw new Error(error)
        req.user  = decodedToken;
    })
    next();
   } catch (error) {
    console.log(error);
    return res.status(400).send("Invalid token")
   }
}

module.exports = auth;