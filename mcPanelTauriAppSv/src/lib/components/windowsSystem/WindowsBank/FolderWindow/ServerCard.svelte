<script>
    // @ts-nocheck
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";

  const { serverUuid, serverName, folderName, isInFolder } = $props();

  // Regler nom de classes bizzares + rendre plus beau

  function onSwitchStateButtonClick() {
    folderSystem.getFolder(folderName).toggleServerPresence(serverUuid);
  }
</script>

<div class="container">
  <div class="containerLeft">
    <h3 id="folderName">{serverName}</h3>
  </div>
  <div class="containerRight">
    <button class="switchStateButton" onclick={onSwitchStateButtonClick}>
      {#if isInFolder}
        <Icon path={pathDb.minus} size="18" />
      {:else}
        <Icon path={pathDb.plus} size="18" />
      {/if}
    </button>
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
    width: 80%;
  }

  h3 {
    color: #fff;
  }

  .container:hover {
    background-color: #283446;
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

  .containerRight button {
    --containerEditButtonSize: 30px;
    background-color: transparent;
    border: 0px solid;
    border-radius: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 14px;
    width: var(--containerEditButtonSize);
    height: var(--containerEditButtonSize);
    transition: background-color 0.2s ease;
  }

  .containerRight button:hover {
    background-color: #1d2735;
    cursor: pointer;
  }

  .containerRight button:active {
    transition:
      background-color 0s ease,
      color 0s ease;
    background-color: #121820;
    color: #998fbb;
  }
</style>
