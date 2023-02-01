// ==UserScript==
// @name         Amazon review collector
// @namespace    https://www.amazon.com
// @version      0.2
// @description  Development stuff
// @author       themysticsavages
// @icon         https://www.google.com/s2/favicons?sz=64&domain=tampermonkey.net
// @match        https://www.amazon.com/*/product-reviews/*
// @run-at       document-end
// ==/UserScript==

(async function () {
  var params = new URLSearchParams(window.location.search);
  var chunked = true;

  if (params.get("pageNumber") === null) {
    throw new Error(
      "[arc] Page number not specified, define a page start and page end with ?pageNumber=2&pageMacro=5"
    );
  }
  if (params.get("pageMacro") === null) {
    throw new Error(
      "[arc] Pages to index were not specified, define a page start and page end with ?pageNumber=2&pageMacro=5"
    );
  }
  if (params.get("noChunk") !== null) {
    console.info("[arc] Chunking is disabled by ?noChunk");
    chunked = false;
  } else {
    console.info("[arc] Chunking is enabled. This can be disabled with ?noChunk");
  }

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

  var added = [...JSON.parse(await localStorage.getItem("elements")), elements];
  await localStorage.setItem("elements", JSON.stringify(added));

  var pageNumber = parseInt(params.get("pageNumber"));
  if (pageNumber === parseInt(params.get("pageMacro"))) {
    var dimCSS = `#dimScreen {
      position: fixed;
      padding: 0;
      margin: 0;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.5);
    }`
    var messageCSS = `#message {
      position: fixed;
      top: 50%;
      right: 50%;
      transform: translate(50%,-50%);
      background: #131921;
      color: white;
      padding: 10px;
      overflow-y: auto;
      width: 50%;
      height: 50%;
      z-index: 3;
    }
    #ajson {
      background-color: #232F3E;
      padding: 5px;
      margin-top: 10px;
    }
    #abutton {
      border: none;
      padding: 5px;
      background-color: #232F3E;
      color: white;
    }
    #abutton:hover { background-color: #304054; }
    `
    var copyScript = 'navigator.clipboard.writeText(document.querySelector("#ajson").innerText).then(() => alert("Copied"))'
    var closeScript = 'document.querySelector("#dimScreen").remove(); document.querySelector("#message").remove()'

    document.head.insertAdjacentHTML("beforeend", `<style>${dimCSS}</style>`)
    document.head.insertAdjacentHTML("beforeend", `<style>${messageCSS}</style>`)
    document.body.insertAdjacentHTML("beforeend", "<div id='dimScreen'></div>")
    document.body.insertAdjacentHTML("beforeend",
      `<div id='message'><h2>Here's that stuff you wanted</h2><button id='abutton' onclick='${copyScript}'>Copy JSON</button>&nbsp;&nbsp;<button id='abutton' onclick='${closeScript}'>Close</button>
      <br><pre id='ajson' style='white-space: pre-wrap;'>${JSON.stringify(
      chunked
        ? chunk((await JSON.parse(localStorage.getItem("elements"))).flat(Infinity), 5)
        : (await JSON.parse(localStorage.getItem("elements"))).flat(Infinity)
    )}</pre></div>`);
    await localStorage.setItem("elements", JSON.stringify([]));
    throw new Error("[]");
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
