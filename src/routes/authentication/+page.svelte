<script>
  import { goto } from "$app/navigation";
  import EmailValidationCard from "$lib/components/auth/EmailValidationCard.svelte";
  import LoginCard from "$lib/components/auth/LoginCard.svelte";
  import SignupCard from "$lib/components/auth/SignupCard.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";
  import { onMount } from "svelte";

  let currentAction = $state("signup");
  let email = $state("");

  onMount(async () => {
    const { error } = await supabase.auth.getUser();
    if (!error) {
        goto("/core/dashboard")
    }
  });
</script>

<div class="page">
  {#if currentAction == "login"}
    <LoginCard bind:currentAction bind:email />
  {:else if currentAction == "signup"}
    <SignupCard bind:currentAction bind:email />
  {:else if currentAction == "emailValidation"}
    <EmailValidationCard bind:email bind:currentAction />
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
