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
    console.info("Resetting datas on user command");
    folderSystem.resetDatas();
  }
</script>

<div class="page">
  <SettingsPageBase
    title="Débug"
    description="Cette section est dédié à la résolution de problèmes liés au logiciel. Il est recommandé de ne pas executer les actions ci-dessous sauf sur demande du support."
  />
  <SettingsBlock>
    <SettingsItem
      title="Réinitialisation des données"
      description="Cette action effacera tous les serveurs de l'interface et supprimera vos dossiers. Vos serveurs ne seront pas supprimés mais il faudra les réimporter si vous souhaitez les utiliser."
    >
      <Button
        iconPath={pathDb.arrowClockwise}
        onclick={fullDatasReset}>Réinitialiser</Button
      >
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
