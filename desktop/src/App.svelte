<script lang="ts">
  import { getClient, ResponseType } from "@tauri-apps/api/http";
  import { platform } from "@tauri-apps/api/os";
  import { invoke } from "@tauri-apps/api/tauri";
  import {
    writeBinaryFile,
    type BinaryFileContents,
    exists,
  } from "@tauri-apps/api/fs";

  import Modal from "./lib/Modal.svelte";
  import Alert from "./lib/Alert.svelte";
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
  let asin = "";

  type Response = {
    type: "status" | "response";
    message?: string;
  };

  function scrapeData() {
    browser.onmessage = (e) => {
      let data: Response = JSON.parse(e.data);
      if (data.type === "status") {
        message = data.message;
      } else {
        console.log(JSON.stringify(data));
      }
    };
    browser.send(
      JSON.stringify({
        command: "login",
        username: $email,
        password: $password,
      })
    );
    browser.send(JSON.stringify({ command: "scrape", asin: asin }));
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
      browser = new WebSocket("ws://localhost:8001");
    } else if ((await platform()) === "win32") {
      if (exists("river.exe")) {
        return;
      }

      let links = getLatestRelease();
      const linuxBinary = await downloadEXE(links[0]);
      await writeBinaryFile("river", linuxBinary);
      await invoke("run_river");
    }
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
  <button on:click={() => (showModal = true)}
    ><i class="fa fa-cog sidebar-item" /> Settings</button
  >
  <div class="search-bar">
    <input
      type="text"
      placeholder="Search..."
      bind:value={asin}
      on:keydown={(e) => {
        if (e.key === "enter") {
          console.log("OJK");
        }
      }}
    />
    <button on:click={scrapeData}>
      <i class="fa fa-magnifying-glass" />
    </button>
  </div>
  <Modal bind:showModal>
    <div slot="header">
      <h2>Account information</h2>
      <p style="color: var(--fg1)">
        Required to download Amazon reviews for analysis. This is never used
        anywhere except locally.
      </p>
    </div>
    <label for="Address">Username/email</label>
    <input type="email" name="Address" bind:value={$email} />
    {#if validPass}<i class="fa fa-times" />{:else}<i
        class="fa fa-check"
      />{/if}<br />
    <label for="Password">Password</label>
    <input type="password" name="Password" bind:value={$password} />
  </Modal>
</main>

<style>
  :root {
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

    background-color: var(--color-surface-100);
    color: #fff;
  }
  button {
    background-color: var(--color-primary-300);
    color: var(--color-surface-100);
    border: none;
    border-radius: 10px;
    padding: 5px 15px;
  }
  button:hover {
    background-color: var(--color-primary-200);
  }
  :global(body) {
    -ms-overflow-style: none;
  }
  :global(html::-webkit-scrollbar) {
    display: none;
  }
  .search-bar {
    display: flex;
    width: 100%;
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
</style>
