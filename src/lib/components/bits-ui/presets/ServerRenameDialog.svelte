<script>
  import { postServer } from "$lib/components/recurentActions.svelte";
  import InputDialog from "../baseComponents/InputDialog.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";

  let newName = $state("");

  const uuid = $derived(uiStore.currentUuid);

  function renameServer() {
    postServer(uuid, "rename", { newName: newName });
    /* TODO :  When created throw a toast here with a undo button
     to not have a modal that would cause too much friction but offers
     a undo option

    */
    uiStore.closeDialog("serverRenameDialog")
  }
</script>

<InputDialog
  bind:value={newName}
  onConfirm={renameServer}
  title="Renommer le serveur"
  description="Entrez le nouveau nom de votre serveur."
  placeholder="Nouveau nom"
  name="serverRenameDialog"
/>
