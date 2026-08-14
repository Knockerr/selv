<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import Button from "../bits-ui/baseComponents/Button.svelte";
  import Input from "../bits-ui/baseComponents/Input.svelte";
  import AuthCard from "./AuthCard.svelte";
  import ClickableText from "../bits-ui/baseComponents/ClickableText.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";

  let { currentAction = $bindable(), email = $bindable() } = $props();

  let password = $state("");
  let confirmPassword = $state("");

  const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
      );
  };

  const emailCorrect = $derived(validateEmail(email));
  let emailInputColor = $derived(
    emailCorrect || !email ? "" : "var(--dangerous)",
  );
  const arePasswordIdentical = $derived(password == confirmPassword);
  let passwordInputColor = $derived(
    arePasswordIdentical ? "" : "var(--dangerous)",
  );

  async function signUp() {
    console.log("Trying to sign up new user");
    if (!email || !password) return;
    const { data, error } = await supabase.auth.signUp({
      email: email,
      password: password,
    });
    if (error) {
      console.error("error: ", error);
      return;
    }
    console.log("Sign up users data: ", data);
    currentAction = "emailValidation";
  }
</script>

<AuthCard>
  <div class="content">
    <div class="titleSection">
      <h1 class="title">Bienvenue!</h1>
      <span class="subtitle"
        >Entrez vos informations pour créer votre compte gratuitement.</span
      >
    </div>

    <div class="inputsContainer">
      <Input
        label="Adresse email"
        bind:value={email}
        placeholder="Email"
        labelProps={{ style: "font-size:0.95rem;" }}
        color={emailInputColor}
      />
      <Input
        label="Mot de passe"
        password
        bind:value={password}
        placeholder="Password"
        labelProps={{ style: "font-size:0.95rem;" }}
        color={passwordInputColor}
      />
      <Input
        label="Confirmer le mot de passe"
        password
        bind:value={confirmPassword}
        placeholder="Password"
        labelProps={{ style: "font-size:0.95rem;" }}
        color={passwordInputColor}
      />
      <Button
        emphasize
        width="100%"
        height="40px"
        disabled={!arePasswordIdentical || !password || !emailCorrect}
        onclick={signUp}
        style="font-size:0.95rem; font-weight: 500;">Créer le compte</Button
      >
      <ClickableText
        style="font-size:0.95rem; align-self:center;"
        onclick={() => {
          currentAction = "login";
        }}>J'ai déjà un compte</ClickableText
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
