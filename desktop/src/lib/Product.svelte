<script lang="ts">
  export let title: string;
  export let image: string;
</script>

{#if title !== "" && image !== ""}
  <div class="container">
    <div class="review">
      <img src={image} alt={title} />
      <span>{title}</span>
    </div>
    <slot />
  </div>
{/if}

<style>
  .container {
    background-color: var(--color-surface-200);
    padding: 10px;
    border-radius: 10px;
  }
  .review {
    display: flex;
    align-items: center;
    gap: 10px;
  }
</style>
