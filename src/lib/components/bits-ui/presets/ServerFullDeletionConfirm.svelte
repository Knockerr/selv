<script>
  import {
    getDeletedServer,
    getServer,
    postDeletedServer,
    postServer,
  } from "$lib/components/recurentActions.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { untrack } from "svelte";
  import Confirm from "../baseComponents/Confirm.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";

  const uuid = $derived(uiStore.currentUuid);
  let serverName = $state("Chargement...");

  let { open = $bindable(false) } = $props();

  $effect(async () => {
    uuid;
    if (!uuid) return;
    const serverDatas = await getDeletedServer(uuid, "datas");
    serverName = serverDatas.datas.name;
  });

  async function fullDeleteServer() {
    postDeletedServer(uuid, "fullDelete");
  }
</script>

<Confirm
  title="Suppression définitive de serveur"
  description={`Supprimez définitivement votre serveur '${serverName}' et toutes ces données. Cette action est instantanée et irréversible.`}
  onConfirm={fullDeleteServer}
  name="serverFullDeletionConfirm"
  bind:open
/>
