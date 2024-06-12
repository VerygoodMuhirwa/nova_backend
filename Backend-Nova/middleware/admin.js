
const admin = async(req,res,next)=>{
    if(!req.user.role =="USER")return res.send.status(200).send("Not authorized");
    next();
}

module.exports =admin