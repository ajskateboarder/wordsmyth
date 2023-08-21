<script lang="ts">
  import { invoke } from "@tauri-apps/api";
  import StarRating from "../lib/StarRating.svelte";

  let loading = false;
  let content: string = "";

  type Data = {
    asin: string;
    price: string;
    rating: string;
    title: string;
    image: string;
    review_count: string;
  };
  let data: Data[] = [];

  const ws = new WebSocket("ws://localhost:8001");

  ws.onmessage = async (e) => {
    data = await invoke("search_results", { html: e.data });
    loading = false;
  };

  async function handle() {
    ws.send(content);
    loading = true;
  }
</script>

<h1>Find products</h1>
<div class="search-bar">
  <input
    type="text"
    placeholder="Search..."
    bind:value={content}
    on:keydown={(e) => {
      if (e.key === "Enter") {
        handle();
      }
    }}
  />
  <button on:click={handle}>
    {#if loading}
      <i class="fa-solid fa-circle-notch fa-spin" />
    {:else}
      <i class="fa fa-magnifying-glass" />
    {/if}
  </button>
</div>
<br />
<div class="list-container">
  {#if !loading}
    {#each data as datum}
      {#if !datum.title.startsWith("Sponsored")}
        <div class="list-item">
          <div class="image">
            <img src={datum.image} alt="pdocut" />
          </div>
          <div class="item-text">
            <p>{datum.title}</p>
            {#if datum.price !== "None"}
              <sup>$</sup><b style="font-size: 20px;"
                >{datum.price.split(".")[0]}</b
              ><sup>{datum.price.split(".")[1]}</sup>
            {/if}
            {#if datum.rating !== "None"}
              <StarRating rating={parseFloat(datum.rating.split(" ")[0])} />
              {datum.review_count}
            {/if}
          </div>
        </div>
      {/if}
    {/each}
  {:else}
    {#each Array(23) as _}
      <div class="list-item">
        <img src="/placeholder.png" alt="product" loading="lazy" />
        <div class="item-text">
          <p>...</p>
          <b>...</b>
          <p>...</p>
        </div>
      </div>
    {/each}
  {/if}
</div>

<style>
  .list-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    justify-content: center;
  }

  .list-item {
    display: flex;
    background-color: var(--color-surface-200);
    border-radius: 1q0px;
    padding: 10px;
    align-items: center;
    margin-bottom: 20px;
  }

  .list-item img {
    max-width: 100px; /* Adjust the width as needed */
    margin-right: 20px;
  }

  .item-text {
    flex: 1;
  }

  .image {
    width: 150px;
    display: flex;
    justify-content: center;
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
