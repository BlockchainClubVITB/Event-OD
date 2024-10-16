import nodemailer from "nodemailer";
import fs from "fs";
import csv from "csv-parser";

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "blockchainclub@vitbhopal.ac.in",
    pass: "dgul wazj evka null",
  },
});

async function sendMail(email, registrationNumber) {
  try {
    const info = await transporter.sendMail({
      from: "blockchainclub@vitbhopal.ac.in",
      to: email,
      subject: "Your Ticket to Blockchain Mastery: Blockchain Internships, Jobs and a Sustainable Future for the Next 10 Years!!",
      html: `<p>Dear Blockchain Enthusiast,</p>
          <p>The future of blockchain is calling—and your exclusive entry is just an attachment away!</p>
          <p> In just a few hours, we’ll dive deep into Unlocking ₹30 LPA+ Internships, Jobs, and a Sustainable Future with Blockchain, followed by an exciting hands-on session tomorrow, 17th October.</p>
          <p>What’s in store?</p>
        
          <p>Deploy your own smart contract with real-time guidance. </p>

          <p>Earn an official certificate to showcase your new skills. </p>

          <p>Explore top opportunities in the blockchain space. </p>
          
          <p>Don’t forget to bring your laptop—it’s your key to fully participating and deploying your own smart contract in the session. </p>

          <p>Ticket Alert: Your attached ticket only grants you entry to this event.  </p>

          <p>See you soon, </p>

          <p>Blockchain Club, </p>

          <p>VIT Bhopal University</p>`,
      attachments: [
        {
          filename: `${registrationNumber}.png`,
          path: `./qrcodes/${registrationNumber}.png`,
        },
      ],
    });
    fs.appendFileSync('log.txt', `Email sent to ${email}: ${info.response}\n`);
  } catch (error) {
    fs.appendFileSync('log.txt', `Error sending email to ${email}: ${error}\n`);
  }
}

function readCSVAndSendEmails() {
  const results = [];
  fs.createReadStream('data3.csv')
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', () => {
      let delay = 0;
      results.forEach((row, index) => {
        setTimeout(() => {
          const email = row.Email;
          const registrationNumber = row.Registration.trim();
          sendMail(email, registrationNumber);
        }, delay);
        delay += 20000; // 20 seconds delay
      });
    });
}


readCSVAndSendEmails();