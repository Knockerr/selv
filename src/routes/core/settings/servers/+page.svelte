<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Input from "$lib/components/bits-ui/baseComponents/Input.svelte";
  import Switch from "$lib/components/bits-ui/baseComponents/switch.svelte";
  import DeletedFoldersManager from "$lib/components/core/settings/DeletedFoldersManager.svelte";
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
    title="Serveurs"
    description="Choisissez vos préférences pour vos serveurs."
  />
  <SettingsBlock>
    <SettingsItem
      title="Serveurs supprimés"
      description="Restorez ou supprimez définitivement les serveurs que vous avez supprimé. Les serveurs supprimés sont effacés de manière irréversible au bout de 15 jours"
      noborder
    >
      <DeletedFoldersManager />
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
