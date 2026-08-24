<script>
  
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import FolderManagement from "$lib/components/formSystem/forms/folderManagement.svelte";
  import Icon from "$lib/components/Icon.svelte";
  import ServerItem from "$lib/components/serverItem.svelte";
  import FolderSystem from "$lib/components/serverList/folderSystem.svelte";
  import SliderSwitch from "$lib/components/SliderSwitch.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import Input from "$lib/components/bits-ui/baseComponents/Input.svelte";
  import Dialog from "$lib/components/bits-ui/baseComponents/dialog.svelte";
  import CreateServerDialog from "$lib/components/bits-ui/presets/createServerDialog.svelte";
  import ImportServerDialog from "$lib/components/bits-ui/presets/importServerDialog.svelte";
  import EditFolderDialog from "$lib/components/bits-ui/presets/editFolderDialog.svelte";
  import ServerRenameDialog from "$lib/components/bits-ui/presets/ServerRenameDialog.svelte";
  import ServerDuplicateDialog from "$lib/components/bits-ui/presets/ServerDuplicateDialog.svelte";
  import ServerDeletionConfirm from "$lib/components/bits-ui/presets/ServerDeletionConfirm.svelte";

  let folderSystemRef = $state();
</script>

<div class="page">
  <div class="titleBar">
    <div class="titleBarLeftSide">
      <h1>Serveurs</h1>
    </div>
    <div class="titleBarRightSide">
      <ImportServerDialog
        refreshFoldersFunction={folderSystemRef.displayFolders}
      />
      <CreateServerDialog
        refreshFoldersFunction={folderSystemRef.displayFolders}
      />
    </div>
  </div>
  <div class="serverSorterGlobalContainer">
    <FolderSystem bind:this={folderSystemRef} />

    <div class="serverList">
      <div class="firstServerListLine">
        <button id="filtersButton">
          <Icon path={pathDb.sliders} size="18" color="#ddd" />Filtres
        </button>
      </div>

      <div class="serverListTable">
        <table>
          <thead>
            <tr>
              <th>Nom</th>
              <th>Statut</th>
              <th>Type</th>
              <th>Version</th>
              <th>Dossier</th>
              <th>Utilisation</th>
              <th></th>
            </tr>
          </thead>
          <tbody id="serverList">
            {#each folderSystem.serversToRender as server}
              <ServerItem uuid={server} />
            {/each}
          </tbody>
        </table>
      </div>
      <div class="serverSorterPageSwitcher">
        <button id="precedentPage" onclick={folderSystem.prevPage}>
          <Icon path={pathDb.arrowLeft} size="20" />
        </button>
        <input
          type="number"
          id="pageNumber"
          placeholder="..."
          value={folderSystem.currentPageIndex + 1}
          max="999"
          readonly
        />
        <button id="nextPage" onclick={folderSystem.nextPage}>
          <Icon path={pathDb.arrowRight} size="20" />
        </button>
      </div>
    </div>
  </div>
</div>

<EditFolderDialog reloadFoldersFunction={folderSystemRef.displayFolders} />
<ServerRenameDialog />
<ServerDuplicateDialog />
<ServerDeletionConfirm />

<style>
  table {
    table-layout: fixed;
    width: 100%;
    border-collapse: collapse;
  }

  .page {
    display: flex;
    flex-direction: column;
    gap: 0px;
    background-color: var(--mainBackgroundColor);
    height: 100%;
    margin: 10px 55px;
    padding-top: 20px;
    padding: 30px;
    box-sizing: border-box;
  }

  .titleBar {
    background-color: var(--mainBackgroundColor);
    margin: 0;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .titleBar h1 {
    margin-left: 10px;
    color: white;
    font-family: "Roboto", sans-serif;
    font-optical-sizing: auto;
    font-weight: 600;
    font-style: normal;
    justify-self: flex-start;
  }

  .titleBarLeftSide {
    margin-left: 5px;
  }

  .titleBarRightSide {
    display: flex;
    flex-direction: row;
    gap: 15px;
    margin-right: 50px;
    margin-top: 20px;
  }

  .serverSorterGlobalContainer {
    display: grid;
    height: 100%;
    grid-template-columns: 1fr 3.75fr;
    grid-template-rows: 1fr;
    margin-top: 10px;
    margin-right: 35px;
    gap: 20px;
    color: whitesmoke;
  }

  .serverList {
    background-color: var(--mainBackgroundColor);
    display: flex;
    flex-direction: column;
    gap: 0px;
    padding-top: 5px;
  }

  .firstServerListLine {
    padding: 0;
    margin: 0;
  }

  #filtersButton {
    margin-left: 10px;
    background-color: var(--mainBackgroundColor);
    border: 1px #1f2937;
    border-style: dashed;
    border-radius: 7px;
    color: white;
    font-family: "Open Sans", sans-serif;
    font-size: 14px;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 5px;
    transition:
      background-color 0.3s ease,
      transform 0.3s ease;
    position: relative;
    top: 10px;
    display: flex;
    flex-direction: row;
    gap: 5px;
    margin-bottom: 20px;
  }

  #filtersButton:hover {
    background-color: rgb(36, 46, 73);
    transform: scale(1.02);
  }

  #filtersButton:active {
    transition: background-color 0s;
    background-color: rgb(19, 25, 43);
  }

  .serverListTable {
    margin: 0 10px;
    border: #1f2937 1.5px solid;
    border-radius: 15px;
    background-color: var(--mainBackgroundColor);
  }

  .serverListTable table {
    table-layout: fixed;
    width: 100%;
    border-collapse: collapse;
  }

  .serverListTable th {
    font-family: "Roboto", sans-serif;
    font-weight: 500;
    font-size: 17px;
    text-align: left;
    padding-left: 15px;
    border-bottom: #1f2937 solid 1.5px;
    vertical-align: middle;
    height: 60px;
  }

  .serverSorterPageSwitcher {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-end;
    margin-right: 10px;
    margin-top: 5px;
    --pageSwitcherColor: rgba(196, 196, 196, 0.534);
  }

  .serverSorterPageSwitcher button {
    background-color: var(--mainBackgroundColor);
    border: 1px solid #1f2937;
    border-radius: 20px;
    color: var(--pageSwitcherColor);
    font-family: "Open Sans", sans-serif;
    font-size: 14px;
    padding: 5px;
    font-size: 20px;
    width: 60px;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
  }

  #precedentPage {
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
    border-right: none;
    transition:
      transform 0.3s ease,
      background-color 0.1s ease,
      color 0.15s ease;
  }

  #precedentPage:hover {
    transform: translateX(-5px);
    color: rgba(255, 255, 255, 0.856);
  }

  #nextPage {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
    border-left: none;
    transition:
      transform 0.3s ease,
      background-color 0.1s ease,
      color 0.15s ease;
  }

  #nextPage:hover {
    transform: translateX(5px);
    color: rgba(255, 255, 255, 0.856);
  }

  .serverSorterPageSwitcher button:hover {
    background-color: rgb(36, 46, 73);
  }

  .serverSorterPageSwitcher button:active {
    transition: background-color 0s;
    background-color: rgb(19, 25, 43);
  }

  .serverSorterPageSwitcher input {
    background-color: var(--mainBackgroundColor);
    border: 1px solid #1f2937;
    color: var(--pageSwitcherColor);
    font-family: "Open Sans", sans-serif;
    width: 50px;
    font-size: 14px;
    padding: 5px;
    font-size: 20px;
    transition: background-color 0.3s ease;
    text-align: center;
    transition:
      transform 0.3s ease,
      background-color 0.1s ease,
      color 0.15s ease;
  }

  .serverSorterPageSwitcher input:hover {
    color: rgba(255, 255, 255, 0.856);
  }

  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
</style>
