<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Confirm from "$lib/components/bits-ui/baseComponents/Confirm.svelte";
  import InputDialog from "$lib/components/bits-ui/baseComponents/InputDialog.svelte";
  import LoadingDialog from "$lib/components/bits-ui/LoadingDialog.svelte";
  import PanelSettingsBlock from "$lib/components/bits-ui/presets/panelSettingsBlock.svelte";
  import PanelSettingsItem from "$lib/components/bits-ui/presets/panelSettingsItem.svelte";
  import RegisterServerDialog from "$lib/components/bits-ui/presets/RegisterServerDialog.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import {
    getExternalBackend,
    getServer,
    postServerWithCredentials,
  } from "$lib/components/recurentActions.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { onMount } from "svelte";

  sidebarStore.setCurrentTab("panel", "Connectivité");

  const params = new URLSearchParams(window.location.search);
  let uuid = params.get("uuid") ?? "demoUuid";

  let domainInput = $state("");
  let serverDomain = $state("");
  let isServerRegistered = $derived(serverDomain === null ? false : true);

  async function updateServerDomain() {
    const res = await getServer(uuid, "tunnel/domain");
    serverDomain = res.domain;
  }

  onMount(() => {
    updateServerDomain();
  });

  async function handleDomainChange() {
    if (!domainInput) return;
    uiStore.load();
    const res = await getExternalBackend(`domains/${domainInput}/availability`);
    uiStore.stopLoad();
    const domainAvailable = res.available;
    if (domainAvailable) {
      uiStore.openDialog("ipAvailability-available");
    } else {
      uiStore.openDialog("ipAvailability-unavailable");
    }
  }

  async function changeDomain() {
    await postServerWithCredentials(uuid, "tunnel/changeDomain", {
      newDomain: domainInput,
    });
    serverDomain = domainInput;
  }

  async function unregisterServer() {
    await postServerWithCredentials(uuid, "tunnel/unregister");
    serverDomain = null;
  }
</script>

<div class="page">
  <h1 class="title">Connectivité</h1>

  <div class="settingsContainer">
    <PanelSettingsBlock width="650px">
      {#if isServerRegistered}
        <PanelSettingsItem
          title="Connexion à distance"
          description="Désactiver la connexion à distance empêchera les joueurs de se connecter à votre serveur à distance."
          inputType="button"
          inputLabel="Désactiver"
          onclick={() => {
            uiStore.openDialog("unregisterServerDialog");
          }}
          emphasize
        ></PanelSettingsItem>
      {:else}
        <PanelSettingsItem
          title="Connexion à distance"
          description="Activez la connexion à distance pour que les joueurs puissent se connecter à votre serveur de manière sécurisée via une adresse IP."
          inputType="button"
          inputLabel="Activer"
          onclick={() => {
            uiStore.openDialog("registerServerDialog");
          }}
          emphasize
        ></PanelSettingsItem>
      {/if}
      <PanelSettingsItem
        title="Statut actuel"
        description="Informations relatives à la connexion à distance.."
        inputType="none"
        itemDisabled={!isServerRegistered}
      >
        <span>IP actuelle : {serverDomain}.nomLogiciel.com</span
        ></PanelSettingsItem
      >
      <PanelSettingsItem
        title="Ip de serveur"
        description="Choisissez l'ip utilisée par les joueurs pour se connecter à votre serveur. Si le serveur n'est pas lancé pendant 60 jours (ou durant les 7 jours suivant sa création), l'ip sera réinitialisée."
        inputType="ip"
        bind:value={domainInput}
        itemDisabled={!isServerRegistered}
      >
        <div class="w-full flex flex-row justify-end">
          <Button
            style="font-size: 0.8rem;"
            height="27px"
            onclick={handleDomainChange}>Disponibilité</Button
          >
        </div>
      </PanelSettingsItem>
    </PanelSettingsBlock>
  </div>
</div>

<Confirm
  title="Disponibilité d'IP"
  description={`L'ip ${domainInput} est disponible. Cliquez sur "Modifier" pour l'utiliser. Vous ne pourrez plus utiliser votre ancienne IP pour vous connecter à votre serveur et d'autres utilisasteurs pourront la réserver à leur tour.`}
  name="ipAvailability-available"
  confirmLabel="Modifier"
  onConfirm={changeDomain}
/>

<Confirm
  title="Disponibilité d'IP"
  description={`L'ip ${domainInput} est déjà utilisée par un autre utilisateur.`}
  name="ipAvailability-unavailable"
  confirmLabel="Compris"
/>

<Confirm
  title="Désactiver la connexion à distance"
  description={`Votre serveur ne sera plus accesible en dehors de votre réseau local et l'IP qui vous était attribuée pourra être réclamée par d'autres utilisateurs.`}
  name="unregisterServerDialog"
  confirmLabel="Compris"
  onConfirm={unregisterServer}
/>

<RegisterServerDialog {uuid} onregister={() => (serverDomain = domainInput)} />

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
