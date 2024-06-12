const mongoose = require("mongoose")
const jwt = require("jsonwebtoken")
const userSchema = new mongoose.Schema({
    username:{
        type:String,
        required:true
    },
    email:{
        type:String,
        unique:true,
        required:true
    },
    password:{
        type:String,
        required:true
    },

    pic: {
        type: String,
        default:
          "https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg",
      },
},{timestamps:true});

userSchema.methods.generateAuthToken= function(){
    return jwt.sign({
        _id:this._id,
        email:this.email,
        role:"USER"
    }, process.env.SECRET)
}
    

const User = mongoose.model("User", userSchema);
module.exports = User;
