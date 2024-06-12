const bcrypt = require("bcrypt")
const hashPassword = async(password, salt)=>{
    return await bcrypt.hash(password, salt)
}

const comparePassword=(reqPassword,storedPassword)=>{
   return bcrypt.compare(reqPassword, storedPassword);
}

module.exports = {hashPassword, comparePassword}