<script>
  const { label, width = "550px", children } = $props();
</script>

<div class="flex flex-col gap-0">
  <span class="text-base font-semibold" style:width>{label}</span>
  <div class="container">
    {@render children?.()}
  </div>
</div>

<style>
  .container {
    height: fit-content;
    background-color: var(--background-alt);
    border: 1px solid var(--color-muted-foreground);
    border-radius: 12px;
    overflow: hidden;
  }

  .container:last-child{
    border-bottom: none;
  }
</style>
