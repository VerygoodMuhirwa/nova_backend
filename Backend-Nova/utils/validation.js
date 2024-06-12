
const Joi = require("joi")

const validateSignupRequest = async(req)=>{
    const schema = Joi.object({
        username: Joi.string().required(),
        email: Joi.string().email().required(),
        password: Joi.string().min(4).required(),
    })
    return schema.validate(req);
}


const validateLoginRequest = async(req)=>{
    const schema = new Joi.object({
        email: Joi.string().email().required(),
        password: Joi.string().min(4).required(),
    })
   return schema.validate(req)
}


module.exports = {validateSignupRequest, validateLoginRequest}
