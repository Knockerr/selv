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
  import { onMount, untrack } from "svelte";
  import WindowAligned from "../../WindowAligned.svelte";
  import WindowSlider from "../../WindowSlider.svelte";
  import { windowsManager } from "../../windowsManager.svelte";
  import WindowDropdown from "../../WindowDropdown.svelte";

  const { refreshFoldersFunction } = $props(); 

  let windowId = "ServerCreationWindow";

  // TODO : mettre des valeurs de base

  const availableServerTypes = $state(["vanilla", "spigot", "paper", "forge"]);
  const availableVersions = $state([
    "1.8.9",
    "1.9.4",
    "1.10.2",
    "1.11.2",
    "1.12.2",
    "1.13.2",
    "1.14.4",
    "1.15.2",
    "1.16.5",
    "1.17.1",
    "1.18.2",
    "1.19.4",
    "1.20.5",
    "1.21.9",
  ]);

  // récuperation des attributs du serveur
  let serverName = $state("");
  let serverType = $state("");
  let serverVersion = $state("");
  let allocatedRam = $state("");

  // + UUID, creationDate, lastUseDate

  async function onServerCreationClick() {
    windowsManager.closeAll();

    const response = await fetch(`http://localhost:8000/api/servers/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: serverName,
        ram: allocatedRam,
        version: serverVersion,
        type: serverType,
      }),
    });

    const data = await response.json();

    await folderSystem.addServer(data.uuid);

    windowsManager.closeAll();

    refreshFoldersFunction();
  }

  const isOpen = $derived(windowsManager.openWindows.has(windowId));
  $effect(() => {
    isOpen;
    untrack(() => {
      console.error("JE veux m'ouvrir!");
    });
  });
</script>

{#if isOpen}
  <Window height="60%" width="30%" title={"Création de serveur"} {windowId}>
    <WindowLabel>
      Enter your new server's specifications and parameters!
    </WindowLabel>
    <WindowSection title="Le serveur">
      <WindowAligned>
        <WindowLabel>Nom du serveur:</WindowLabel>
        <WindowTextInput bind:value={serverName}></WindowTextInput>
      </WindowAligned>
      <WindowAligned>
        <WindowLabel>Type de serveur:</WindowLabel>
        <WindowDropdown bind:value={serverType} options={availableServerTypes}
        ></WindowDropdown>
      </WindowAligned>
      <WindowAligned>
        <WindowLabel>Version du serveur:</WindowLabel>
        <WindowDropdown bind:value={serverVersion} options={availableVersions}
        ></WindowDropdown>
      </WindowAligned>
    </WindowSection>
    <WindowSection title="Technique :">
      <WindowLabel>Ram allouée (en Go)</WindowLabel>
      <WindowTextInput bind:value={allocatedRam} placeholder={"4"} />
    </WindowSection>
    <WindowButton onclick={onServerCreationClick}>Créer</WindowButton>
  </Window>
{/if}
