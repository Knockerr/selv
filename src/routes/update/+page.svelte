<script>
  import Button from "$lib/components/bits-ui/baseComponents/Button.svelte";
  import Container from "$lib/components/bits-ui/baseComponents/Container.svelte";
  import IconButton from "$lib/components/bits-ui/baseComponents/iconButton.svelte";
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { marked } from "marked";
  import { onMount } from "svelte";

  let currentVersion = $state("v0.1.0");
  let newVersion = $state("v0.1.2");
  let updateTag = $state("patch");
  let downloadSize = $state("5Mo");
  let releaseDate = $state("08/08/26");
  let updateMdInfos = $state("`Salut! Je suis du code`");

  onMount(async () => {
    const res = await fetch(
      "https://raw.githubusercontent.com/sveltejs/kit/master/README.md",
    );
    updateMdInfos = await res.text();
  });
</script>

<div class="page">
  <div class="container" width="80%">
    <div class="titleContainer">
      <div class="titles">
        <h1 class="title">Mise à jour</h1>
        <h2 class="versions">
          {currentVersion}
          {#if newVersion}
            ->
            {newVersion}
          {/if}
        </h2>
        {#if newVersion}
          <div class="tag">
            {updateTag}
          </div>
        {/if}
      </div>
      {#if !newVersion}
        <Button emphasize iconPath={pathDb.arrowClockwise} className="mr-5 mt-2"
          >Chercher des mises à jour</Button
        >
      {:else}
        <Button emphasize iconPath={pathDb.download} className="mr-5 mt-2"
          >Installer</Button
        >
      {/if}
    </div>

    <div class="middleSection">
      {#if newVersion}
        <div class="infosContainer">
          <span class="informativeText">
            Une nouvelle version est disponible! Mettez à jour le logiciel pour
            accéder aux dernières fonctionnalitées et patchs de sécurité.
          </span>
          <span class="informativeText"
            >Vos serveurs actifs seront éteint pendant la mise à jour. Vous
            devrez les relancer manuellement après cette dernière.</span
          >
        </div>
        <div class="updateInfos">
          <span class="updateInfo"
            >Taille du téléchargement: {downloadSize}</span
          >
          <span class="updateInfo">Date: {releaseDate}</span>
        </div>
      {:else}
        <span class="informativeText">Vous êtes à jour!</span>
      {/if}
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
  }

  .versions {
    font-size: 1.1rem;
    font-weight: 500;
    margin-left: 10px;
    margin-bottom: 15px;
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
    height: 25%;
    box-sizing: border-box;
    padding: 30px 0;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .infosContainer {
    display: flex;
    flex-direction: column;
    gap: 5px;
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
