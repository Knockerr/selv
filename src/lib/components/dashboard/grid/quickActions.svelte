<script>
  import { goto } from "$app/navigation";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import { pathDb } from "$lib/icons/pathDb";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { stats } from "$lib/stores/stats.svelte";
  import { Command, open } from "@tauri-apps/plugin-shell";
  import QuickActionsElement from "../dashboardUtilities/QuickActionsElement.svelte";
  import GridElem from "./gridElem.svelte";
  import { openUrl } from "@tauri-apps/plugin-opener";

  const actions = $derived([
    {
      label: "Créer un serveur",
      icon: pathDb.plus,
      color: "#33d",
      onclick: async () => {
        goto("/core/serverList");
        sidebarStore.setCurrentTab("main", "Servers");
        // Waiting for dialog to load in DOM
        await new Promise((r) => setTimeout(r, 150));
        uiStore.openDialog("createServerDialog");
      },
    },
    {
      label: "Tout arrêter",
      icon: pathDb.stopCircle,
      color: "#d22",
      onclick: () => {
        fetch("http://localhost:40401/api/servers/stopAll", {
          method: "POST",
        });
      },
    },

    {
      label: "Dernier serveur",
      icon: pathDb.arrowLeft,
      color: "",
      disabled: !stats.lastVisitedServer,
      onclick: () => {
        goto(`/panel/console?uuid=${stats.lastVisitedServer}`);
      },
    },
    {
      label: "Importer un serveur",
      icon: pathDb.download,
      color: "#33d",
      onclick: async () => {
        goto("/core/serverList");
        sidebarStore.setCurrentTab("main", "Servers");
        // Waiting for dialog to load in DOM
        await new Promise((r) => setTimeout(r, 150));
        uiStore.openDialog("importServerDialog");
      },
    },
    {
      label: "Mises à jour",
      icon: pathDb.update,
      color: "#b50",
      onclick: () => {
        goto("/update");
      },
    },
    {
      label: "Fichiers",
      icon: pathDb.folder,
      color: "",
      onclick: async () => {
        // Fetching %localappdata%/servers
        const res = await fetch(
          "http://localhost:40401/api/servers/localPath",
          {
            method: "GET",
          },
        );
        const datas = await res.json();

        Command.create("explorer", datas["serversPath"]).execute();
      },
    },
    {
      label: "Paramètres",
      icon: pathDb.gears,
      color: "",
      onclick: () => {
        goto("/core/settings/account");
        sidebarStore.setCurrentTab("main", "Paramètres");
      },
    },
    {
      label: "Discord",
      icon: pathDb.question,
      color: "#5865F2",
      onclick: () => {
        openUrl("https://discord.gg/FVh9daFrH7");
      }, // TODO : Goto discord link
    },
  ]);
</script>

<GridElem title="Actions rapides">
  <div class="card">
    {#each actions as { label, icon, color, onclick, disabled }}
      <QuickActionsElement
        {label}
        iconPath={icon}
        {color}
        {onclick}
        {disabled}
      />
    {/each}
  </div>
</GridElem>

<style>
  .card {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 11px;
  }
</style>
