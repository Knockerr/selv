<script>
  // @ts-nocheck
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { onMount } from "svelte";
  import FolderManagement from "./formSystem/forms/folderManagement.svelte";
  import Icon from "./Icon.svelte";
  import EditFolderDialog from "./bits-ui/presets/editFolderDialog.svelte";
  import IconButton from "./bits-ui/baseComponents/iconButton.svelte";
  import { uiStore } from "./bits-ui/uiComponentsStore.svelte";

  const {
    folderName = "UNDEFINED",
    numberOfServers = 0,
    isFavorite,
    removeEditButton = false,
  } = $props();

  const onFolderClick = () => {
    folderSystem.selectFolder(folderName);
  };

  let openFolderWindow = () => {
    console.info("Opening folder windows " + `FolderWindow-${folderName}`);
    windowsManager.open(`FolderWindow-${folderName}`);
  };
</script>

<div
  class="container"
  class:selected={folderSystem.currentSelectedFolder === folderName}
  role="button"
  onclick={onFolderClick}
  onkeydown={(e) => {
    e.preventDefault();
    onFolderClick();
  }}
  tabindex="0"
>
  <div class="containerLeft">
    {#if isFavorite === "true"}
      <Icon path={pathDb.folderStar} size="18" color="#ddd" />
    {:else}
      <Icon path={pathDb.folder} size="18" color="#ddd" />
    {/if}

    <h3 id="folderName">{folderName}</h3>
  </div>
  <div class="containerRight">
    <p id="numOfServs">{numberOfServers}</p>

    {#if !removeEditButton}
      <IconButton
        onclick={() => {
          uiStore.setCurrentEditedFolder(folderName);
          uiStore.openDialog("editFolderDialog");
        }}
        iconPath={pathDb.pencil}
      />
    {:else}
      <div id="blank"></div>
    {/if}
  </div>
</div>

<style>
  .container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 5px;
    border: 0px solid;
    border-radius: 12px;
    background-color: #040713;
    transition: background-color 0.13s ease;
    padding-left: 10px;
  }

  h3 {
    color: #fff;
  }

  p {
    font-size: 15px;
    color: whitesmoke;
  }

  .container:hover {
    background-color: #283446;
    cursor: pointer;
  }

  .selected {
    background-color: #283446 !important;
  }

  .containerLeft,
  .containerRight {
    display: flex;
    flex-direction: row;
    gap: 5px;
    align-items: center;
    margin: 0 5px;
  }

  .containerLeft h3 {
    font-family: "Roboto", sans-serif;
    font-weight: 400;
    font-size: 15px;
    padding-left: 10px;
  }

  .containerRight p {
    font-family: "Roboto", sans-serif;
    font-weight: 400;
    font-size: 14.5px;
    color: #8a8e94;
    margin-right: 0;
  }
</style>
