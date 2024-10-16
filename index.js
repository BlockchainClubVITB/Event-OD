import nodemailer from "nodemailer";

// const emails = [
//   "aryansharma_2022@vitbhopal.ac.in",
//   "agnibhachakraborty2022@vitbhopal.ac.in",
//   "harsh.23mim10152@vitbhopal.ac.in",
//   "omanshikaushal2022@vitbhopal.ac.in",
// ];

const email = "leonardofernandes2022@vitbhopal.ac.in";

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "blockchainclub@vitbhopal.ac.in",
    pass: "dgul wazj evka null",
  },
});

async function sendMail() {
  try {
    const info = await transporter.sendMail({
      from: "blockchainclub@vitbhopal.ac.in",
      to: email,
      subject: "Test email",
      text: "This is a test email",
    });
    console.log(info);
  } catch (error) {
    console.log(error);
  }
}

sendMail();
