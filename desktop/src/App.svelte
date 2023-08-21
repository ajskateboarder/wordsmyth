<script lang="ts">
  import Router from "./Router.svelte";

  // Don't ask LOL
  class RootBuilder {
    private root: HTMLElement;
    constructor() {
      let root = document.querySelector(":root") as HTMLElement;
      this.root = root;
    }
    add(key: string, value: string): RootBuilder {
      this.root.style.setProperty(`${key}`, value);
      return this;
    }
  }

  new RootBuilder()
    .add("--bg-hhh", "#1d2021")
    .add("--bg", "#282828")
    .add("--bg_s", "#32302f")
    .add("--bg1", "#3c3836")
    .add("--bg2", "#504945")
    .add("--bg3", "#665c54")
    .add("--bg4", "#7c6f64")
    .add("--fg", "#fbf1c7")
    .add("--fg1", "#ebdbb2")
    .add("--fg2", "#d5c4a1")
    .add("--fg3", "#bdae93")
    .add("--fg4", "#a89984")
    .add("background-color", "var(--bg-hhh)")
    .add("color", "var(--fg)");
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
  <Router />
</main>

<style>
  :root {
    background-color: var(--bg-hhh);
    color: var(--fg);
  }
  :global(body) {
    -ms-overflow-style: none;
  }
  :global(html::-webkit-scrollbar) {
    display: none;
  }
</style>
