const wdc = require("./server/wdc.js");
const express = require("express");
const app = express();
bodyParser = require("body-parser");
var path = require("path");
const port = 3000;

app.set("views", path.join(__dirname, "views"));
app.engine("html", require("ejs").renderFile);
app.set("view engine", "html");
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.render("index");
});

app.post("/wdconvert", async (req, res) => {
  wdc.convert(req, res);
});

app.listen(port, () => {
  console.log(`App running on port ${port}!`);
});
