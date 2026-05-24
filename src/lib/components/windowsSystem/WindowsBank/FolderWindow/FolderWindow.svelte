<script>
  // @ts-nocheck
  import Icon from "$lib/components/Icon.svelte";
  import ServerItem from "$lib/components/serverItem.svelte";
  import FolderSystem from "$lib/components/serverList/folderSystem.svelte";
  import SliderSwitch from "$lib/components/SliderSwitch.svelte";
  import Window from "$lib/components/windowsSystem/Window.svelte";
  import WindowButton from "$lib/components/windowsSystem/WindowButton.svelte";
  import WindowLabel from "$lib/components/windowsSystem/WindowLabel.svelte";
  import WindowSection from "$lib/components/windowsSystem/WindowSection.svelte";
  import WindowTextInput from "$lib/components/windowsSystem/WindowTextInput.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { onMount } from "svelte";
  import WindowAligned from "../../WindowAligned.svelte";
  import WindowSlider from "../../WindowSlider.svelte";
  import { windowsManager } from "../../windowsManager.svelte";
  import ServersManager from "./ServersManager.svelte";

  const { folderName } = $props();

  // Liaison au store
  let windowId = $derived("FolderWindow-" + folderName);

  let isFolderFav = $derived(
    folderSystem.getFolderData(folderName)?.isFolderFav || false,
  );

  $effect(async () => {
    if (isFolderFav !== folderSystem.getFavoriteValue(folderName)) {
      await folderSystem.setFavoriteValue(folderName, isFolderFav);
    }
  });

  // Systeme de rennomage de fichiers
  let nouveauNom = $state();
  async function onClickRenommage() {
    await folderSystem.getFolder(folderName).rename(nouveauNom);
    windowsManager.closeAll();
  }

  async function onClickSupprimer() {
    await folderSystem.delete(folderName);
    windowsManager.closeAll();
  }

  const isOpen = $derived(windowsManager.openWindows.has(windowId));
</script>

{#if isOpen}
  <Window height="60%" width="30%" title={folderName} {windowId}>
    <WindowSection title="Gestion">
      <WindowAligned>
        <WindowLabel>Dossier favori:</WindowLabel>
        <WindowSlider bind:value={isFolderFav} />
      </WindowAligned>
      <WindowAligned>
        <WindowTextInput placeholder="Nouveau nom" bind:value={nouveauNom} />
        <WindowButton
          onclick={async () => {
            await onClickRenommage();
          }}>Renommer</WindowButton
        >
      </WindowAligned>
    </WindowSection>
    <WindowSection title="Serveurs">
      <ServersManager {folderName}></ServersManager>
    </WindowSection>

    <WindowSection title="Zone critique">
      <WindowButton
        onclick={async () => {
          await onClickSupprimer();
        }}>Supprimer</WindowButton
      >
    </WindowSection>
  </Window>
{/if}
