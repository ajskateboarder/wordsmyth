<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  export let title: string | undefined;
  export let image: string | undefined;
  export let disabled: boolean | null;

  const analysis = () => dispatch("analysis");
  const remove = () => dispatch("remove");
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions a11y-interactive-supports-focus -->
<div class="container">
  <div>
    <div class="review">
      <img src={image} alt={title} height="50" width="50" />
      <span>{title}</span>
    </div>
    <slot />
  </div>
  <div class="analysis">
    <slot name="analysis"
      ><sl-button-group>
        <sl-button on:click={analysis} role="button" {disabled}
          >See analysis</sl-button
        >
        <!-- <button on:click={analysis}>See analysis</button><br /> -->
        <sl-button class="close-button" on:click={remove} role="button"
          ><sl-icon name="x" /></sl-button
        >
      </sl-button-group>&nbsp;&nbsp;&nbsp;
    </slot>
  </div>
</div>

<style>
  .container {
    background-color: var(--sl-color-neutral-50);
    padding: 10px;
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 0 0 1px #000;
    border: 0.1rem solid var(--color-surface-300);
    margin-top: 10px;
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
  .close-button::part(base):hover {
    background-color: var(--sl-color-danger-100);
    border: 1px solid var(--sl-color-danger-300);
    color: var(--sl-color-danger-600);
  }
</style>
