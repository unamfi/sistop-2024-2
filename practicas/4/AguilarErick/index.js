import os from "os";
import chalk from "chalk";
import gradient from "gradient-string";

let time = new Date();
setInterval(() => {
  console.clear();
  const totalMemory = os.totalmem();
  const freeMemory = os.freemem();
  const usedMemory = totalMemory - freeMemory;
  const percentUsed = (usedMemory / totalMemory) * 100;
  let progressBar = "";
  for (let i = 0; i < 100; i++) {
    progressBar += i < percentUsed ? chalk.bgRed(" ") : chalk.bgGreen(" ");
  }
  console.log(
    chalk.bold.blueBright("Total Memory:"),
    chalk.yellow((totalMemory / 1024 / 1024 / 1024).toFixed(2) + " GB")
  );
  console.log(
    chalk.bold.blueBright("Free Memory:"),
    chalk.yellow((freeMemory / 1024 / 1024 / 1024).toFixed(2) + " GB")
  );
  console.log(
    chalk.bold.blueBright("Used Memory:"),
    chalk.yellow((usedMemory / 1024 / 1024 / 1024).toFixed(2) + " GB")
  );
  console.log(
    chalk.bold.blueBright("Memory Usage:"),
    progressBar,
    percentUsed.toFixed(2) + "%"
  );
  const processMemoryUsage = process.memoryUsage().heapUsed;
  console.log(
    chalk.bold.blueBright("Process Memory Usage:"),
    gradient(
      "orange",
      "yellow"
    )((processMemoryUsage / 1024 / 1024).toFixed(2) + " kB")
  );
  time = new Date();
  console.log(
    chalk.bold.blueBright("System Time:"),
    chalk.green(time.toLocaleTimeString())
  );
}, 1000);
