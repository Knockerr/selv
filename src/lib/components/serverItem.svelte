<script>
  import { goto } from "$app/navigation";
  import { pathDb } from "$lib/icons/pathDb";
  import { onDestroy, onMount, untrack } from "svelte";
  import Icon from "./Icon.svelte";
  import IconButton from "./bits-ui/baseComponents/iconButton.svelte";
  import Dropdown from "./bits-ui/baseComponents/Dropdown.svelte";
  import {
    postServer,
    restartServer,
    startServer,
    stopServer,
  } from "./recurentActions.svelte";
  import { uiStore } from "./bits-ui/uiComponentsStore.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";
  import FolderSystem from "./serverList/folderSystem.svelte";

  const { uuid = "" } = $props();

  let name = $state("");
  let serverType = $state("");
  let serverVersion = $state("");
  let lastUse = $state("");
  let state = $state("");

  $inspect(state);

  let suggestedActionInfos = $state({});

  let stateWs;
  function trackServerState() {
    stateWs = new WebSocket(`ws://127.0.0.1:8000/ws/servers/${uuid}/state`);

    stateWs.onopen = () => {
      console.info("Succesfully connected to state ws for ", uuid);
    };

    stateWs.onmessage = (event) => {
      state = event.data;
      switch (state) {
        case "stopped":
          suggestedActionInfos = {
            label: "Démarrer",
            icon: pathDb.start,
            execute: () => {
              startServer(uuid);
            },
          };
          break;
        case "running":
          suggestedActionInfos = {
            label: "Arrêter",
            icon: pathDb.stop,
            execute: () => {
              stopServer(uuid);
            },
          };
          break;
        default:
          console.warn("Couldn't match " + state + " state");
      }
    };

    stateWs.onerror = (err) => {
      console.error("Error in state ws for " + uuid + " : " + "err");
    };

    stateWs.onclose = () => {
      console.debug("Closed state ws for " + uuid);
    };
  }

  onDestroy(() => {
    if (stateWs && stateWs.OPEN) stateWs.close();
  });

  onMount(() => {
    console.log("mounting");
    trackServerState();
    fetch(`http://127.0.0.1:8000/api/servers/${uuid}/serverListDatas`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!data) return;
        name = data.name ?? "";
        serverType = data.type ?? "";
        lastUse = data.lastUse ?? "";
        serverVersion = data.version ?? "";
      })
      .catch((err) => console.error("fetch error:", err));
  });

  $effect(() => {
    console.log("Uuid changed!");
    fetch(`http://127.0.0.1:8000/api/servers/${uuid}/serverListDatas`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!data) return;
        name = data.name ?? "";
        serverType = data.type ?? "";
        const lastUseUtc = new Date(data.lastUse) || "";
        lastUse = lastUseUtc.toLocaleString();
        serverVersion = data.version ?? "";
      })
      .catch((err) => console.error("fetch error:", err));
  });

  const moreDropdownItems = $derived([
    {
      icon: suggestedActionInfos.icon,
      label: suggestedActionInfos.label,
      onclick: suggestedActionInfos.execute,
    },
    {
      icon: pathDb.console,
      label: "Console",
      onclick: () => {
        goto("/panel/console?uuid=" + uuid);
      },
    },
    {
      type: "separator",
    },
    {
      icon: pathDb.pencil,
      label: "Renommer",
      onclick: () => {
        uiStore.setCurrentUuid(uuid);
        uiStore.openDialog("serverRenameDialog");
      },
    },
    {
      icon: pathDb.copy,
      label: "Dupliquer",
      onclick: () => {
        uiStore.setCurrentUuid(uuid);
        uiStore.openDialog("serverDuplicateDialog");
      },
    },
    {
      type: "separator",
    },
    {
      icon: pathDb.garbage,
      label: "Supprimer",
      dangerous: true,
      onclick: () => {
        uiStore.setCurrentUuid(uuid);
        uiStore.openDialog("serverDeletionConfirm");
      },
    },
  ]);

  let foldersDropdownItems = $state([]);

  $effect(() => {
    // Trick to use a deeply reactive state for foldersDropdownItems (to allow binding to item.value)
    folderSystem.folderDatas;
    untrack(() => {
      Object.entries(folderSystem.folderDatas).forEach(
        ([folderName, folderDatas]) =>
          foldersDropdownItems.push({
            label: folderName,
            type: "checkItem",
            value: folderSystem.getFolder(folderName).getServers.includes(uuid),
            onclick: (checked) => {
              if (checked) folderSystem.getFolder(folderName).addServer(uuid);
              else folderSystem.getFolder(folderName).removeServer(uuid);
            },
          }),
      );
    });
  });
