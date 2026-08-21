<script>
  import {
    getServer,
    postServer,
  } from "$lib/components/recurentActions.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { untrack } from "svelte";
  import Confirm from "../baseComponents/Confirm.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";
  import { stats } from "$lib/stores/stats.svelte";

  const uuid = $derived(uiStore.currentUuid);
  let serverName = $state("Chargement...");

  $effect(async () => {
    uuid;
    if (!uuid) return;
    const name = await getServer(uuid, "name");
    serverName = name.name;
  });

  async function softDeleteServer() {
    const result = await postServer(uuid, "softDelete");
    await folderSystem.removeServer(result.uuid);
    await stats.removeRecentServer(result.uuid);
  }
</script>

<Confirm
  title="Suppression de serveur"
  description={`Le serveur '${serverName}' sera supprimé immédiatement. Une copie de sécurité sera conservée 15 jours en cas d'erreur, après quoi elle sera définitivement effacée.`}
  onConfirm={softDeleteServer}
  name="serverDeletionConfirm"
/>
