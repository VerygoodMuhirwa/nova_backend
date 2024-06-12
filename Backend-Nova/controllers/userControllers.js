const User = require("../models/userModel");
const { hashPassword, comparePassword } = require("../utils/hashes");

const {
  validateSignupRequest,
  validateLoginRequest,
} = require("../utils/validation");

const signUp = async (req, res) => {
  try {
    const errors = await validateSignupRequest(req.body);
    if (errors.error)
      return res.status(400).json({ error: errors.error.message });

    const { username, email, password } = req.body;
    const userExists = await User.findOne({ email });
    console.log(userExists);
    if (userExists)
      return res
        .status(409)
        .json({ message: "The user witht that email already exists" });
    const hashedPassword = await hashPassword(password, 10);
    const user = await User.create({
      username,
      email,
      password: hashedPassword,
    });
    if (!user) return res.status(400).json({ message: "faced an error " });
    return res.status(201).json({ message: "User created successfully" });
  } catch (error) {
    console.log(error);
    return res.status(500).send("Internal server error");
  }
};

const login = async (req, res) => {
  try {
    const errors = await validateLoginRequest(req.body);
    if (errors.error) return res.status(400).json({ error: errors.error.message });
    const { email, password } = req.body;
    const userExists = await User.findOne({ email });
    if (!userExists)
      return res.status(404).json({ message: "Invalid email or password" });
    const passwordMatches = await comparePassword(password, userExists.password);
    if (!passwordMatches)
      return res.json({ message: "Invalid password" }).status(404);
    return res
      .status(200)
      .json({
        message: "User logged in successfully",
        token: userExists.generateAuthToken(),
      });
  } catch (error) {
    console.log(error);
    return res.status(500).send("Internal server error");
  }
};

module.exports = { signUp, login };
