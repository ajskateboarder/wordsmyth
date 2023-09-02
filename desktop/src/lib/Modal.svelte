<script lang="ts">
  import { fs } from "@tauri-apps/api";
  export let showModal: boolean;

  let dialog: HTMLDialogElement;

  $: {
    if (dialog && showModal) {
      dialog.showModal();
      document.body.style.overflow = "hidden";
    }
    if (!showModal) {
      document.body.style.overflow = "auto";
    }
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
  bind:this={dialog}
  on:close={() => (showModal = false)}
  on:click|self={() => dialog.close()}
>
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div on:click|stopPropagation>
    <slot name="header" />
    <hr />
    <slot />
    <hr />
    <!-- svelte-ignore a11y-autofocus -->
    <button autofocus on:click={() => dialog.close()} class="submit"
      >Done</button
    >
  </div>
</dialog>

<style>
  dialog {
    max-width: 32em;
    border-radius: 0.2em;
    border: none;
    padding: 20px;
    overflow: hidden;
    color-scheme: dark;
    background-color: var(--color-surface-200);
    color: white;
  }
  dialog::backdrop {
    background: rgba(0, 0, 0, 0.3);
  }
  dialog > div {
    padding: 1em;
  }
  dialog[open] {
    animation: zoom 0.2s;
  }
  @keyframes zoom {
    0% {
      transform: scale(0.95);
    }
    50% {
      transform: scale(1.01);
    }
    100% {
      transform: scale(1);
    }
  }
  dialog[open]::backdrop {
    animation: fade 0.1s ease-out;
  }
  @keyframes fade {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
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
  hr {
    background-color: var(--color-surface-600);
    height: 1px;
    border: 0;
  }
</style>
