<script>
  // @ts-nocheck

  /*
  TODO : 
  -> fix bugs; 
  -> Optimize the fetch of server datas (store saw servers in a cache?);
  */

  /*
    Datas strucure:
  {
    nomDuDossier: {
      "isFolderFav": false,
      "servers": []
    }
  }

  */

  import { pathDb } from "$lib/icons/pathDb";
  import { onMount, untrack } from "svelte";
  import FolderItem from "../folderItem.svelte";
  import Icon from "../Icon.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import FolderManagement from "../formSystem/forms/folderManagement.svelte";
  import FolderWindowsContainer from "../windowsSystem/WindowsBank/FolderWindow/FolderWindowsContainer.svelte";
  import InputDialog from "../bits-ui/baseComponents/InputDialog.svelte";
  import { uiStore } from "../bits-ui/uiComponentsStore.svelte";

  let foldersToRender = $state([]);
  let favfoldersToRender = $state([]);

  let folderName = $state("all");

  onMount(() => {
    displayFolders();
  });

  $inspect(folderSystem.foldersToRender).with(() => {
    console.info(
      `Folders To Render : >>>>>>>>>>>>>>>>>>> ${folderSystem.foldersToRender}`,
    );
  });

  function clearFoldersContainers() {
    foldersToRender = [];
    favfoldersToRender = [];
  }

  export function displayFolders() {
    clearFoldersContainers();
    if (!folderSystem.folderDatas) return;
    Object.keys(folderSystem.folderDatas).forEach((folderName) => {
      const folderDatas = folderSystem.getFolder(folderName).datas();
      if (folderDatas.isFolderFav) {
        favfoldersToRender = [...favfoldersToRender, folderName];
      } else {
        foldersToRender = [...foldersToRender, folderName];
      }
      console.info(`foldersToRender > ${foldersToRender}`);
      console.info(`favfoldersToRender > ${favfoldersToRender}`);
    });
  }

  function createFolder(folderName) {
    console.log("Creating folder..");

    if (folderSystem.folderDatas.hasOwnProperty(folderName)) {
      alert(folderName + " already exists in db! Aborting..");
      return;
    }

    folderSystem.createFolder(folderName, false, []);

    displayFolders();
  }

  $effect(() => {
    folderSystem.folderDatas;
    untrack(() => {
      displayFolders();
    });
  });

  // TODO : Switch buttons to IconButtons..
</script>

<div class="folderSystem">
  <div class="folderSystemTitle">
    <h2>Dossiers</h2>
    <div class="folderSystemTitleRight">
      <button
        id="reloadFoldersButton"
        class="folderSystemButton"
        aria-label="TODO"
        onclick={displayFolders}
      >
        <Icon path={pathDb.arrowClockwise} size="18" />
      </button>
      <button
        id="createFolderButton"
        class="folderSystemButton"
        aria-label="TODO"
        onclick={() => {
          uiStore.openDialog("createFolderDialog");
        }}
      >
        <Icon path={pathDb.folderPlus} size="18" />
      </button>
    </div>
  </div>
  <div class="foldersContainer">
    <div class="favoriteFolders" id="favoriteFoldersContainer">
      <FolderItem
        folderName="all"
        numberOfServers={[...folderSystem.getAllServers].length}
        isFavorite="true"
        removeEditButton={true}
      />
      {#each favfoldersToRender as favFolder (favFolder)}
        <FolderItem
          folderName={favFolder}
          numberOfServers={folderSystem.getFolderData(favFolder)?.servers
            ?.length || 0}
          isFavorite="true"
        />
      {/each}
    </div>
    <div class="seperator"></div>
    <div class="normalFolders">
      {#each foldersToRender as folder (folder)}
        <FolderItem
          folderName={folder}
          numberOfServers={folderSystem.getFolderData(folder)?.servers
            ?.length || 0}
          isFavorite="false"
        />
      {/each}
    </div>
  </div>
</div>

<InputDialog
  title="Création de dossier"
  description="Entrez le nom de votre dossier"
  placeholder="Nom du dossier"
  onConfirm={(value) => {
    createFolder(value);
    uiStore.closeDialog("createFolderDialog");
  }}
  name="createFolderDialog"
/>

<style>
  button {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .folderSystem {
    background-color: var(--mainBackgroundColor);
    padding: 5px;
  }

  .folderSystemTitle {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
    padding: 0 20px;
    line-height: 60px;
  }

  .folderSystemTitle h2 {
    font-family: "Roboto", sans-serif;
    font-weight: 400;
    font-size: 22px;
  }

  .folderSystemTitleRight {
    display: flex;
    flex-direction: row;
  }

  .folderSystemButton {
    border: 0px solid;
    background-color: var(--mainBackgroundColor);
    color: white;
    font-size: 20px;
    border-radius: 50%;
    height: 35px;
    width: 35px;
    transform: scale(1.15);
  }

  @keyframes fullRotation {
    from {
      transform: rotate(0deg) scale(1.15);
    }
    to {
      transform: rotate(360deg) scale(1.15);
    }
  }

  .folderSystemButton:hover {
    transition: background-color 0.3s ease;
    background-color: rgb(50, 59, 80);
  }

  .folderSystemButton:active {
    transition: background-color 0s ease;
    background-color: rgb(32, 38, 54);
  }

  .foldersContainer {
    background-color: transparent;
    height: 100%;
    padding: 5px;
    margin-left: 30px;
    margin-right: 10px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 0px;
  }

  .favoriteFolders {
    background-color: var(--mainBackgroundColor);
    padding: 5px;
    margin-bottom: 15px;
  }

  .normalFolders {
    background-color: var(--mainBackgroundColor);
    padding: 5px;
    margin-bottom: 15px;
  }

  .seperator {
    border-bottom: #1f2937 1.25px solid;
    background-color: transparent;
    height: 0px;
    width: 95%;
    align-self: center;
  }
</style>
