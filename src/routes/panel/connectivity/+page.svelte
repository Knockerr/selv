<script>
  import { sidebarStore } from "$lib/sideBarsStore.svelte";

  sidebarStore.setCurrentTab("panel", "Connectivité");
</script>

<div class="page">
  <h1 class="title">Connectivité</h1>
</div>

<style>
  .page {
    height: 100%;
    width: 100%;
  }

  .title {
    width: 100%;
    padding: 5px 50px;
    box-sizing: border-box;
    font-family: var(--robotFont);
    font-size: 3rem;
    font-weight: 500;
  }
</style>
