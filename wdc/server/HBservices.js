/*
File: HBservices.js
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
var count1 = 1;
var count2 = 1;

var helpers = {
  counter1: function () {
    return count1++;
  },
  counter2: function () {
    return count2++;
  },

  tc: function (aString) {
    return aString[0].toUpperCase() + aString.substr(1).toLowerCase();
  },
  uc: function (aString) {
    return aString.toUpperCase();
  },
  p: function (aString) {
    return aString.substr(1);
  },
  rd: function (aString) {
    return aString.toString().replace("$", "-");
  },
  deldq: function (aString) {
    return aString
      .toString()
      .replace(/\\/,"\\\\")
      .replaceAll(/"/g, `\\"`)
      .replaceAll(/\\&quot;/g, ``)
      .replaceAll(/\\\//g, ` `);
  },
  ifEquals: function (arg1, arg2, options) {
    return arg1 == arg2 ? options.fn(this) : options.inverse(this);
  },
  dataValue: function (arg) {
    if (!arg || !arg.type) return '"unknown value"';
    if (arg.type == "wikibase-entityid") return "wd:" + arg.value.id;
    if (arg.type == "monolingualtext")
      return (
        '"' +
        arg.value.text
          .toString()
          .replace(/\\/,"\\\\")
          .replace(/"/g, `\\"`)
          .replace(/\\\//g, ` `)
          .replaceAll(/\\&quot;/g, `"`) +
        '"@' +
        arg.value.language
      );
    if (arg.type == "string")
      return (
        '"' +
        arg.value
          .toString()
          .replace(/\\/,"\\\\")  /* replaces last occurrence of \ */
          .replace(/"/g, `\\"`)
          .replace(/\\\//g, ` `)
          .replaceAll(/\\&quot;/g, `"`) +
        '"'
      );
    if (arg.type == "time")
      { if (arg.value.time.substr(1).includes('-00-00T00:00:00Z'))
        return '"' + arg.value.time.substr(1).replace('-00-00T00:00:00Z', '-01-01T00:00:00Z') + '"^^xsd:dateTime'; 
      else if (arg.value.time.substr(1).includes('-00T00:00:00Z'))
        return '"' + arg.value.time.substr(1).replace('-00T00:00:00Z', '-01T00:00:00Z') + '"^^xsd:dateTime';
      else 
        return '"' + arg.value.time.substr(1) + '"^^xsd:dateTime';
      }
    if (arg.type == "quantity")
      return '"' + arg.value.amount + '"^^xsd:decimal';
    if (arg.type == "globecoordinate")
      return (
        '"Point(' +
        arg.value.longitude +
        " " +
        arg.value.latitude +
        ')"^^geo:wktLiteral'
      );
    return arg.value + "   # WARNING Unmanaged value";
  },
  dataValueRDFStar: function (arg) {
    if (!arg || !arg.type) return '"unknown value"';
    if (arg.type == "wikibase-entityid") return "wd:" + arg.value.id;
    if (arg.type == "monolingualtext")
      return (
        '"' +
        arg.value.text
          .replace(/\\/,"\\\\")
          .replaceAll(/"/g, `\\"`)
          .replaceAll(/\\\//g, ` `)
          .replaceAll(/&quot;/g, `"`) +
        '"'
      );
    if (arg.type == "string")
      return (
        '"' +
        arg.value
          .replace(/\\/,"\\\\")
          .replaceAll(/"/g, `\\"`)
          .replaceAll(/\\\//g, ` `)
          .replaceAll(/&quot;/g, `"`) +
        '"'
      );
    if (arg.type == "time")
      return '"' + arg.value.time.substr(1) + '"^^xsd:dateTime';
    if (arg.type == "quantity")
      return '"' + arg.value.amount + '"^^xsd:decimal';
    if (arg.type == "globecoordinate")
      return (
        '"Point(' +
        arg.value.longitude +
        " " +
        arg.value.latitude +
        ')"^^geo:wktLiteral'
      );
    return arg.value + "   # WARNING Unmanaged value";
  },
	'allNormals': function(arg) { 
		for (var i in arg) {
			if (arg[i].rank !== 'normal')
				return false
		}
		return true
	},
	'hasDeprecated': function(arg) { 
		for (var i in arg) {
			if (arg[i].rank == 'deprecated')
				return true
		}
		return false
	},
	'hasPreferred': function(arg) { 
		for (var i in arg) {
			if (arg[i].rank == 'preferred')
				return true
		}
		return false
	},
	'isDeprecated': function(arg) { return arg.rank == 'deprecated' },
	'isNormal': function(arg) { return arg.rank == 'normal' },
	'isPreferred': function(arg) { return arg.rank == 'preferred' }
};

function filterLanguages(items, languages, strict = false) {
  var residuals = {};
  var r = 0;
  for (var o in items) {
    if (Array.isArray(items[o])) {
      var x = filterLanguages(items[o], languages, true);
      if (x) {
        residuals[o] = x;
        r++;
      }
    } else if (languages.indexOf(items[o].language) !== -1) {
      residuals[o] = items[o];
      r++;
    }
  }
  return r > 0 ? residuals : strict ? null : items;
}

(function (exports) {
  (exports.helpers = helpers), (exports.filterLanguages = filterLanguages);
})(typeof exports === "undefined" ? (window["HBservices"] = {}) : exports);
