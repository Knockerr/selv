<script>
  const { title, children } = $props();
</script>

<div class="container">
  {#if title}
    <span class="title">{title}</span>
  {/if}
  {@render children?.()}
</div>

<style>
  .container {
    background-color: rgba(0, 0, 0, 0.25);
    border: 2px solid var(--muted);
    border-radius: 15px;
    width: 100%;
    height: fit-content;
    box-sizing: border-box;
    padding: 0px;
    overflow: hidden;
  }

  .title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--foreground);
  }
</style>
