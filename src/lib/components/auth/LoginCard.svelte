<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import Button from "../bits-ui/baseComponents/Button.svelte";
  import Input from "../bits-ui/baseComponents/Input.svelte";
  import AuthCard from "./AuthCard.svelte";
  import ClickableText from "../bits-ui/baseComponents/ClickableText.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";

  let password = $state("");

  let { currentAction = $bindable(), email = $bindable(), onlogin } = $props();

  async function login() {
    console.log("Trying to log user in");

    const { data, error } = await supabase.auth.signInWithPassword({
      email: email,
      password: password,
    });
    if (error) {
      console.error(error);
      return;
    }
    onlogin()
  }
</script>

<AuthCard>
  <div class="content">
    <div class="titleSection">
      <h1 class="title">Bon retour!</h1>
      <span class="subtitle">Entrez vos informations pour vous connecter</span>
    </div>

    <div class="inputsContainer">
      <Input
        label="Adresse email"
        bind:value={email}
        placeholder="Email"
        labelProps={{ style: "font-size:0.95rem;" }}
      />
      <Input
        label="Mot de passe"
        password
        bind:value={password}
        placeholder="Password"
        labelProps={{ style: "font-size:0.95rem;" }}
      />
      <Button
        emphasize
        width="100%"
        height="40px"
        onclick={login}
        style="font-size:0.95rem; font-weight: 500;">Se connecter</Button
      >
      <ClickableText
        style="font-size:0.95rem; align-self:center;"
        onclick={() => {
          currentAction = "signup";
        }}>Je n'ai pas de compte</ClickableText
      >
      <ClickableText
        style="font-size:0.95rem; align-self:center;"
        onclick={() => {
          alert("En développement. Contacter le support.");
        }}>J'ai oublié mon mot de passe</ClickableText
      >
    </div>
  </div>
</AuthCard>

<style>
  .content {
    display: flex;
    flex-direction: column;
    gap: 30px;
    width: 100%;
    height: fit-content;
  }

  .titleSection {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .title {
    width: 100%;
    margin: 0;
    color: var(--foreground);
    font-size: 2.1rem;
  }

  .subtitle {
    width: 100%;
    margin: 0;
    color: var(--foreground-alt);
    font-size: 0.95rem;
  }

  .inputsContainer {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
</style>
