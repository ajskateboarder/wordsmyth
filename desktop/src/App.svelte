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
  import StarRating from "svelte-star-rating";

  import Modal from "./lib/Modal.svelte";
  import Alert from "./lib/Alert.svelte";
  import Product from "./lib/Product.svelte";

  import { email, password } from "./stores";

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

  let message = "";
  let url = "";
  let reviews: Response[] = [];
  let analyzed: any[] = [];
  let product = {
    title: "",
    image: "",
  };

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
  };

  function doAnalysis() {
    analyzed = [];
    console.log(reviews);
    model = new WebSocket("ws://localhost:8002");
    model.onmessage = (e) => {
      analyzed = [...analyzed, JSON.parse(e.data)];
      console.log(e.data);
      message = `${analyzed.length}/${reviews.length} reviews analyzed`;
    };
    model.onopen = () => {
      console.log("Model started");
      reviews.forEach((message) => model.send(message.reviewText));
    };
  }

  function scrapeData() {
    try {
      browser.close();
      model.close();
    } catch {}
    reviews = [];
    browser = new WebSocket("ws://localhost:8001");
    browser.onmessage = (e) => {
      let data: Response = JSON.parse(e.data);
      if (data.type === "status") {
        message = data.message as string;
        if (data.message === "Scraping done") {
          browser.close();
          setTimeout(doAnalysis, 1000);
        }
      } else if (data.type === "response") {
        reviews = [...reviews, data];
        message = `${reviews.length} reviews collected`;
      } else if (data.type === "response_product") {
        product = data;
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
      browser.send(JSON.stringify({ command: "scrape", asin: asin }));
    };
  }

  (async () => {
    if ((await platform()) === "linux") {
      if (!(await exists("river"))) {
        message = "Downloading Amazon scraper...";
        let links = await getLatestRelease();
        const linuxBinary = await downloadEXE(links[0]);
        await writeBinaryFile("river", linuxBinary);
      }
      await invoke("run_river");
      message = "";
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

  const config = {
    emptyColor: "var(--color-surface-100)",
    fullColor: "var(--color-primary-100)",
    showText: true,
    size: 20,
  };
  const style = "margin-top: 10px";

  (async function () {
    document.body.classList.add(`${await appWindow.theme()}-mode`);
  })();
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"
    integrity="sha512-z3gLpd7yknf1YoNbCzqRKc4qyor8gaKU1qmn+CShxbuBusANI9QpRohGBreCFkKxLhei6S9CQXFEbbKuqLg0DA=="
    crossorigin="anonymous"
    referrerpolicy="no-referrer"
  /><link rel="preconnect" href="https://fonts.googleapis.com" />
  <link
    rel="preconnect"
    href="https://fonts.gstatic.com"
    crossorigin="anonymous"
  />
  <link
    href="https://fonts.googleapis.com/css2?family=Rubik&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<main>
  {#if message !== ""}
    <Alert {message} />
  {/if}
  <div class="top-bar">
    <button on:click={() => (showModal = true)}
      ><i class="fa fa-cog sidebar-item" /> Settings</button
    ><br /><br />
    <form on:submit|preventDefault>
      <div class="search-bar">
        <input type="text" placeholder="Enter a URL" bind:value={url} />
        <button on:click={scrapeData}>
          <i class="fa fa-magnifying-glass" />
        </button>
      </div>
    </form>
  </div>
  <div class="product-container">
    {#each Array(100).fill() as _}
      <Product
        title="guy"
        image="https://thumbs.dreamstime.com/t/creative-vector-illustration-default-avatar-profile-placeholder-isolated-background-art-design-grey-photo-blank-template-mo-118823351.jpg"
      >
        <StarRating
          rating={reviews.length > 0
            ? parseFloat(average(reviews.map((e) => e.overall)).toFixed(2))
            : 0}
          {config}
          {style}
        />
      </Product>
    {/each}
  </div>
  <!-- MODAL CODE -->
  <Modal bind:showModal>
    <div slot="header">
      <h3>Account information</h3>
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
    </div>
    <h3>Theme</h3>
    <button
      on:click={() => {
        if (document.body.classList.contains("dark-mode")) {
          document.body.classList.remove("dark-mode");
          document.body.classList.add("light-mode");
        } else {
          document.body.classList.add("dark-mode");
          document.body.classList.remove("light-mode");
        }
      }}>Toggle</button
    >
    <br />
  </Modal>
</main>

<style>
  :global(body) {
    background-color: var(--color-surface-100);
    -ms-overflow-style: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    cursor: default;
    padding: 0;
    margin: 0;
    overflow: hidden;
  }
  :global(*) {
    user-select: none;
    -ms-overflow-style: none;
    -moz-user-select: none;
    -ms-user-select: none;
  }
  :global(body.dark-mode) {
    --color-primary-100: #2196f3;
    --color-primary-200: #50a1f5;
    --color-primary-300: #6eacf6;
    --color-primary-400: #87b8f8;
    --color-primary-500: #9dc3f9;
    --color-primary-600: #b2cffb;

    --color-surface-100: #121212;
    --color-surface-200: #282828;
    --color-surface-300: #3f3f3f;
    --color-surface-400: #575757;
    --color-surface-500: #717171;
    --color-surface-600: #8b8b8b;

    color: #fff;
  }
  :global(body.light-mode) {
    --color-primary-100: #2196f3;
    --color-primary-200: #50a1f5;
    --color-primary-300: #6eacf6;
    --color-primary-400: #87b8f8;
    --color-primary-500: #9dc3f9;
    --color-primary-600: #b2cffb;

    --color-surface-600: #121212;
    --color-surface-500: #282828;
    --color-surface-400: #3f3f3f;
    --color-surface-300: #575757;
    --color-surface-200: #717171;
    --color-surface-100: #a3a3a3;

    color: black;
    background-color: white;
  }
  :global(button) {
    cursor: pointer;
    border: none;
    user-select: none;
    border-radius: 10px;
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
  button:hover {
    background-color: var(--color-primary-200);
  }
  :global(html::-webkit-scrollbar) {
    display: none;
  }
  .search-bar {
    display: flex;
    width: 97%;
    align-items: center;
    justify-content: center;
    position: sticky;
    padding: 0;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    right: 0;
    top: 0;
    left: 0;
    z-index: 3;
  }
  .search-bar input[type="text"] {
    flex: 1;
    padding: 8px;
    border: 1px solid transparent;
    background-color: var(--color-surface-200);
    border-right: none;
    font-size: 14px;
    color: var(--fg);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    border-radius: 25px 0 0 25px;
  }
  :global(body.light-mode) .search-bar input[type="text"] {
    background-color: var(--color-surface-500);
  }
  .search-bar input[type="text"]:focus {
    outline: none;
    border: 1px solid var(--color-primary-200);
    box-shadow: 0 0 10px var(--color-primary-200);
  }
  .search-bar input[type="text"]:focus ~ button {
    border: 1px solid var(--color-primary-200);
    box-shadow: 0 0 10px var(--color-primary-200);
  }
  .search-bar button {
    padding: 8px 12px;
    margin-left: -8px;
    border: 1px solid transparent;
    border-radius: 0 25px 25px 0;
    background-color: var(--color-primary-300);
    color: black;
    font-size: 14px;
    cursor: pointer;
  }
  .search-bar button:hover {
    background-color: var(--color-primary-200);
  }
  .product-container {
    position: absolute;
    right: 50%;
    transform: translateX(50%);
    width: 95%;
    padding: 10px;
    margin-top: 100px;
    margin-left: 10px;
    z-index: -999;
    overflow: auto;
  }
  .top-bar {
    width: 100%;
    top: 0px;
    padding: 10px;
    background-color: #1e1e1e;
    border-bottom: 2px solid var(--color-surface-200);
    position: fixed;
  }

  :global(body.light-mode .container) {
    background-color: var(--color-surface-300);
  }
</style>
