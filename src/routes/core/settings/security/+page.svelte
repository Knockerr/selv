<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import IconButton from "$lib/components/bits-ui/baseComponents/iconButton.svelte";
  import Input from "$lib/components/bits-ui/baseComponents/Input.svelte";
  import Switch from "$lib/components/bits-ui/baseComponents/switch.svelte";
  import TOTPEnrollmentDialog from "$lib/components/bits-ui/presets/TOTPEnrollmentDialog.svelte";
  import Tile from "$lib/components/bits-ui/Tile.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import SettingsBlock from "$lib/components/core/settings/SettingsBlock.svelte";
  import SettingsItem from "$lib/components/core/settings/SettingsItem.svelte";
  import SettingsPageBase from "$lib/components/core/settings/SettingsPageBase.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { supabase } from "$lib/supabaseClient.svelte";
  import { onMount } from "svelte";

  let connectedFactors = $state([]);

  async function updateConnectedFactors() {
    const factors = await supabase.auth.mfa.listFactors();
    console.warn(factors);
    factors.data.totp.forEach((factors) => {
      connectedFactors.push({
        name: factors.friendly_name,
        id: factors.id,
      });
    });
  }

  onMount(() => {
    updateConnectedFactors();
  });

  function fullDatasReset() {
    folderSystem.resetDatas();
  }

  function enrollTOTP() {
    uiStore.openDialog("TOTPEnrollmentDialog");
  }
</script>

<div class="page">
  <SettingsPageBase
    title="Sécurité"
    description="Gérez la sécurité de votre compte."
  />
  <SettingsBlock title="">
    <SettingsItem
      title="Authentification à deux facteurs"
      description="Connnectez une ou plusieurs applications d'authentification pour garantir la sécurité de votre compte."
    >
      <Button onclick={enrollTOTP}>Ajouter</Button>
    </SettingsItem>
    <SettingsItem
      title="Application d'A2F"
      description="Gérez en temps réel quelles applications d'authentification sont liées à votre compte"
    >
      {#if connectedFactors == true}
        {#each connectedFactors as { name, id }}
          <Tile
            label={name}
            className="capitalize"
            width="300px"
            height="35px"
            fontSize="0.9rem"
          >
            <IconButton
              iconPath={pathDb.garbage}
              color="var(--dangerous)"
              onclick={async () => {
                const { data, error } = await supabase.auth.mfa.unenroll({
                  factorId: id,
                });
                if (error) {
                  console.error(
                    `Error whilst unenrolling factorId ${factorId} : ${error}`,
                  );
                }
                await updateConnectedFactors();
              }}
            />
          </Tile>
        {/each}
      {:else}
        <span>Aucune application d'authentification connectée.</span>
      {/if}
    </SettingsItem>
  </SettingsBlock>
</div>

<TOTPEnrollmentDialog />

<style>
  .page {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .container {
    width: fit-content;
    height: fit-content;
    background: transparent;
  }

  span {
    font-size: 0.9rem;
    color: var(--foreground-alt);
  }
</style>
