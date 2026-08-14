<script>
  //@ts-nocheck
  import { checkPermissions } from "@tauri-apps/api/core";
  import TabItem from "./tabItem.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { open } from "@tauri-apps/plugin-shell";
  import { onMount } from "svelte";
  import { Command } from "@tauri-apps/plugin-shell";
  import { path } from "@tauri-apps/api";
  import { goto } from "$app/navigation";
  import { getServer } from "../recurentActions.svelte";
  import { uiStore } from "../bits-ui/uiComponentsStore.svelte";
  import Confirm from "../bits-ui/baseComponents/Confirm.svelte";

  const { uuid, name } = $props();

  let serverPath = $state("/");

  onMount(() => {
    console.log("mounting");
    fetch(`http://127.0.0.1:8000/api/servers/${uuid}/serverListDatas`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!data) return;
        serverPath = data.path ?? "";
      })
      .catch((err) => console.error("fetch error:", err));
  });

  const tabs = $state(["Console", "Fichiers", "Parametres"]);
  const unselectableTabs = ["Fichiers"];

  const tabsIcons = {
    Console: pathDb.treeStructure,
    Fichiers: pathDb.folder,
    Parametres: pathDb.wrench,
  };

  async function handleTabClick(tabName) {
    console.warn(tabName);
    switch (tabName) {
      case "Console":
        goto(`/panel/console?uuid=${uuid}`);
        break;
      case "Fichiers":
        console.warn(serverPath);
        await Command.create("explorer", [serverPath]).execute();
        break;
      case "Parametres":
        const data = await getServer(uuid, "propertiesInfos");
        const propertiesExist = data.exist;
        if (!propertiesExist) {
          uiStore.openDialog("propertiesWarning");
          return;
        }
        goto(`/panel/parametres?uuid=${uuid}`);
        break;
    }
  }
</script>

<div class="component">
  <h1 id="title"><a href="/core/dashboard">Panel</a></h1>
  <h2 class="topDatas" id="serverUuid">
    {uuid}
  </h2>
  <div class="tabsContainer">
    {#each tabs as tab}
      <TabItem
        tabName={tab}
        tabIconPath={tabsIcons[tab]}
        onclick={() => handleTabClick(tab)}
        unselectable={unselectableTabs.includes(tab)}
      />
    {/each}
  </div>
</div>

<Confirm
  title="Propriétés du serveur"
  description="Le fichier permettant de définir les propriétés du serveur n'existe pas tant que le serveur n'a pas été lancé au moins une fois après avoir accepté l'EULA."
  confirmLabel="Compris"
  name="propertiesWarning"
/>

<style>
  * {
    font-family: Arial, Helvetica, sans-serif;
    color: #ededed;
  }

  .component {
    height: 100%;
    width: 300px;
    background-color: #111825;
    border-right: 1.5px solid #1b2639;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    align-items: center;
    border-radius: 0;
    position: relative;
  }

  #title {
    padding: 0;
    margin-bottom: 10px;
    font-size: 3rem;
  }

  #title a {
    text-decoration: none;
    font-style: none;
  }

  #serverUuid {
    font-size: 0.7rem;
    margin: 0;
    margin-left: 5px;
    margin-bottom: 45px;
    align-self: flex-start;
    font-weight: 200;
  }

  .tabsContainer {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    height: max-content;
  }
</style>
