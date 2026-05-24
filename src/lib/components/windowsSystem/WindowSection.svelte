<script>
  // @ts-nocheck
  const { children, title } = $props();
</script>

<div class="component">
  <h3>{title}</h3>
  <div class="separator"></div>
  <div class="content">
    {@render children?.()}
  </div>
</div>

<style>
  .component {
    display: flex;
    flex-direction: column;
    align-items: left;
  }

  .separator {
    margin-bottom: 10px;
    height: 1.8px;
    width: 85%;
    background-color: #1f2937;
    align-self: center;
  }

  h3 {
    color: #ddd;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 1.7rem;
    padding: 0;
    margin: 0;
    margin-top: 15px;
    margin-bottom: 10px;
  }

  .content {
    margin-left: 12px;
  }
</style>