</script>

<tr>
  <td
    ><button
      onclick={() => {
        goto(`/panel/console?uuid=${uuid}`);
      }}
      id="serverName">{name}</button
    ></td
  >
  <td
    ><div id="quickButtons">
      <button id="start" disabled={state === "running"} onclick={() => {startServer(uuid)}}>
        <Icon path={pathDb.playCircle} size="15" color="#38ab4a" />
      </button>
      <button
        id="restart"
        disabled={state === "stopped"}
        onclick={() => {restartServer(uuid)}}
      >
        <Icon
          path={pathDb.restartCircle}
          size="15"
          vb="0 -960 960 960"
          color="orange"
        />
      </button>
      <button id="stop" disabled={state === "stopped"} onclick={() => {stopServer(uuid)}}>
        <Icon path={pathDb.stopCircle} size="15" color="#a82a2a" />
      </button>
    </div></td
  >
  <td id="serverType">{serverType}</td>
  <td id="serverVersion">{serverVersion}</td>
  <td id="folders">
    <Dropdown items={foldersDropdownItems}>
      {#snippet triggerSnippet()}
        <IconButton iconSize="20" iconPath={pathDb.bookmarks} />
      {/snippet}
    </Dropdown>
  </td>
  <td id="lastUse">{lastUse}</td>
  <td>
    <Dropdown items={moreDropdownItems}>
      {#snippet triggerSnippet()}
        <IconButton iconSize="20" iconPath={pathDb.threeDotsVertical} />
      {/snippet}
    </Dropdown>
  </td>
</tr>

<style>
  * {
    color: white;
  }

  td {
    font-family: "Roboto", sans-serif;
    font-weight: 500;
    font-size: 15px;
    text-align: left;
    padding-left: 15px;
    border-top: #1f2937 solid 1.5px;
    vertical-align: middle;
    height: 70px;
  }

  button {
    background-color: var(--mainBackgroundColor);
    border: none;
    height: 25px;
    width: 25px;
    padding: 5px;
    margin-left: 3px;
    border-radius: 50%;
    color: white;
    transform: scale(1.6);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }

  #quickButtons {
    display: flex;
    flex-direction: row;
    gap: 12px;
  }

  #quickButtons button {
    padding: 0;
    height: fit-content;
    width: fit-content;
    overflow: hidden !important;
  }

  #quickButtons button::after {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    background-color: #0009;
    content: "";
    display: none;
  }

  #quickButtons button:disabled {
    cursor: default;
  }

  #quickButtons button:disabled::after {
    display: inline;
  }

  #quickButtons:hover {
    cursor: pointer;
  }

  #serverName {
    all: unset;
    cursor: pointer;
    color: white;
    font-family: "Roboto", sans-serif;
    font-size: 18px;
    font-weight: 375;
    text-align: left;
  }

  @media (max-width: 1300px) {
    #folders {
      display: none;
    }
  }

  @media (max-width: 1225px) {
    #lastUse {
      display: none;
    }
  }

  @media (max-width: 1040px) {
    #serverType {
      display: none;
    }
    #serverVersion {
      display: none;
    }
  }
</style>
