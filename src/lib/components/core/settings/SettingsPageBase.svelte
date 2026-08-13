<script>
  const { title, description } = $props();
</script>

<div class="component">
  <div class="titleSection">
    <span class="title">
      {title}
    </span>
    <span class="description">
      {description}
    </span>
  </div>
</div>

<style>
  .component {
    display: flex;
    flex-direction: column;
  }

  .titleSection{
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 70%;
  }

  .title{
    font-size: 1.75rem;
    font-weight: 500;
    color: var(--foreground);
  }

  .description{
    font-size: 1.1rem;
    color: var(--foreground-alt);
  }

  
</style>
