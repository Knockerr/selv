<script>
  let { progress = $bindable(0), max = 100, width, height } = $props();

  let filledPercentage = $derived(Math.ceil((progress * 100) / max));
  let filledWidth = $derived(`${filledPercentage}%`);
  let full = $derived(filledPercentage >= 100);
</script>

<div class="component" style:width style:height>
  <div class="filled" class:full style:width={filledWidth}></div>
</div>

<style>
  .component {
    width: 150px;
    height: 12px;
    background-color: #777;
    border: 1px solid var(--color-background-dark);
    border-radius: 999px;
    position: relative;
    overflow: hidden;
  }

  .filled {
    height: 100%;
    background-color: #ddd;
    transition: all 0.3s ease;
  }

  .filled.full {
    background-color: var(--success);
  }
</style>
