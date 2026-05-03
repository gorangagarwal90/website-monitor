const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  let report = "";

  try {
    await page.goto("https://drytechgeofoam.in/", { waitUntil: "networkidle2" });

    await page.type("input[name='your-name']", "Test User");
    await page.type("input[name='your-phone']", "9999999999");

    await page.click("input[type='submit']");

    await page.waitForSelector(".wpcf7-response-output", { timeout: 10000 });

    report = "✅ Form working on drytechgeofoam.in";

  } catch (err) {
    report = "❌ Form FAILED on drytechgeofoam.in";
  }

  console.log(report);

  await browser.close();
})();
