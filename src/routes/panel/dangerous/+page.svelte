<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Confirm from "$lib/components/bits-ui/baseComponents/Confirm.svelte";
  import InputDialog from "$lib/components/bits-ui/baseComponents/InputDialog.svelte";
  import LoadingDialog from "$lib/components/bits-ui/LoadingDialog.svelte";
  import PanelSettingsBlock from "$lib/components/bits-ui/presets/panelSettingsBlock.svelte";
  import PanelSettingsItem from "$lib/components/bits-ui/presets/panelSettingsItem.svelte";
  import RegisterServerDialog from "$lib/components/bits-ui/presets/RegisterServerDialog.svelte";
  import ServerDeletionConfirm from "$lib/components/bits-ui/presets/ServerDeletionConfirm.svelte";
  import ServerDuplicateDialog from "$lib/components/bits-ui/presets/ServerDuplicateDialog.svelte";
  import ServerRenameDialog from "$lib/components/bits-ui/presets/ServerRenameDialog.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import {
    getExternalBackend,
    getServer,
    postServerWithCredentials,
  } from "$lib/components/recurentActions.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { onMount } from "svelte";

  sidebarStore.setCurrentTab("panel", "Dangereux");

  const params = new URLSearchParams(window.location.search);
  let uuid = params.get("uuid") ?? "demoUuid";

  onMount(() => {});
</script>

<div class="page">
  <h1 class="title">Dangereux</h1>

  <div class="settingsContainer">
    <PanelSettingsBlock width="650px">
      <PanelSettingsItem
        title="Supprimer le serveur"
        description="Supprimez votre serveur. Vous aurez 15 jours pour le restorer après quoi tous ses fichiers et toutes ses informations seront supprimées définitivement."
        inputType="button"
        inputLabel="Supprimer"
        onclick={() => {
          uiStore.openDialog("serverDeletionConfirm");
        }}
        dangerous
      ></PanelSettingsItem>
    </PanelSettingsBlock>
  </div>
</div>

<ServerDeletionConfirm />


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
</style>
