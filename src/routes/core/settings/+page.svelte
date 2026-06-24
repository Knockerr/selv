<script>
  import CustomButton from "$lib/components/CustomButton.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";

  function fullDatasReset() {
    folderSystem.resetDatas();
  }
</script>

<h1>Settings</h1>

<CustomButton
  iconPath={pathDb.arrowClockwise}
  onclick={fullDatasReset}
  >Reinitialiser les données (action destructrice)</CustomButton
>

<style>
</style>
