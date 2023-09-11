<script>
  export let message = "";
</script>

<div class="alert-container">
  <div class="alert">{@html message}</div>
</div>

<style scoped>
  .alert-container {
    display: flex;
    justify-content: center;
    position: fixed;
    bottom: calc(90vh);
    left: 50%;
    transform: translateX(-50%) translateY(85vh);
    z-index: 9999;
  }

  .alert {
    background-color: black;
    text-align: center;
    border: 1px solid var(--color-primary-100);
    padding: 15px;
    border-radius: 5px;
    width: 300px; /* Adjust width as needed */
  }
</style>
