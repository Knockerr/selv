<script>
  import { goto } from "$app/navigation";
  import { onDestroy, onMount } from "svelte";
  import { fly } from "svelte/transition";
  import Button from "../bits-ui/baseComponents/Button.svelte";
  import Input from "../bits-ui/baseComponents/Input.svelte";
  import AuthCard from "./AuthCard.svelte";
  import ClickableText from "../bits-ui/baseComponents/ClickableText.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import Select from "../bits-ui/baseComponents/select.svelte";

  let { currentAction = $bindable() } = $props();

  let totpInput = $state("");
  let loading = $state(false);
  let availableFactorsItems = $state([]);
  let factorId = $state("");

  onMount(async () => {
    const { data, error } = await supabase.auth.mfa.listFactors();
    if (error) {
      console.error("Impossible to list factors: ", error);
    }
    data.totp.forEach((factor) => {
      availableFactorsItems.push({
        label: factor.friendly_name,
        value: factor.id,
        disabled: false,
      });
    });
  });

  async function checkTotp() {
    if (!factorId) return;

    loading = true;
    const { data, error } = await supabase.auth.mfa.challengeAndVerify({
      factorId: factorId,
      code: totpInput,
    });

    if (error) {
      console.error("Error whilst validating TOTP:", error);
      loading = false;
      return;
    }
    goto("/core/dashboard");
  }
</script>

<AuthCard>
  <div class="content">
    <div class="titleSection">
      <h1 class="title">Authentification à deux facteurs</h1>
      <span class="subtitle"
        >Entrez le code visible sur votre application d'authentification.</span
      >
    </div>
    <div class="flex flex-row w-full content-start">
      <Select
        items={availableFactorsItems}
        bind:value={factorId}
        width="200px"
        iconPath={pathDb.threeDotsVertical}
        label="Application d'authentification"
        style="margin: 0!important;"
      />
    </div>

    <Input
      label="Code de vérification"
      placeholder="123456"
      bind:value={totpInput}
    />

    <Button onclick={checkTotp} iconPath={pathDb.arrowRight} emphasize
      >Vérifier</Button
    >

    <Button
      iconPath={pathDb.undo}
      onclick={() => {
        currentAction = "login";
      }}
    >
      Changer de compte
    </Button>
  </div>
</AuthCard>

<style>
  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 30px;
    width: 100%;
    height: fit-content;
  }

  .titleSection {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .title {
    width: 100%;
    margin: 0;
    color: var(--foreground);
    font-size: 2.1rem;
  }

  .subtitle {
    width: 90%;
    margin: 0;
    color: var(--foreground-alt);
    font-size: 0.95rem;
  }
</style>
