<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let title: string | undefined;
  export let image: string | undefined;

  const analysis = () => dispatch("analysis");
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
    <button on:click={analysis}>See analysis</button>
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
    width: 150px;
    min-width: 150px;
    justify-content: center;
  }
</style>
