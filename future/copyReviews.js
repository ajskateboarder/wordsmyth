// ==UserScript==
// @name         Amazon review collector
// @namespace    https://www.amazon.com
// @version      0.1
// @description  Development stuff
// @author       themysticsavages
// @icon         https://www.google.com/s2/favicons?sz=64&domain=tampermonkey.net
// @match        https://www.amazon.com/*/product-reviews/*
// @match        https://html.duckduckgo.com/html/
// @run-at       document-end
// @grant        GM_getValue
// @grant        GM_setValue
// ==/UserScript==

(async function () {
  var chunk = (arr, len) => {
    var chunks = [],
      i = 0,
      n = arr.length;

    while (i < n) {
      chunks.push(arr.slice(i, (i += len)));
    }
    return chunks;
  };

  var elements = [];

  document
    .querySelectorAll("span[data-hook='review-body']")
    .forEach((element) =>
      elements.push(element.textContent.replace(/(\r\n|\n|\r)/gm, "").trim())
    );

  var added = [...(await GM_getValue("elements")), elements];
  await GM_setValue("elements", added);

  var pageNumber = parseInt(
    new URLSearchParams(window.location.search).get("pageNumber").toString()
  );
  if (pageNumber === 5) {
    document.body.innerHTML = JSON.stringify(
      // this is for optimal performance when using with the algorithms
      chunk((await GM_getValue("elements")).flat(Infinity), 5)
    );
    await GM_setValue("elements", []);
    throw new Error("Hello world");
  }
  setTimeout(
    () =>
      (window.location = window.location.href.slice(0, -1) + (pageNumber + 1)),
    1000
  );
})();
