<script>
  const { title, value, unit = "", style } = $props();
</script>

<div class="component" {style}>
  <span class="title">{title}</span>
  <div class="valueRow">
    <span class="value">{value}</span>
    {#if unit}
      <span class="unit">{unit}</span>
    {/if}
  </div>
</div>

<style>
  .component {
    display: flex;
    flex-direction: column;
    gap: 4px;
    box-sizing: border-box;
    padding: 14px 16px;
  }

  .title {
    color: var(--foreground-alt);
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .valueRow {
    display: flex;
    align-items: baseline;
    gap: 6px;
  }

  .value {
    font-size: 2.6rem;
    font-weight: 600;
    line-height: 1;
    letter-spacing: -0.02em;
  }

  .unit {
    font-size: 1.1rem;
    color: var(--foreground-alt);
    font-weight: 500;
  }
</style>