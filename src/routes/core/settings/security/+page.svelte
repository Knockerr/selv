<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Input from "$lib/components/bits-ui/baseComponents/Input.svelte";
  import Switch from "$lib/components/bits-ui/baseComponents/switch.svelte";
  import SettingsBlock from "$lib/components/core/settings/SettingsBlock.svelte";
  import SettingsItem from "$lib/components/core/settings/SettingsItem.svelte";
  import SettingsPageBase from "$lib/components/core/settings/SettingsPageBase.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";

  function fullDatasReset() {
    folderSystem.resetDatas();
  }

  /*
  <h2 id="dangerZoneTitle">Danger zone</h2>

  <Button iconPath={pathDb.arrowClockwise} onclick={fullDatasReset}
    >Reinitialiser les données (action destructrice)</Button
  >
  */
</script>

<div class="page">
  <SettingsPageBase
    title="Sécurité"
    description="Gérez la sécurité de votre compte."
  />
  <SettingsBlock title="">
    <SettingsItem
      title="Adresse mail"
      description="Choisissez votre adresse email de contact et de connexion. Elle ne sera pas partagée."
    >
      <Switch />
    </SettingsItem>
  </SettingsBlock>
</div>

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
</style>
