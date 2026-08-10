<script>
  // @ts-nocheck
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import IconButton from "../../baseComponents/iconButton.svelte";

  const { serverUuid, serverName, folderName, isInFolder } = $props();

  // Regler nom de classes bizzares + rendre plus beau

  async function onSwitchStateButtonClick() {
    await folderSystem.getFolder(folderName).toggleServerPresence(serverUuid);
  }
</script>

<div class="container">
  <div class="containerLeft">
    <div class="folderNameContainer">
      <h3 id="folderName">{serverName}</h3>
    </div>
  </div>
  <div class="containerRight">
    {#if isInFolder}
      <IconButton
        iconSize="14"
        iconPath={pathDb.minus}
        onclick={onSwitchStateButtonClick}
      />
    {:else}
      <IconButton
        iconSize="14"
        iconPath={pathDb.plus}
        onclick={onSwitchStateButtonClick}
      />
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
    background-color: rgba(255, 255, 255, 0.068);
    transition: background-color 0.13s ease;
    padding-left: 10px;
    width: 80%;
  }

  .container:hover {
    background-color: var(--muted);
  }

  h3 {
    color: #fff;
  }

  .containerLeft,
  .containerRight {
    display: flex;
    flex-direction: row;
    gap: 5px;
    align-items: center;
    margin: 0 5px;
    margin-right: 15px;
  }

  .containerLeft {
    flex: 1;
  }

  .folderNameContainer {
    width: 100%;
  }

  .containerLeft h3 {
    font-family: "Roboto", sans-serif;
    font-weight: 400;
    font-size: 15px;
    padding-left: 10px;
    width: 100%;
    max-width: 270px;
    overflow-x: hidden;
  }
</style>
