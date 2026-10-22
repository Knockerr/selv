<script>
  import { goto } from "$app/navigation";
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Container from "$lib/components/bits-ui/baseComponents/Container.svelte";
  import IconButton from "$lib/components/bits-ui/baseComponents/iconButton.svelte";
  import ProgressBar from "$lib/components/bits-ui/baseComponents/ProgressBar.svelte";
  import Icon from "$lib/components/Icon.svelte";
  import { post } from "$lib/components/recurentActions.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { event } from "@tauri-apps/api";
  import { getVersion } from "@tauri-apps/api/app";
  import { check } from "@tauri-apps/plugin-updater";
  import { marked } from "marked";
  import { onMount } from "svelte";

  let currentVersion = $state("v0.1.0");
  let newVersion = $state("");
  let updateTag = $state("patch");
  let downloaded = $state(0);
  let downloadSize = $state(0);
  let downloadState = $state();
  let releaseDate = $state("08/08/26");
  let updateMdInfos = $state("");

  let update;
  async function checkUpdate() {
    update = await check();
    if (!update) {
      newVersion = null;
      return;
    }
    console.log(`Found update ${update.version} from ${update.date}`);
    currentVersion = await getVersion();
    newVersion = update.version;
    releaseDate = update.date;
    await updateMd();
    // Update tag
    const match = updateMdInfos.match(/^\[([^\]]+)\]/);
    if (match) {
      console.log("Tag trouvé :", match[1]);
      updateTag = match[1];
    }
  }

  async function updateMd() {
    const res = await fetch(
      "https://github.com/Knockerr/selv/releases/latest/download/latest.json",
      {
        method: "GET",
      },
    );

    const data = await res.json();
    if (data.notes) updateMdInfos = data.notes;
  }

  async function closeBackend() {
    let res = await post("shutdown");
    if (!res.ok) {
      console.error("Impossible to stop internal backend : ", res);
    }
  }

  async function installUpdate() {
    await checkUpdate();
    if (!update) return;
    let downloaded = $state(0);
    let contentLength = $state(0);

    // Closing all servers and internal backend
    downloadState = "Fermeture des serveurs";
    await closeBackend();

    await update.downloadAndInstall((event) => {
      switch (event.event) {
        case "Started":
          contentLength = event.data.contentLength;
          downloadState = "Démarrage du téléchargement";
          console.log(`started downloading ${event.data.contentLength} bytes`);
          break;
        case "Progress":
          downloaded += event.data.chunkLength;
          downloadState = "Téléchargement en cours...";
          console.log(`downloaded ${downloaded} from ${contentLength}`);
          break;
        case "Finished":
          downloadState = "Téléchargement terminé, installation..";
          console.log("download finished");
          break;
      }
    });

    downloadState = "Installation terminée! Redémarrage..";
    // Give user time to see message
    await new Promise((r) => setTimeout(r, 1500));
    await relaunch();
  }

  // TODO BEFOREPROD: Test update system with repo in public

  onMount(() => {
    checkUpdate();
    updateMd();
  });
</script>

<div class="page">
  <div class="container" width="80%">
    <div class="titleContainer">
      <div class="titles">
        <h1 class="title">
          Mise à jour
          {#if newVersion}
            <div class="tag">
              {updateTag}
            </div>
          {/if}
        </h1>
        <h2 class="versions">
          {currentVersion}
          {#if newVersion}
            ->
            {newVersion}
          {/if}
        </h2>
      </div>
      {#if !newVersion}
        <Button
          iconPath={pathDb.arrowClockwise}
          className="mr-5 mt-2"
          onclick={checkUpdate}>Chercher des mises à jour</Button
        >
      {:else}
        <Button
          emphasize
          iconPath={pathDb.download}
          className="mr-5 mt-2"
          onclick={installUpdate}
          disabled={downloadState}>Installer</Button
        >
      {/if}
    </div>

    <div class="middleSection">
      <div class="left">
        {#if newVersion && !downloadState}
          <div class="infosContainer">
            <span class="informativeText">
              Une nouvelle version est disponible! Mettez à jour le logiciel
              pour accéder aux dernières fonctionnalitées et patchs de sécurité.
            </span>
            <span class="informativeText"
              >Vos serveurs actifs seront éteint pendant la mise à jour. Vous
              devrez les relancer manuellement après cette dernière.</span
            >
          </div>
          <div class="updateInfos">
            <span class="updateInfo">Date: {releaseDate}</span>
          </div>
        {:else if downloadState}
          <div class="dowloadStateContainer">
            <span>{downloadState}</span>
            <div class="downloadProgressContainer">
              <ProgressBar
                width="250px"
                progress={downloaded}
                max={downloadSize}
              />
              <span class="downloadProgressText"
                >{downloaded} / {downloadSize}</span
              >
            </div>
          </div>
        {:else if !newVersion}
          <span class="informativeText">Vous êtes à jour!</span>
        {/if}
      </div>
      <div class="right">
        <Button iconPath={pathDb.arrowRight} disabled={downloadState} emphasize={!newVersion} onclick={goto("/core/dashboard")}>
          {#if newVersion}
            Continuer sans mettre à jour
          {:else}
            Continuer
          {/if}</Button
        >
      </div>
    </div>

    {#if newVersion}
      <h4 class="updateMdTitle">Nouveautées:</h4>
    {:else}
      <h4 class="updateMdTitle">Dernière mise à jour:</h4>
    {/if}
    <div class="updatesInfosContainer">{@html marked(updateMdInfos)}</div>
  </div>
</div>

<style>
  .page {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .container {
    width: 60%;
    height: 60%;
    background-color: var(--background-alt);
    border: 1px solid var(--color-muted-foreground);
    border-radius: 12px;
    overflow: hidden;
    box-sizing: border-box;
    padding: 25px;
    display: flex;
    flex-direction: column;
  }

  .titleContainer {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  h1,
  h2,
  h4 {
    margin: 0;
  }

  .titles {
    display: flex;
    flex-direction: column;
    gap: 0px;
  }

  .title {
    font-size: 2.5rem;
    display: flex;
    flex-direction: row;
    gap: 20px;
    align-items: center;
  }

  .versions {
    font-size: 1.1rem;
    font-weight: 500;
    margin-left: 10px;
    margin-bottom: -15px;
  }

  .tag {
    background-color: #2355c2;
    color: white;
    width: fit-content;
    height: fit-content;
    padding: 3px 11px;
    font-size: 0.8rem;
    font-weight: 600;
    border-radius: 999px;
    text-transform: uppercase;
  }

  .middleSection {
    height: 35%;
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }

  .left {
    height: 25%;
    box-sizing: border-box;
    padding: 45px 0;
    display: flex;
    flex-direction: column;
    gap: 25px;
  }

  .right {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    box-sizing: border-box;
    margin-right: 30px;
  }

  .infosContainer {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 120%;
  }

  .informativeText {
    color: var(--foreground);
    font-size: 1.05rem;
  }

  .updateInfos {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .dowloadStateContainer {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .downloadProgressContainer {
    display: flex;
    flex-direction: row;
    gap: 10px;
    align-items: center;
  }

  .downloadProgressText {
    color: var(--color-foreground-alt);
  }

  .updateMdTitle {
    margin-top: 15px;
    margin-bottom: 3px;
    font-size: 1.3rem;
  }

  .updatesInfosContainer {
    background-color: var(--color-background);
    border: 2px solid var(--color-border-card);
    box-sizing: border-box;
    padding: 5px;
    border-radius: 10px;
    flex: 1;
    overflow-y: scroll;
  }

  :global(a) {
    color: var(--success);
  }
</style>
