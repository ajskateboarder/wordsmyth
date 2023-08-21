<script lang="ts">
  import Router from "./Router.svelte";
  import { getClient, ResponseType } from "@tauri-apps/api/http";
  import { platform } from "@tauri-apps/api/os";
  import { invoke } from "@tauri-apps/api/tauri";
  import {
    writeBinaryFile,
    type BinaryFileContents,
    exists,
  } from "@tauri-apps/api/fs";
  import Alert from "./lib/Alert.svelte";

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
      if (exists("river.exe")) {
        return;
      }

      let links = getLatestRelease();
      const linuxBinary = await downloadEXE(links[0]);
      await writeBinaryFile("river", linuxBinary);
      await invoke("run_river");
    }
    console.log("maybe started");
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
  <Router />
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
  :global(body) {
    -ms-overflow-style: none;
  }
  :global(html::-webkit-scrollbar) {
    display: none;
  }
</style>
