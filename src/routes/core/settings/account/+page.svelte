<script>
  import { goto } from "$app/navigation";
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Confirm from "$lib/components/bits-ui/baseComponents/Confirm.svelte";
  import Dialog from "$lib/components/bits-ui/baseComponents/dialog.svelte";
  import Input from "$lib/components/bits-ui/baseComponents/Input.svelte";
  import InputDialog from "$lib/components/bits-ui/baseComponents/InputDialog.svelte";
  import SaveSnackbar from "$lib/components/bits-ui/baseComponents/SaveSnackbar.svelte";
  import Switch from "$lib/components/bits-ui/baseComponents/switch.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import SettingsBlock from "$lib/components/core/settings/SettingsBlock.svelte";
  import SettingsItem from "$lib/components/core/settings/SettingsItem.svelte";
  import SettingsPageBase from "$lib/components/core/settings/SettingsPageBase.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";
  import { onMount } from "svelte";

  // TODO : add new password confirmation

  let email = $state("");
  let newPassword = $state("");
  let oldPassword = $state("");

  let emailInput = $state("");

  async function updateUserProperty(property) {
    const { data, error } = await supabase.auth.updateUser(property);
    if (error) {
      console.error("Error whilst trying to edit user property: ", error);
      return;
    }
  }

  async function getUserProperties() {
    const { data, error } = await supabase.auth.getUser();
    if (error) {
      console.error("Error whilst trying to edit user property: ", error);
      return;
    }
    return data;
  }

  async function signOut() {
    console.log("User trying to sign out");
    const { error } = await supabase.auth.signOut();
    if (error) {
      console.error("Error on user signout: ", error);
    }
    console.log("User signed out succesfully");
    goto("/authentication");
  }

  onMount(async () => {
    const data = await getUserProperties();
    const userData = data.user;
    email = userData.email;
  });
</script>

<div class="page">
  <SettingsPageBase
    title="Compte"
    description="Gérez les informations liées à votre compte"
  />
  <SettingsBlock>
    <SettingsItem
      title="Adresse mail"
      description="Modifiez votre adresse email de contact et de connexion. Elle ne sera pas partagée."
    >
      <span>Adresse actuelle: {email}</span>
      <Button
        onclick={() => {
          uiStore.openDialog("emailEditDialog");
        }}>Modifier</Button
      >
    </SettingsItem>
    <SettingsItem
      title="Mot de passe"
      description="Modifiez le mot de passe utilisé pour vous connecter."
    >
      <Button
        onclick={() => {
          uiStore.openDialog("passwordEditDialog");
        }}>Modifier</Button
      >
    </SettingsItem>
    <SettingsItem
      title="Déconnexion"
      description="Cliquer sur ce bouton pour vous déconnecter de votre compte."
    >
      <Button onclick={signOut}>Déconnexion</Button>
    </SettingsItem>
  </SettingsBlock>
</div>

<InputDialog
  title="Adresse e-mail"
  description="Modifiez l'adresse mail liée à votre compte."
  label="Nouvelle adresse"
  placeholder="exemple@domaine.com"
  onConfirm={() => {
    updateUserProperty({ email: emailInput });
  }}
  bind:value={emailInput}
  name="emailEditDialog"
/>

<Confirm
  title="Mot de passe"
  description="Modifiez le mot de passe de votre compte."
  onConfirm={() => {
    updateUserProperty({
      password: newPassword,
      current_password: oldPassword,
    });
  }}
  name="passwordEditDialog"
>
  <Input
    label="Mot de passe actuel"
    placeholder="Mot de passe"
    bind:value={oldPassword}
    password
  ></Input>
  <Input
    label="Nouveau mot de passe"
    placeholder="Mot de passe"
    bind:value={newPassword}
    password
  ></Input>
</Confirm>

<style>
  .page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  span {
    font-size: 0.95rem;
    color: var(--foreground);
  }
</style>
