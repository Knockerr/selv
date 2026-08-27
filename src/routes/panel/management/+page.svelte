<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Confirm from "$lib/components/bits-ui/baseComponents/Confirm.svelte";
  import InputDialog from "$lib/components/bits-ui/baseComponents/InputDialog.svelte";
  import LoadingDialog from "$lib/components/bits-ui/LoadingDialog.svelte";
  import PanelSettingsBlock from "$lib/components/bits-ui/presets/panelSettingsBlock.svelte";
  import PanelSettingsItem from "$lib/components/bits-ui/presets/panelSettingsItem.svelte";
  import ServersManager from "$lib/components/bits-ui/presets/presetSpecificComponents/ServersManager.svelte";
  import RegisterServerDialog from "$lib/components/bits-ui/presets/RegisterServerDialog.svelte";
  import ServerDeletionConfirm from "$lib/components/bits-ui/presets/ServerDeletionConfirm.svelte";
  import ServerDuplicateDialog from "$lib/components/bits-ui/presets/ServerDuplicateDialog.svelte";
  import ServerRenameDialog from "$lib/components/bits-ui/presets/ServerRenameDialog.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import {
    formatSeconds,
    getExternalBackend,
    getServer,
    postServerWithCredentials,
  } from "$lib/components/recurentActions.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { onMount } from "svelte";

  sidebarStore.setCurrentTab("panel", "Gestion");

  const params = new URLSearchParams(window.location.search);
  let uuid = params.get("uuid") ?? "demoUuid";

  let infos = {};

  onMount(async () => {
    const data = await getServer(uuid, "datas");
    const serverDatas = data.datas;

    const lastUseDate = new Date(serverDatas.last_use_date);
    let lastUseDateFormatted = lastUseDate.toLocaleString("fr-FR", {
      dateStyle: "long",
      timeStyle: "short",
    });

    const creationDate = new Date(serverDatas.creation_date);
    let creationDateFormatted = creationDate.toLocaleString("fr-FR", {
      dateStyle: "long",
      timeStyle: "short",
    });

    infos = {
      name: serverDatas.name,
      type: serverDatas.server_type,
      version: serverDatas.version,
      ram: serverDatas.max_ram,
      path: serverDatas.path,
      uptime: formatSeconds(serverDatas.uptime),
      lastUse: lastUseDateFormatted,
      creationDate: creationDateFormatted,
      port: serverDatas.local_port,
    };
  });
</script>

<div class="page">
  <h1 class="title">Gestion</h1>

  <div class="settingsContainer">
    <PanelSettingsBlock width="650px">
      <PanelSettingsItem
        title="Renommer le serveur"
        description="Changez le nom de votre serveur (à la fois dans l'interface et dans les fichiers) dès maintenant."
        inputType="button"
        inputLabel="Renommer"
        onclick={() => {
          uiStore.openDialog("serverRenameDialog");
        }}
      ></PanelSettingsItem>
      <PanelSettingsItem
        title="Dupliquer le serveur"
        description="Créer un doublon de votre serveur. Cette option ne devrait pas être utilisée pour créer des sauvegardes."
        inputType="button"
        inputLabel="Dupliquer"
        onclick={() => {
          uiStore.openDialog("serverDuplicateDialog");
        }}
      ></PanelSettingsItem>
      <PanelSettingsItem
        title="Informations"
        description="Informations concernant votre serveur."
        inputType="none"
      >
        <div class="infosContainer">
          <span>Identifiant: {uuid}</span>
          <span>Nom: {infos.name}</span>
          <span>Moteur: {infos.type}</span>
          <span>Version: {infos.version}</span>
          <span>Ram attribuée: {infos.ram}</span>
          <span>Port local: {infos.port}</span>
          <span>Chemin local: {infos.path}</span>
          <span>Temps d'utilisation total: {infos.uptime}</span>
          <span>Dernière utilisation: {infos.lastUse}</span>
          <span>Création: {infos.creationDate}</span>
        </div>
      </PanelSettingsItem>
    </PanelSettingsBlock>
  </div>
</div>

<ServerDuplicateDialog />
<ServerRenameDialog />

<style>
  .page {
    height: 100%;
    width: 100%;
  }

  .title {
    width: 100%;
    padding: 25px 70px;
    box-sizing: border-box;
    font-family: var(--robotFont);
    font-size: 3rem;
    font-weight: 500;
  }

  .settingsContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .infosContainer {
    display: flex;
    flex-direction: column;
    max-width: 300px;
    gap: 5px;
  }

  .infosContainer > span {
    color: var(--color-foreground-alt);
    font-size: 0.9rem;
  }
</style>
