<script>
  import { pathDb } from "$lib/icons/pathDb";
  import { minecraftVersions } from "$lib/serversInfosDb";
  import { online } from "svelte/reactivity/window";
  import Button from "../baseComponents/Button.svelte";
  import ComboBox from "../baseComponents/ComboBox.svelte";
  import Dialog from "../baseComponents/dialog.svelte";
  import Input from "../baseComponents/Input.svelte";
  import Select from "../baseComponents/select.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";

  const { refreshFoldersFunction } = $props();

  let currentName = $state("");
  let currentVersion = $state("");
  let currentType = $state("");
  let currentRam = $state("");

  const allMinecraftVersions = Object.keys(minecraftVersions);
  const availableVersions = $derived.by(() => {
    let temp = [];
    allMinecraftVersions.forEach((version) => {
      if (minecraftVersions[version].availableTypes.includes(currentType))
        temp.push(version);
    });
    return temp;
  });

  const availableVersionItems = $derived.by(() => {
    let temp = [];
    if (availableVersions === undefined) return;
    availableVersions.forEach((version) => {
      temp.push({
        label: version,
        value: version,
      });
    });
    return temp;
  });

  const availableTypesItems = [
    {
      value: "vanilla",
      label: "défaut",
    },
    {
      value: "spigot",
      label: "Spigot",
    },
    {
      value: "paper",
      label: "Paper",
    },
    {
      value: "forge",
      label: "Forge",
    },
  ];

  async function onServerCreationClick() {
    const response = await fetch(`http://localhost:8000/api/servers/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: currentName,
        ram: parseInt(currentRam),
        version: currentVersion,
        type: currentType,
      }),
    });

    const data = await response.json();

    await folderSystem.addServer(data.uuid);

    refreshFoldersFunction();
  }
</script>

<Dialog
  title="Création de serveur"
  description="Entrez les specifications et les paramètres de votre serveur."
>
  {#snippet triggerButton()}
    <Button iconPath={pathDb.plus} iconSize="18" emphasize={true}
      >Créer un serveur</Button
    >
  {/snippet}

  <Input
    placeholder="Serveur du [userName] //TODO"
    label="Nom du serveur"
    width="calc(100% - 2rem)"
    iconPath={pathDb.pencil}
    bind:value={currentName}
  ></Input>

  <Select
    items={availableTypesItems}
    label="Type de serveur"
    placeholder="Choisissez le type de serveur"
    bind:value={currentType}
  ></Select>

  <ComboBox
    placeholder="Entrez la version"
    items={availableVersionItems}
    label="Version de votre serveur"
    iconPath={pathDb.pencil}
    type="single"
    bind:value={currentVersion}
  />

  <Input
    placeholder="8"
    label="Ram allouée au serveur"
    width="calc(100% - 2rem)"
    iconPath={pathDb.hardDrives}
    bind:value={currentRam}
  ></Input>

  {#snippet closeButton()}
    <Button iconPath={pathDb.plus} onclick={onServerCreationClick}>Créer</Button
    >
  {/snippet}
</Dialog>
