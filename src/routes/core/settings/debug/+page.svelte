<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Confirm from "$lib/components/bits-ui/baseComponents/Confirm.svelte";
  import Input from "$lib/components/bits-ui/baseComponents/Input.svelte";
  import Switch from "$lib/components/bits-ui/baseComponents/switch.svelte";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import SettingsBlock from "$lib/components/core/settings/SettingsBlock.svelte";
  import SettingsItem from "$lib/components/core/settings/SettingsItem.svelte";
  import SettingsPageBase from "$lib/components/core/settings/SettingsPageBase.svelte";
  import { post } from "$lib/components/recurentActions.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { downloadReport } from "$lib/logger.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import { stats } from "$lib/stores/stats.svelte";

  let debugAction = $state(() => {});

  function fullDatasReset() {
    console.info("Resetting datas on user command");
    folderSystem.resetDatas();
    stats.resetDatas();
  }

  function shutdownBackend(){
    console.info("Shutting down backend on user command");
    post("http://127.0.0.1:40401/shutdown")

  }
</script>

<div class="page">
  <SettingsPageBase
    title="Débug"
    description="Cette section est dédié à la résolution de problèmes liés au logiciel. Il est recommandé de ne pas executer les actions ci-dessous sauf sur demande du support."
  />
  <SettingsBlock>
    <SettingsItem
      title="Télécharger le rapport d'activité"
      description="Cette action téléchargera sur votre pc un rapport complet des journaux du logiciel, permettant de repérer et comprendre certains problèmes de fonctionnement. Attention: Certaines informations personnelles peuvent être présentes dans les données générées. Se référer à l'Article 3.7 de la politique de confidentialité."
      noborder
    >
      <Button
        iconPath={pathDb.download}
        onclick={() => {
          downloadReport();
        }}>Télécharger</Button
      >
    </SettingsItem>
    <SettingsItem
      title="Couper le backend interne"
      description="Cette action coupera le backend interne du logiciel et tous vos serveurs. Un redémarrage du logiciel sera nécessaire."
      noborder
    >
      <Button
        iconPath={pathDb.stop}
        onclick={() => {
          debugAction = shutdownBackend;
          uiStore.openDialog("debugConfirm");
        }}>Éteindre</Button
      >
    </SettingsItem>
    <SettingsItem
      title="Réinitialisation des données"
      description="Cette action effacera tous les serveurs de l'interface et supprimera vos dossiers. Vos serveurs ne seront pas supprimés mais il faudra les réimporter si vous souhaitez les utiliser."
      noborder
    >
      <Button
        iconPath={pathDb.arrowClockwise}
        onclick={() => {
          debugAction = fullDatasReset;
          uiStore.openDialog("debugConfirm");
        }}>Réinitialiser</Button
      >
    </SettingsItem>
  </SettingsBlock>
</div>

<Confirm
  onConfirm={() => {
    debugAction();
    debugAction = () => {};
  }}
  name="debugConfirm"
  title="Action de débug"
  description="Êtes vous sûr de vouloir réaliser cette action? Celle-ci peut avoir des conséquences destructrices sur vos serveurs ou alterer le fonctionnement du logiciel. Assurez vous d'avoir lu la description de l'action pour savoir quels en sont les impacts. Il est conseillé de n'executer cette action que si vous savez ce que vous faites ou avez été conseillé par le support officiel de Selv."
/>

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
