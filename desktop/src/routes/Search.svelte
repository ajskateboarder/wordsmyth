<script lang="ts">
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

  async function handle() {
    loading = true;
    data = [
      {
        asin: "2",
        price: "12 bu",
        rating: "5",
        title: "p",
        image: "https://google.com/favicon.ico",
        review_count: "120",
      },
    ];
    loading = false;
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
    border: 1px solid var(--fg4);
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
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    right: 0;
    top: 0;
    left: 0;
    z-index: 3;
  }

  .search-bar input[type="text"] {
    flex: 1;
    padding: 8px;
    border: 1px solid grey;
    border-right: none;
    font-size: 14px;
    color: var(--fg);
    background-color: var(--bg1);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
  }

  .search-bar input[type="text"]:focus {
    outline: none;
    border: 1px solid #fdbb7c;
    box-shadow: 0 0 10px #fdbb7c;
  }

  .search-bar input[type="text"]:focus ~ button {
    border: 1px solid #fdbb7c;
    box-shadow: 0 0 10px #fdbb7c;
  }

  .search-bar button {
    padding: 8px 12px;
    margin-left: -8px; /* Overlap with input box */
    border: 1px solid grey;
    border-radius: 0 4px 4px 0; /* Rounded only on the right side */
    background-color: #fdbb7c;
    color: black;
    font-size: 14px;
    cursor: pointer;
  }

  @keyframes pulse-animation {
    0% {
      box-shadow: 0 0 0 0px rgba(0, 0, 0, 0.2);
    }
    100% {
      box-shadow: 0 0 0 20px rgba(0, 0, 0, 0);
    }
  }

  .search-bar button:hover {
    background-color: var(--fg2);
  }
</style>
