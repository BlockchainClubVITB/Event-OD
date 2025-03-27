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
      subject: "A Milestone Achieved – Your Journey at PokéBlock Quest, AdVITya 2025",
      html: `<p>Dear Blockchain Enthusiast,</p>
          <p>Your participation in <b>PokéBlock Quest</b> at <b>AdVITya 2025</b> was nothing short of remarkable. This wasn’t just another <b>Capture The Flag</b> challenge—it was a test of logic, problem-solving, and determination, and you took it head-on.</p>
          <p>Every puzzle you cracked and every challenge you solved added to an electrifying competition. Whether you emerged at the top or pushed your limits, you are now part of an elite group that dared to take on this unique Pokémon-themed CTF experience.</p>
          <p>Enclosed is your official recognition of participation—a testament to your initiative and technical acumen. We encourage you to share this milestone on social media and tag us using <b>#BlockchainClubVITB #PokéBlockQuest #AdVITya2025 #VITBhopal</b>.</p>
          <p>Let’s stay connected for even bigger challenges ahead:</p>
          <p>LinkedIn: <a href="https://linkedin.com/company/blockchain-club-vitb/"><b>https://linkedin.com/company/blockchain-club-vitb/</b></a></p>
          <p>Instagram: <a href="https://instagram.com/blockchain.vitb/"><b>https://instagram.com/blockchain.vitb/</b></a></p>
          <p>X (Twitter): <a href="https://x.com/blockchainvitb"><b>https://x.com/blockchainvitb</b></a></p>
          <p>YouTube: <a href="https://youtube.com/@blockchainclubvitb"><b>https://youtube.com/@blockchainclubvitb</b></a></p>
          <p>WhatsApp Community: <a href="https://chat.whatsapp.com/KI3mnptIqiR6gTgv0grRJG"><b>https://chat.whatsapp.com/KI3mnptIqiR6gTgv0grRJG</b></a></p>
          <p>This is just the beginning. Stay tuned for what’s next.</p>
          <p>Best Regards,</p>
          <p>Blockchain Club<br>
          VIT Bhopal University</p>`,
      attachments: [
        {
          filename: `${registrationNumber}.png`,
          path: `./certificates2/${registrationNumber}.png`,
        },
      ],
    });
    fs.appendFileSync("log.txt", `Email sent to ${email}: ${info.response}\n`);
  } catch (error) {
    fs.appendFileSync("log.txt", `Error sending email to ${email}: ${error}\n`);
  }
}

function readCSVAndSendEmails() {
  const results = [];
  fs.createReadStream("data.csv")
    .pipe(csv())
    .on("data", (data) => results.push(data))
    .on("end", () => {
      let delay = 0;
      results.forEach((row, index) => {
        setTimeout(() => {
          const email = row.Email;
          const registrationNumber = row.Registration.trim();
          sendMail(email, registrationNumber);
        }, delay);
        delay += 20000;
      });
    });
}

readCSVAndSendEmails();
