/*
File: wdc.js
Author: Fabio Vitali
Version: 1.0 
Last change on: 18 april 2022


Copyright (c) 2021 by Fabio Vitali

   Permission to use, copy, modify, and/or distribute this software for any
   purpose with or without fee is hereby granted, provided that the above
   copyright notice and this permission notice appear in all copies.

   THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
   WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
   MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
   SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
   WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
   OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
   CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

*/

/*

Inside main node file add: 

const wdc = require('wdc.js') ; 

app.post('/wdconvert', async function(req, res) { 
	wdc.convert(req,res)
});

use npm to install
- handlebars
- adm-zip
multer


*/

const HBservices = require("./HBservices.js");
const Handlebars = require("handlebars");
const AdmZip = require("adm-zip");
const fs = require("fs");
const fsp = fs.promises;
const multer = require("multer");

var path = require("path");
global.rootDir = path.resolve(__dirname);

// var tmpDir = "/public/wdc/" ;
const base = global.rootDir + "/uploads/";
const temporaryDirPrefix = "wdc-";
const uploadFileName = "docFile";
const uploadTemplateName = "t";
const outputSuffix = ".ttl";
const zipSuffix = "-converted.zip";
const languages = ["en"];

for (var i in HBservices.helpers) {
  Handlebars.registerHelper(i, HBservices.helpers[i]);
}

exports.convert = async function (req, res) {
  let tmpDir =
    fs.mkdtempSync(base + temporaryDirPrefix, { recursive: true }) + "/";
  fs.chmodSync(tmpDir, 0o775);

  //	const upload = multer({ dest: tmpDir })
  //	let middleware = upload.single('docFile')

  const middleware = multer({ dest: tmpDir }).single(uploadFileName);
  middleware(req, res, async () => doConvert(req, res, tmpDir));
};

doConvert = async function (req, res, dir) {
  let tmpPath = "";
  let filename = [];
  let outputZipFilename = req.file.originalname.split(".")[0] + zipSuffix;

  let err = "";
  let outputs = [];

  var templates = JSON.parse(req.body[uploadTemplateName]);
  var zip = new AdmZip(req.file.path);
  var zipEntries = zip.getEntries();

  console.log(
    "wdcConvert on file " +
      req.file.originalname +
      " with " +
      templates.length +
      " templates."
  );
  let beforeEntries = async function () {
    for (var j in templates) {
      filename[j] = templates[j].fn + outputSuffix;
      outputs[j] = await fsp.open(dir + filename[j], "a");
      templates[j].exec = await Handlebars.compile(templates[j].template);
      console.log(JSON.stringify(templates, null, 2));
    }
  };
  let eachEntry = function (entry) {
    return new Promise(async function (resolve, reject) {
      try {
        console.log("Entry: " + entry.entryName);
        let data = JSON.parse(zip.readAsText(entry));
        for (var j in templates) {
          let converted = "";
          for (var i in data.entities) {
            let entity = cleanUp(data.entities[i]);
            converted += templates[j].exec(entity);
          }
          await outputs[j].write(converted);
          console.log(
            Object.keys(data.entities).length +
              " entities converted in " +
              templates[j].fn +
              " from " +
              entry.entryName
          );
        }
      } catch (e) {
        console.log("Error in " + entry.entryName + ": " + e.message);
        err += "Error in " + entry.entryName + ": " + e.message + "\n";
      }
      resolve();
    });
  };

  let afterEntries = async function () {
    try {
      let outputZip = new AdmZip();
      for (var j in templates) {
        await outputs[j].close();
        await outputZip.addLocalFile(dir + filename[j]);
      }
      await outputZip.writeZip(dir + outputZipFilename);
      console.log("Zip file " + outputZipFilename + " saved.");
      setTimeout(() => {
        fs.rmSync(dir, { recursive: true, force: true });
        console.log("Temporary directory " + dir + " removed.");
      }, 10000);
      res.header("Access-Control-Expose-Headers", "*");
      res.download(dir + outputZipFilename);
    } catch (e) {
      res.send(JSON.stringify(e));
      console.log(
        "Error in clearing temporary directory " + dir + ": " + e.message
      );
    }
  };

  await beforeEntries();
  let promises = zipEntries.map(eachEntry);
  Promise.all(promises).then(afterEntries);
};

function cleanUp(e) {
  var ret = JSON.parse(JSON.stringify(e));
  ret.labels = HBservices.filterLanguages(ret.labels, languages);
  ret.descriptions = HBservices.filterLanguages(ret.descriptions, languages);
  ret.aliases = HBservices.filterLanguages(ret.aliases, languages, true);
  return ret;
}
