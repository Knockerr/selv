<script>
  const { height = "100px", width = "100px" } = $props();
</script>

<div class="loader" style:width style:height></div>

<style>
  .loader {
    width: 100px;
    height: 100px;
    border: 6px solid transparent;
    border-top: 6px solid #3b82f6;
    border-bottom: 6px solid var(--emphasized);
    border-radius: 50%;
    animation: rotate 1s linear infinite;
  }

  @keyframes rotate {
    to {
      transform: rotate(360deg);
    }
  }
</style>
