<script>
  import GridElem from "./gridElem.svelte";

  // Coming soon!
  let articles = $state([]);
</script>

<GridElem title="Articles">
  <div class="card" class:empty={articles.length === 0}>
    <div class="defaultContent">Aucun article pour le moment...</div>
  </div>
</GridElem>

<style>
  .card {
    height: 100%;
    width: 100%;
  }

  .defaultContent {
    color: var(--foreground-alt);
    font-size: 0.95rem;
    position: relative;
    top: -20px;
    display: none;
  }

  .card.empty {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .card.empty .defaultContent {
    display: inline;
  }
</style>
