<script>
  import { pathDb } from "$lib/icons/pathDb";
  import Button from "../baseComponents/Button.svelte";
  import ComboBox from "../baseComponents/ComboBox.svelte";
  import Dialog from "../baseComponents/dialog.svelte";
  import Input from "../baseComponents/Input.svelte";
  import Select from "../baseComponents/select.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";
  import { getMinecraftVersions } from "$lib/manifestsManager.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";

  const { refreshFoldersFunction } = $props();

  let minecraftVersions = $derived(getMinecraftVersions());

  let currentName = $state("");
  let currentVersion = $state("");
  let currentType = $state("");
  let currentRam = $state("");

  const availableVersionItems = $derived.by(() => {
    if (!minecraftVersions || !currentType) return;
    let temp = [];
    minecraftVersions[currentType].versions.forEach((version) => {
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
      label: "Vanilla",
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
    uiStore.load("Téléchargement des fichiers");
    const { data, error } = await supabase.auth.getSession();
    if (error) {
      console.error("Can't get user");
      return;
    }
    const uid = await data?.session.user.id;

    console.warn("data > ", data);
    console.warn("UID > ", uid);

    const response = await fetch(`http://localhost:40401/api/servers/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: currentName,
        ram: parseInt(currentRam),
        version: currentVersion,
        type: currentType,
        owner: uid,
      }),
    });

    const sData = await response.json();

    await folderSystem.addServer(sData.uuid);

    uiStore.stopLoad();

    refreshFoldersFunction();
  }
</script>

<Dialog
  title="Création de serveur"
  description="Entrez les specifications et les paramètres de votre serveur."
  name="createServerDialog"
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
    iconPath={pathDb.gears}
  ></Select>

  <ComboBox
    placeholder="Entrez la version"
    items={availableVersionItems}
    label="Version de votre serveur"
    iconPath={pathDb.hash}
    type="single"
    bind:value={currentVersion}
  />

  <Input
    placeholder="8"
    defaultValue="8"
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
