<!-- <script lang="ts">
  export let title: string | undefined;
  export let image: string | undefined;
</script>

{#if title !== "" && image !== ""}
  <div class="container">
    <div class="entire-thing">
      <div class="review">
        <img src={image} alt={title} height="50" width="50" />
        <span>{title}</span>
      </div>
      <slot />
    </div>
  </div>
{/if}

<style>
  .container {
    background-color: var(--color-surface-200);
    padding: 10px;
    border-radius: 10px;
    margin-top: 10px;
  }
  .review {
    display: flex;
    align-items: center;
    gap: 10px;
  }
</style> -->
<script lang="ts">
  export let title: string | undefined;
  export let image: string | undefined;
</script>

<div class="container">
  <div>
    <div class="review">
      <img src={image} alt={title} height="50" width="50" />
      <span>{title}</span>
    </div>
    <slot />
  </div>
  <div class="analysis">
    <button>See analysis</button>
  </div>
</div>

<style>
  .container {
    background-color: var(--color-surface-200);
    padding: 10px;
    border-radius: 10px;
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .review {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .analysis {
    display: flex;
    align-items: center;
  }
</style>
