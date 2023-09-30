<script lang="ts">
  import { getClient, ResponseType } from "@tauri-apps/api/http";
  import { platform } from "@tauri-apps/api/os";
  import { invoke } from "@tauri-apps/api/tauri";
  import {
    writeBinaryFile,
    type BinaryFileContents,
    exists,
  } from "@tauri-apps/api/fs";
  import { appWindow } from "@tauri-apps/api/window";

  import Modal from "./lib/Modal.svelte";
  import Product from "./lib/Product.svelte";
  import RatingBar from "./lib/RatingBar.svelte";

  import { email, password, ProductHandler } from "./stores";
  import { notify } from "./alert";

  let showModal = false;
  let validPass = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($email);

  $: {
    const emailValue = localStorage.getItem("email");
    if (emailValue !== null) {
      email.set(emailValue);
    }
    const passwordValue = localStorage.getItem("password");
    if (passwordValue !== null) {
      password.set(passwordValue);
    }
    if (showModal === true) {
      validPass = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($email);
      (document.querySelector(".submit") as HTMLButtonElement).disabled =
        validPass;
    }
  }

  email.subscribe((value) => {
    localStorage.setItem("email", value);
  });
  password.subscribe((value) => {
    localStorage.setItem("password", value);
  });

  let browser: WebSocket;
  let model: WebSocket;

  async function getLatestRelease(): Promise<string[]> {
    const client = await getClient();
    const response = await client.get(
      "https://api.github.com/repos/ajskateboarder/river/releases/latest",
      {
        headers: { "User-Agent": "bot" },
        timeout: 30,
        responseType: ResponseType.JSON,
      }
    );
    const downloadLinks = (response.data as Record<string, any>).assets.map(
      (item: any) => item.browser_download_url
    );
    return downloadLinks;
  }

  async function downloadEXE(url: string) {
    const client = await getClient();
    return (
      await client.get(url, {
        headers: { "User-Agent": "bot" },
        timeout: 30,
        responseType: ResponseType.Binary,
      })
    ).data as BinaryFileContents;
  }

  let message = ``;
  let url = "";
  let reviews: Response[] = [];
  let isLatestDone: "not triggered" | "triggered" | "done" = "not triggered";

  $: asin = (() => {
    let _path = url.split("/");
    if (_path[_path.length - 1].includes("?")) {
      return _path[_path.length - 2];
    }
    if (_path[0] !== "https:") {
      return url;
    }
    return _path[_path.length - 1];
  })();

  type Response = {
    type: "status" | "response";
    message?: string;
    reviewText: string;
    overall: number;
    productId: string;
    title: string;
    image: string;
    rating: string;
  };

  function doAnalysis() {
    model = new WebSocket("ws://localhost:8002");
    let toAnalyze = ProductHandler.read(asin)?.reviews as any[];
    model.onmessage = (e) => {
      let analyzed = ProductHandler.saveAnalysis(asin, JSON.parse(e.data));
      message = `${analyzed.length}/${
        reviews?.length
      } reviews analyzed <progress max="100" value="${
        (analyzed.length / toAnalyze.length) * 100
      }"></progress>`;
      if (analyzed.length === toAnalyze.length) {
        message = "";
        isLatestDone = "done";
      }
    };
    model.onopen = () => {
      toAnalyze.forEach((message) => model.send(message.reviewText));
    };
  }

  function scrapeData() {
    try {
      browser.close();
      model.close();
    } catch {}
    browser = new WebSocket("ws://localhost:8001");
    isLatestDone = "triggered";
    let reviews;
    browser.onmessage = (e) => {
      let data: Response = JSON.parse(e.data);
      if (data.type === "status") {
        if (data.message === "Logging in...") {
          notify({
            message: "Logging scraper into Amazon... this may take sometime",
            closable: true,
            duration: Infinity,
          });
          return;
        }
        if (data.message === "Logging in done") {
          try {
            document.querySelectorAll("sl-alert").forEach((e) => e.remove());
          } catch {}
          return;
        }
        message = data.message as string;
        if (data.message === "Scraping done") {
          browser.close();
          products = ProductHandler.fetchProducts();
          setTimeout(doAnalysis, 1000);
        }
      } else if (data.type === "response") {
        reviews = ProductHandler.saveReview(asin, data);
        message = `${reviews.length} reviews collected`;
      } else if (data.type === "response_product") {
        ProductHandler.saveProductInfo(asin, data);
        products = ProductHandler.fetchProducts();
      }
    };
    browser.onopen = () => {
      browser.send(
        JSON.stringify({
          command: "login",
          username: $email,
          password: $password,
        })
      );
      if (localStorage.getItem(asin) !== null) {
        localStorage.removeItem(asin);
        products = ProductHandler.fetchProducts();
      }
      browser.send(JSON.stringify({ command: "scrape", asin: asin }));
    };
  }

  (async () => {
    if ((await platform()) === "linux") {
      if (!(await exists("river"))) {
        notify({ message: "Downloading Amazon scraper..." });
        let links = await getLatestRelease();
        const linuxBinary = await downloadEXE(links[0]);
        await writeBinaryFile("river", linuxBinary);
      }
      await invoke("run_river");
    } else if ((await platform()) === "win32") {
      if (await exists("river.exe")) {
        return;
      }
      let links = await getLatestRelease();
      const linuxBinary = await downloadEXE(links[0]);
      await writeBinaryFile("river", linuxBinary);
      await invoke("run_river");
    }
  })();

  const average = (array: number[]) =>
    array.reduce((a, b) => a + b) / array.length;

  (async function () {
    document.body.classList.add(`${await appWindow.theme()}-mode`);
  })();

  let products = ProductHandler.fetchProducts();
  const modalStates = Array(products.length).fill(false);
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.8.0/cdn/themes/light.css"
  />
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.8.0/cdn/themes/dark.css"
  />
  <script
    type="module"
    src="https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.8.0/cdn/shoelace.js"
  ></script>
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.1/css/fontawesome.min.css"
  />
