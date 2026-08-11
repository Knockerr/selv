<script>
  import { postServer } from "$lib/components/recurentActions.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import InputDialog from "../baseComponents/InputDialog.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";

  let dupName = $state("");

  const uuid = $derived(uiStore.currentUuid);

  async function duplicateServer() {
    const result = await postServer(uuid, "duplicate", { dupName: dupName });
    // Registering the new server on the frontend
    console.warn("result.newServerUuid", result.newServerUuid);
    await folderSystem.addServer(result.newServerUuid);
    uiStore.closeDialog("serverDuplicateDialog");
  }
</script>

<InputDialog
  bind:value={dupName}
  onConfirm={duplicateServer}
  title="Dupliquer le serveur"
  description="Entrez le nom de la copie de votre serveur."
  placeholder="Nom de la copie"
  name="serverDuplicateDialog"
/>
