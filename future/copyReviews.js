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
  var params = new URLSearchParams(window.location.search);
  var chunked = true;

  if (params.get("pageNumber") === null) {
    throw new Error(
      "ARC: Page number not specified, define a page start and page end with ?pageNumber=2&pageMacro=5"
    );
  }
  if (params.get("pageMacro") === null) {
    throw new Error(
      "ARC: Pages to index were not specified, define a page start and page end with ?pageNumber=2&pageMacro=5"
    );
  }
  if (params.get("noChunk") !== null) {
    console.log("ARC: Chunking is disabled by ?noChunk");
    chunked = false;
  } else
    console.log("ARC: Chunking is enabled. This can be disabled with ?noChunk");

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

  var pageNumber = parseInt(params.get("pageNumber"));
  if (pageNumber === parseInt(params.get("pageMacro"))) {
    document.body.innerHTML = JSON.stringify(
      chunked
        ? chunk((await GM_getValue("elements")).flat(Infinity), 5)
        : (await GM_getValue("elements")).flat(Infinity)
    );
    await GM_setValue("elements", []);
    throw new Error("Hello world");
  }
  params.set("pageNumber", pageNumber + 1);
  setTimeout(
    () =>
      (window.location = `${location.protocol}//${location.host}${
        location.pathname
      }?${params.toString()}`),
    1000
  );
})();
