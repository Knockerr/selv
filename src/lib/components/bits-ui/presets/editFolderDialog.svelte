<script>
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { untrack } from "svelte";
  import Button from "../baseComponents/Button.svelte";
  import ComboBox from "../baseComponents/ComboBox.svelte";
  import Dialog from "../baseComponents/dialog.svelte";
  import IconButton from "../baseComponents/iconButton.svelte";
  import Input from "../baseComponents/Input.svelte";
  import Item from "../baseComponents/item.svelte";
  import Select from "../baseComponents/select.svelte";
  import Switch from "../baseComponents/switch.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";
  import ServersManager from "./presetSpecificComponents/ServersManager.svelte";

  const componentName = `editFolderDialog`;
  const folderName = $derived(uiStore.currentEditedFolder);

  $inspect(folderName).with(() => {
    console.info("folderName", folderName);
  });

  let switchRef = $state();
  let newName = $state("");

  let dialogOpen = $state(false);
  let dialogOpenTrigger = $derived(uiStore.isDialogOpen(componentName));
  $effect(() => {
    let _ = dialogOpenTrigger;
    if (dialogOpenTrigger) {
      dialogOpen = true;
    }
  });
  $effect(() => {
    let _ = dialogOpen;
    if (!dialogOpen) {
      uiStore.closeDialog(componentName);
    }
  });

  let isFolderFav = $derived(
    folderSystem.getFolderData(folderName)?.isFolderFav || false,
  );
  let isFolderFavInput = $state(untrack(() => isFolderFav));

  $effect(() => {
    if (isFolderFavInput !== isFolderFav) {
      folderSystem.setFavoriteValue(folderName, isFolderFavInput);
    }
  });

  async function onRenameClick() {
    await folderSystem.getFolder(folderName).rename(newName);
    dialogOpen = false;
  }

  async function onDeleteClick() {
    await folderSystem.delete(folderName);
    dialogOpen = false;
  }
</script>

<Dialog
  title="Édition de dossier"
  description="Entrez et/ou modifiez les paramètres de votre dossier à votre convenance."
  bind:open={dialogOpen}
>
  <Item
    title="Favori"
    description="Un serveur mis en favoris apparait dans la partie supérieur"
    onclick={switchRef.toggle}
  >
    {#snippet input()}
      <Switch bind:this={switchRef} bind:checked={isFolderFavInput} />
    {/snippet}
  </Item>

  <div class="flex flex-col gap-0.5">
    <Input
      placeholder="Nouveau nom"
      iconPath={pathDb.pencil}
      label="Renommer le dossier"
      className="max-w-[calc(100% - 2rem)]"
      bind:value={newName}
    />
    <div class="flex flex-row w-full justify-start">
      <Button iconPath={pathDb.wrench} onclick={onRenameClick}>Renommer</Button>
    </div>
  </div>

  <ServersManager {folderName} />

  <div class="flex flex-rox justify-start">
    <Button label="Supprimer le dossier" onclick={onDeleteClick}
      >Supprimer</Button
    >
  </div>
</Dialog>
