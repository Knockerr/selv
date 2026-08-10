<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";

  function fullDatasReset() {
    folderSystem.resetDatas();
  }
</script>

<div class="page">
  <h1>Settings</h1>

  <h2 id="dangerZoneTitle">Danger zone</h2>

  <Button iconPath={pathDb.arrowClockwise} onclick={fullDatasReset}
    >Reinitialiser les données (action destructrice)</Button
  >
</div>

<style>
  .page {
    padding-left: 50px;
    height: 100%;
    width: 100%;
  }

  h1 {
    color: #ddd;
    font-family: var(--robotoFont);
    font-size: 3rem;
    font-weight: 500;
    letter-spacing: 1px;
  }

  #dangerZoneTitle {
    color: rgb(194, 39, 39);
    font-family: var(--robotoFont);
    font-size: 2.5rem;
    font-weight: 500;
    letter-spacing: 1px;
  }
</style>
