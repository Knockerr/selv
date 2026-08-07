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
  import Confirm from "../baseComponents/Confirm.svelte";

  const componentName = `editFolderDialog`;
  const folderName = $derived(uiStore.currentEditedFolder);

  let open = $state(false);

  $inspect(folderName).with(() => {
    console.info("folderName", folderName);
  });

  let switchRef = $state();
  let newName = $state("");

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
    open = false;
  }

  async function onDeleteClick() {
    await folderSystem.delete(folderName);
    open = false;
  }
</script>

<Dialog
  title="Édition de dossier"
  description="Entrez et/ou modifiez les paramètres de votre dossier à votre convenance."
  name={componentName}
  bind:open
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
    <Confirm
      onConfirm={onDeleteClick}
      title="Supression de dossier"
      description="Êtes vous sûr de vouloir supprimer ce dossier? Vous perdrez votre configuration actuelle."
    >
      {#snippet triggerButton()}
        <Button label="Supprimer le dossier">Supprimer</Button>
      {/snippet}
    </Confirm>
  </div>
</Dialog>
