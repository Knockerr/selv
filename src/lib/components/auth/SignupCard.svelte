<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import Button from "../bits-ui/baseComponents/Button.svelte";
  import Input from "../bits-ui/baseComponents/Input.svelte";
  import AuthCard from "./AuthCard.svelte";
  import ClickableText from "../bits-ui/baseComponents/ClickableText.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";
  import Checkbox from "../bits-ui/baseComponents/Checkbox.svelte";
  import { openUrl } from "@tauri-apps/plugin-opener";

  let { currentAction = $bindable(), email = $bindable() } = $props();

  let password = $state("");
  let confirmPassword = $state("");
  let username = $state("");

  let termsConditionCheckbox = $state(false);
  let ageCheckbox = $state(false);

  let passwordInputColor = $state("");
  let passwordCorrect = $state("");

  let emailInputColor = $state("");
  let emailCorrect = $state();

  let errorMessage = $state("");

  const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
      );
  };

  const validatePasswd = (passwd) => {
    return String(passwd).match(
      /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/,
    );
  };

  async function signUp() {
    justCreated = true;
    console.log("Trying to sign up new user");
    if (!email || !password) return;
    const { data, error } = await supabase.auth.signUp({
      email: email,
      password: password,
      options: {
        data: {
          username: username,
          profilePicture:
            "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png",
        },
      },
    });
    if (error) {
      console.error("error: ", error);
      return;
    }
    console.log("Sign up users data: ", data);
    currentAction = "emailValidation";
  }

  function evaluateEmail() {
    emailCorrect = email && validateEmail(email);
    if (!emailCorrect) {
      emailInputColor = "var(--dangerous)";
      errorMessage = "Mauvais format d'adresse mail.";
      return;
    }

    emailCorrect = true;
    errorMessage = "";
    emailInputColor = "";
  }

  function evaluatePassword() {
    const doPasswdFitRequirements = password && validatePasswd(password);
    if (!doPasswdFitRequirements) {
      passwordCorrect = false;
      errorMessage = "Le mot de passe ne répond pas aux exigences.";
      passwordInputColor = "var(--dangerous)";
      return;
    }

    const arePasswordIdentical = password == confirmPassword;
    if (!arePasswordIdentical) {
      passwordCorrect = false;
      errorMessage = "Les mots de passe sont différents.";
      passwordInputColor = "var(--dangerous)";
      return;
    }

    passwordCorrect = true;
    errorMessage = "";
    passwordInputColor = "";
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
        label="Nom d'utilisateur"
        bind:value={username}
        placeholder="Nom d'utilisateur"
        labelProps={{ style: "font-size:0.95rem;" }}
      />
      <Input
        label="Adresse email"
        bind:value={email}
        placeholder="Email"
        labelProps={{ style: "font-size:0.95rem;" }}
        color={emailInputColor}
        onblur={evaluateEmail}
      />
      <Input
        label="Mot de passe"
        requirements={[
          "Plus de 8 caractères",
          "Au moins une majuscule",
          "Au moins une minuscule",
          "Au moins un chiffre",
          "Au moins un caractère spécial",
        ]}
        password
        bind:value={password}
        placeholder="Password"
        labelProps={{ style: "font-size:0.95rem;" }}
        color={passwordInputColor}
        onblur={evaluatePassword}
      />
      <Input
        label="Confirmer le mot de passe"
        password
        bind:value={confirmPassword}
        placeholder="Password"
        labelProps={{ style: "font-size:0.95rem;" }}
        color={passwordInputColor}
        onblur={evaluatePassword}
      />
      {#if errorMessage}
        <p class="error">
          {errorMessage}
        </p>
      {/if}
      <Checkbox
        label="Accepter les conditions d'utilisation et la politique de confidentialité."
        bind:checked={termsConditionCheckbox}
        id="terms"
      >
        {#snippet labelSnippet()}
          Accepter les <ClickableText
            onclick={() => {
              openUrl("https://docs.selvmc.com/informations/cgu");
            }}
            style="font-size: inherit; font-family: inherit; font-weight: inherit; color: inherit"
            >conditions d'utilisation</ClickableText
          >
          et la <ClickableText
            onclick={() => {
              openUrl("https://docs.selvmc.com/informations/terms");
            }}
            style="font-size: inherit; font-family: inherit; font-weight: inherit; color: inherit"
            >politique de confidentialité</ClickableText
          >
        {/snippet}
      </Checkbox>
      <Checkbox
        id="age"
        bind:checked={ageCheckbox}
        label="J'ai au moins 15 ans, ou j'ai l'autorisation de mon représentant légal."
      />
      <Button
        emphasize
        width="100%"
        height="40px"
        disabled={!passwordCorrect ||
          !emailCorrect ||
          !ageCheckbox ||
          !termsConditionCheckbox}
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

  .error {
    color: var(--dangerous);
    margin: 0;
    font-size: 0.8rem;
  }
</style>
