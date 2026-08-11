<script>
  import {
    getServer,
    postServer,
  } from "$lib/components/recurentActions.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import Confirm from "../baseComponents/Confirm.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";

  const uuid = $derived(uiStore.currentUuid);
  const serverName = $derived(async () => await getServer(uuid, "name"));

  async function softDeleteServer() {
    const result = await postServer(uuid, "softDelete");
    folderSystem.removeServer(result.uuid);
  }
</script>

<Confirm
  title="Suppression de serveur"
  description={`Le serveur ${serverName} sera supprimé immédiatement. Une copie de sécurité sera conservée 15 jours en cas d'erreur, après quoi elle sera définitivement effacée.`}
  onConfirm={softDeleteServer}
  name="serverDeletionConfirm"
/>
