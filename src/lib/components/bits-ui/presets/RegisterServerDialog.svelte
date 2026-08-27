<script>
  import {
    getExternalBackend,
    postServerWithCredentials,
  } from "$lib/components/recurentActions.svelte";
  import { onMount } from "svelte";
  import Button from "../baseComponents/Button.svelte";
  import Confirm from "../baseComponents/Confirm.svelte";
  import { uiStore } from "../uiComponentsStore.svelte";
  import Input from "../baseComponents/Input.svelte";
  import IpInput from "./IpInput.svelte";

  const { uuid, onregister } = $props();

  let domain = $state("");
  let domainAvailable = $state(null);

  let error = $state("");

  function checkIpFormat() {
    const regex = /^(?![0-9-]+$)[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/i;
    return regex.test();
  }

  async function updateDomainAvailability() {
    if (!domain) return;

    const isValid = checkIpFormat(domain);
    if (!isValid) {
      error = "Format d'ip non valide.";
      return;
    }

    const res = await getExternalBackend(`domains/${domain}/availability`);
    domainAvailable = res.available;
  }

  function registerServer() {
    postServerWithCredentials(uuid, "tunnel/register", {
      domain: domain,
    });
    onregister();
  }
</script>

<Confirm
  title="Activer la connexion à distance"
  description="Entrez une adresse IP que vos joueurs pourront utiliser pour se connecter à votre serveur."
  onConfirm={registerServer}
  name="registerServerDialog"
  confirmDisabled={!domainAvailable}
>
  <span>
    L'ip peut contenir des lettres minuscules (a-z), des chiffres (0-9) et des
    tirets(-)
  </span>
  {#if domainAvailable === false}
    <span class="unavalaible">Cette IP est déjà utilisée.</span>
  {:else if domainAvailable === true}
    <span class="avalaible">Disponible!</span>
  {/if}
  {#if error}
    <span class="unavalaible">{error}</span>
  {/if}
  <IpInput
    placeholder="nom-du-serveur"
    bind:value={domain}
    className="mt-0 mb-0 relative -top-2"
    onchange={() => {
      domainAvailable = null;
    }}
  />
  <Button className="-top-5" onclick={updateDomainAvailability}
    >Vérifier la disponibilité</Button
  >
</Confirm>

<style>
  span {
    color: var(--color-foreground-alt);
    font-size: 0.9rem;
  }

  .avalaible {
    color: var(--success);
  }
  .unavalaible {
    color: var(--dangerous);
  }
</style>
