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
      html: `<p>Dear Blockchain Enthusiast,</p>,
          <p>The future of blockchain is calling—and your exclusive entry is just an attachment away!</p>,
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
    console.log(`Email sent to ${email}: ${info.response}`);
  } catch (error) {
    console.log(`Error sending email to ${email}: ${error}`);
  }
}

function readCSVAndSendEmails() {
  const results = [];
  fs.createReadStream('data.csv')
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', () => {
      const chunks = [];
      for (let i = 0; i < results.length; i += 50) {
        chunks.push(results.slice(i, i + 50));
      }

      chunks.forEach((chunk, index) => {
        setTimeout(() => {
          chunk.forEach(row => {
            const email = row.Email;
            const registrationNumber = row.Registration.trim();
            sendMail(email, registrationNumber);
          });
        }, index * 60000); // 1 minute interval between chunks
      });
    });
}

readCSVAndSendEmails();