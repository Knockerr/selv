<script>
  const { children } = $props();
</script>

<div class="component">
  {@render children?.()}
</div>

<style>
  .component {
    display: flex;
    flex-direction: row;
  }
</style>
