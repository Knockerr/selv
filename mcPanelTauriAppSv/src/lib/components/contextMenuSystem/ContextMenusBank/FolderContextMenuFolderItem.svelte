<script>
  // @ts-nocheck
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { onMount, untrack } from "svelte";
  import { contextManager } from "../contextMenuManager.svelte";
  import SliderSwitch from "$lib/components/SliderSwitch.svelte";

  const { serverUuid, folderName } = $props();

  // Regler nom de classes bizzares + rendre plus beau

  let isInFolder = $derived(
    folderSystem.getFolder(folderName).contains(serverUuid),
  );
</script>

<div class="container">
  <div class="containerLeft">
    <h3 id="folderName">{folderName}</h3>
  </div>
  <div class="containerRight">
    <SliderSwitch
      bind:value={isInFolder}
      onSwitch={() => {
        if (isInFolder)
          folderSystem.getFolder(folderName).addServer(serverUuid);
        else folderSystem.getFolder(folderName).removeServer(serverUuid);
      }}
    />
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
</style>