</svelte:head>

<main class="sl-theme-dark">
  <div class="top-bar">
    <form on:submit|preventDefault>
      <div
        style="display: flex; justify-content: space-between; align-items: center; width: 98.7%; gap: 10px;"
      >
        <sl-dropdown>
          <sl-button
            slot="trigger"
            caret
            style="display: flex; align-items: center;"
            ><sl-icon name="justify" /></sl-button
          >
          <sl-menu>
            <sl-menu-item
              on:click={() => (showModal = true)}
              on:keydown={() => {}}
              role="button"
              tabindex="0"
              ><sl-icon name="person-gear" slot="prefix" /> User settings</sl-menu-item
            >
            <sl-menu-item
              on:click={() => {
                if (document.body.classList.contains("dark-mode")) {
                  document.body.classList.remove("dark-mode");
                  document.body.classList.add("sl-theme-dark");
                  document.body.classList.add("light-mode");
                } else {
                  document.body.classList.add("dark-mode");
                  document.body.classList.remove("sl-theme-dark");
                  document.body.classList.remove("light-mode");
                }
              }}
              role="button"
              tabindex="0"
              on:keydown={() => {}}
              ><sl-icon name="moon" slot="prefix" /> Toggle theme</sl-menu-item
            >
            <sl-divider />
            <sl-menu-item>
              GitHub
              <sl-icon slot="prefix" name="github" />
            </sl-menu-item>
          </sl-menu>
        </sl-dropdown>
        <sl-input
          style="width: 100%; border-radius: 0px;"
          placeholder="Enter an Amazon product URL"
          class="search-input"
          on:sl-input={() => {
            //@ts-ignore
            url = document.querySelector(".search-input").value;
          }}
        />
        <!-- svelte-ignore a11y-no-static-element-interactions a11y-click-events-have-key-events -->
        <sl-button class="search-button" on:click={scrapeData}
          ><sl-icon name="search" /></sl-button
        >
      </div>
    </form>
  </div>
  <div class="product-container">
    {#each products as product, i}
      <Product
        title={product.meta.title}
        image={product.meta.image}
        on:analysis={() => (modalStates[i] = true)}
        on:remove={() => {
          localStorage.removeItem(product.productId);
          products = ProductHandler.fetchProducts();
        }}
        disabled={(isLatestDone === "triggered" && i === 0) || null}
        ><br />
        {#if message !== "" && isLatestDone === "triggered" && i === 0}
          <slot name="analysis">{@html message}</slot>
        {/if}
        <div style="display: flex; align-items: center; gap: 10px">
          <sl-rating
            readonly
            value={product.reviews.length > 0
              ? parseFloat(
                  average(product.reviews.map((e) => e.overall)).toFixed(2)
                )
              : 0}
            style="--symbol-color-active: var(--sl-color-primary-600)"
            precision="0.01"
          />
        </div>
        <Modal bind:showModal={modalStates[i]}>
          <div slot="header"><h3>Product analysis</h3></div>
          The product rating predicted by Wordsmyth is:
          <sl-rating
            readonly
            value={product.reviews.length > 0
              ? parseFloat(
                  average(product.reviews.map((e) => e.overall)).toFixed(2)
                )
              : 0}
            style="--symbol-color-active: var(--sl-color-primary-600)"
            precision="0.01"
          /><br />
          <RatingBar
            data={product.analyzed
              .map((e) => e.rating)
              .filter((e) => e !== "empty string")}
          /><br />
        </Modal>
      </Product>
    {/each}
  </div>
  {#if products.length === 0}
    <div class="empty-space">
      <h1>Nothing here yet</h1>
      <a
        on:click={() => {
          //@ts-ignore
          document.querySelector(".search-input").value =
            "https://www.amazon.com/Samsung-Factory-Unlocked-Warranty-Renewed/dp/B07PB77Z4J";
        }}
        style="color: var(--sl-color-neutral-300)"
        href="#">Here's an example you can use</a
      >
    </div>
  {/if}
  <Modal bind:showModal>
    <div slot="header">
      <h3>Account information</h3>
    </div>
    <p style="color: var(--fg1)">
      Required to download Amazon reviews for analysis. This is never used
      anywhere except locally.
    </p>
    <label for="Address">Username/email</label>
    <input type="email" name="Address" bind:value={$email} />
    {#if validPass}<i class="fa fa-times" />{:else}<i
        class="fa fa-check"
      />{/if}<br />
    <label for="Password">Password</label>
    <input type="password" name="Password" bind:value={$password} />
    <br />
  </Modal>
</main>

<style>
  .empty-space {
    position: absolute;
    top: 50%;
    right: 50%;
    transform: translate(50%, -50%);
    text-align: center;
    color: var(--sl-color-neutral-300);
  }
  .search-input::part(base) {
    border-radius: 0px;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
  }
  .search-button::part(base) {
    border-radius: 0px;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
  }
  :global(body) {
    background-color: hsl(240, 5.9%, 8%);
    -ms-overflow-style: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    cursor: default;
    padding: 0;
    margin: 0;
  }
  :global(button) {
    cursor: pointer;
    border: none;
    user-select: none;
    border-radius: 5px;
    padding: 5px 15px;
  }
  :global(body.dark-mode button) {
    background-color: var(--color-primary-300);
    color: var(--color-surface-100);
  }
  :global(body.light-mode button) {
    background-color: var(--color-primary-300);
    color: var(--color-surface-600);
  }
  :global(body.dark-mode button:hover),
  :global(body.light-mode button:hover) {
    background-color: var(--color-primary-200);
  }
  :global(html::-webkit-scrollbar) {
    display: none;
  }
  .product-container {
    width: 95%;
    padding: 10px;
    position: relative;
    z-index: 1;
    left: 50%;
    transform: translateX(-50%);
    overflow: auto;
  }
  .top-bar {
    width: 100%;
    top: 0px;
    padding: 10px;
    background-color: var(--sl-color-neutral-0);
    position: sticky;
    border-bottom: 1px solid var(--color-surface-300);
    z-index: 3;
  }
  :global(body.light-mode .container) {
    background-color: var(--color-surface-300);
  }
</style>
