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

  let { currentAction = $bindable(), email = $bindable(), onvalidation } = $props();

  let otpInput = $state();
  let loading = $state(false);

  async function checkForTotp() {
    // Return true if need totp, false otherwise
    const { data, error } =
      await supabase.auth.mfa.getAuthenticatorAssuranceLevel();
    const { currentLevel, nextLevel, currentAuthenticationMethods } = data;
    if (currentLevel == "aal1" && nextLevel == "aal2") {
      currentAction = "totpValidation";
      return true;
    }
    return false;
  }

  async function checkOtp() {
    if (!email) return;
    loading = true;
    const { data, error } = await supabase.auth.verifyOtp({
      email: email,
      token: otpInput,
      type: "email",
    });
    if (error) {
      console.error("Error whilst validating OTP:", error);
      loading = false;
      return;
    }
    onvalidation()
  }
</script>

<AuthCard>
  <div class="content">
    <div class="titleSection">
      <h1 class="title">Vérification d'adresse mail</h1>
      <span class="subtitle"
        >Un code de vérification a été envoyé à votre adresse e-mail "[EMAIL]".
        Entrez ce code ici</span
      >
    </div>
    <Input
      label="Code de vérification"
      placeholder="123456"
      bind:value={otpInput}
    />

    <Button onclick={checkOtp} iconPath={pathDb.arrowRight} emphasize
      >Vérifier</Button
    >

    <Button
      iconPath={pathDb.undo}
      onclick={() => {
        currentAction = "signup";
      }}
    >
      Modifier l'adresse mail
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
