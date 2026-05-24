<script>
  const { children, onclick } = $props();
</script>

<div class="component">
  <button class="button" {onclick}>
    <span class="text">{@render children?.()}</span>
  </button>
</div>

<style>
  button {
    background-color: #030712;
    border: 1px solid #1f2937;
    border-radius: 7px;
    color: #f5f5f5;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 15px;
    font-weight: 500;
    letter-spacing: 1px;
    padding: 0 16px;
    height: 42px;
    line-height: 42px;
    display: flex;
    align-items: center;
    gap: 5px;
    transition:
      background-color 0.3s ease,
      transform 0.3s ease;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    margin: 0;
    margin-bottom: 10px;
  }
  .text {
    display: inline-block;
    transform: scale(1);
  }

  button:hover {
    background-color: #0a1020;
    transform: scale(1.02);
  }

  button:active {
    transition: background-color 0s;
    background-color: #02050d;
  }
</style>
