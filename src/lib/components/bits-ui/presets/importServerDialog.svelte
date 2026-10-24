<script>
  import { open } from "@tauri-apps/plugin-dialog";
  import { pathDb } from "$lib/icons/pathDb";
  import { getMinecraftVersions } from "$lib/ServersVersionHandler.svelte.js";
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
  let currentPath = $state("");

  let minecraftVersions = $derived(getMinecraftVersions());

  const availableVersionItems = $derived.by(() => {
    if (!minecraftVersions) return;
    let temp = [];
    minecraftVersions[currentVersion].versions.forEach((version) => {
      temp.push({
        label: version.id,
        value: version.id,
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

  async function selectFolderDir() {
    const input = await open({
      directory: true,
    });
    if (input !== undefined) currentPath = input;
    console.warn(currentPath);
  }

  async function onServerImportClick() {
    console.warn(currentName);
    console.warn(currentRam);
    console.warn(currentVersion);
    console.warn(currentType);
    console.warn(currentPath);
    const response = await fetch(`http://localhost:8000/api/servers/import`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: currentName,
        ram: parseInt(currentRam),
        version: currentVersion,
        type: currentType,
        path: currentPath.toString(),
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      console.error("Erreur 422 :", JSON.stringify(error, null, 2));
      return;
    }

    const data = await response.json();

    await folderSystem.addServer(data.uuid);

    refreshFoldersFunction();
  }
</script>

<Dialog
  title="Import de serveur"
  description="Entrez les specifications et les paramètres de votre serveur."
  name="importServerDialog"
>
  {#snippet triggerButton()}
    <Button iconPath={pathDb.download} iconSize="18" emphasize={false}
      >Importer un serveur</Button
    >
  {/snippet}

  <Input
    placeholder="Serveur du [userName] //TODO"
    label="Nom du serveur"
    className="max-w-[calc(100% - 2rem)]"
    iconPath={pathDb.pencil}
    bind:value={currentName}
  ></Input>

  <Select
    items={availableTypesItems}
    label="Type de serveur"
    placeholder="Sélectionnez le type de votre serveur"
    bind:value={currentType}
    iconPath={pathDb.gears}
  ></Select>

  <ComboBox
    placeholder="Entrez la version"
    items={availableVersionItems}
    label="Sélectionnez la version de votre serveur"
    iconPath={pathDb.hash}
    type="single"
    bind:value={currentVersion}
  />

  <Input
    placeholder="8"
    label="Ram allouée au serveur"
    className="max-w-[calc(100% - 2rem)]"
    iconPath={pathDb.hardDrives}
    bind:value={currentRam}
  ></Input>

  <Button
    iconPath={pathDb.folder}
    onclick={async () => {
      await selectFolderDir();
    }}>Dossier du serveur</Button
  >

  {#snippet closeButton()}
    <Button iconPath={pathDb.plus} onclick={onServerImportClick}
      >Importer</Button
    >
  {/snippet}
</Dialog>
