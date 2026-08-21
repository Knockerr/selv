<script>
  import { goto } from "$app/navigation";
  import EmailValidationCard from "$lib/components/auth/EmailValidationCard.svelte";
  import LoginCard from "$lib/components/auth/LoginCard.svelte";
  import SignupCard from "$lib/components/auth/SignupCard.svelte";
  import TotpValidationCard from "$lib/components/auth/TotpValidationCard.svelte";
  import Loader from "$lib/components/bits-ui/baseComponents/Loader.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";
  import { onMount, untrack } from "svelte";

  let currentAction = $state("loading");
  let email = $state("");

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

  async function redirect() {
    currentAction = "loading";
    // Redirect to MFA page if needed
    const needTotp = await checkForTotp();
    if (needTotp) {
      currentAction = "totpValidation";
      return;
    } else {
      goto("/core/dashboard");
    }
  }

  onMount(async () => {
    currentAction = "loading";
    const { error } = await supabase.auth.getUser();
    const needTotp = await checkForTotp();
    if (!error) {
      if (needTotp) {
        currentAction = "totpValidation";
        return;
      }
      goto("/core/dashboard");
    } else {
      currentAction = "login";
    }
  });
</script>

<div class="page">
  {#if currentAction == "loading"}
    <Loader width="150px" height="150px" />
  {:else if currentAction == "login"}
    <LoginCard bind:currentAction bind:email onlogin={redirect} />
  {:else if currentAction == "signup"}
    <SignupCard bind:currentAction bind:email />
  {:else if currentAction == "emailValidation"}
    <EmailValidationCard
      bind:email
      bind:currentAction
      onvalidation={redirect}
    />
  {:else if currentAction == "totpValidation"}
    <TotpValidationCard bind:currentAction />
  {/if}
</div>

<style>
  .page {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 100%;
  }
</style>
