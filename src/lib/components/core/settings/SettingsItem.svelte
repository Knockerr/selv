<script>
  const { title, description, children, noborder = false } = $props();
</script>

<div class="component">
  <div class="left">
    <span class="title">{title}</span>
    <span class="description">{description}</span>
  </div>
  <div class="right">
    {@render children?.()}
  </div>
</div>

{#if !noborder}
  <div class="separator"></div>
{/if}

<style>
  .component {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    position: relative;
    height: fit-content;
    box-sizing: border-box;
    padding: 25px;
  }

  .left {
    display: flex;
    flex-direction: column;
    align-self: flex-start;
    gap: 5px;
    width: 40%;
  }

  .title {
    font-size: 1.15rem;
    font-weight: 500;
    color: var(--foreground);
  }

  .description {
    font-size: 0.95rem;
    color: var(--foreground-alt);
  }

  .right {
    width: 40%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 10px;
  }

  .separator {
    width: 500%;
    position: relative;
    left: -25%;
    height: 2px;
    background-color: var(--muted);
  }
</style>
