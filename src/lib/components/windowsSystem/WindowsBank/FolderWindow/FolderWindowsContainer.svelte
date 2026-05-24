<script>
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { windowsManager } from "../../windowsManager.svelte";
  import FolderWindow from "./FolderWindow.svelte";

  let folders = $state(Object.keys(folderSystem.folderDatas));
  $effect(() => {
    folders = Object.keys(folderSystem.folderDatas).filter(
      (name) => folderSystem.getFolderData(name) !== undefined,
    );
  });
</script>

{#each folders as folderName (folderName)}
  <FolderWindow {folderName} />
{/each}
