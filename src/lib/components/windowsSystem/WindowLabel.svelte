<script>
  const { children } = $props();
</script>

<div class="component">
  <p class="text">
    {@render children?.()}
  </p>
</div>

<style>
  p {
    font-family: Arial, Helvetica, sans-serif;
    color: #ddd;
    font-size: 16px;
    margin: 0;
    margin-bottom: 10px;
  }
</style>
