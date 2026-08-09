<script>
  // @ts-nocheck
  import { goto } from "$app/navigation";
  import { pathDb } from "$lib/icons/pathDb";
  import { onMount } from "svelte";
  import Icon from "./Icon.svelte";
  import FolderContextMenu from "./contextMenuSystem/ContextMenusBank/FolderContextMenu/FolderContextMenu.svelte";
  import { windowsManager } from "./windowsSystem/windowsManager.svelte";
  import { contextManager } from "./contextMenuSystem/contextMenuManager.svelte";

  const { uuid = "" } = $props();

  let name = $state("");
  let serverType = $state("");
  let serverVersion = $state("");
  let lastUse = $state("");
  let state = $state("");

  onMount(() => {
    console.log("mounting");
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

  let folderButtonPosX = $state();
  let folderButtonPosY = $state();

  function onFolderButtonClick() {
    const datas = event.target.getBoundingClientRect();
    folderButtonPosX = datas.left;
    folderButtonPosY = datas.top;
    contextManager.open("folderContextMenu-" + uuid);
    event.stopPropagation();
  }
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
      <button id="start">
        <Icon path={pathDb.playCircle} size="15" color="#38ab4a" />
      </button>
      <button id="restart">
        <Icon
          path={pathDb.restartCircle}
          size="15"
          vb="0 -960 960 960"
          color="orange"
        />
      </button>
      <button id="stop">
        <Icon path={pathDb.stopCircle} size="15" color="#a82a2a" />
      </button>
    </div></td
  >
  <td id="serverType">{serverType}</td>
  <td id="serverVersion">{serverVersion}</td>
  <td>
    <button
      class="folderButton buttonPreset1"
      id="folderButton"
      onclick={onFolderButtonClick}
    >
      <Icon path={pathDb.bookmarks} size="13" />
    </button>
  </td>
  <td id="lastUse">{lastUse}</td>
  <td>
    <button id="moreOptionsButton" class="buttonPreset1">
      <Icon path={pathDb.threeDotsVertical} size="13" />
    </button>
  </td>
  <td id="serverUUID" style="display: none">{uuid}</td>
</tr>

<FolderContextMenu
  serverUuid={uuid}
  posx={folderButtonPosX}
  posy={folderButtonPosY}
/>

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

  .buttonPreset1:hover {
    transition: background-color 0.3s ease;
    background-color: rgb(50, 59, 80);
  }

  .buttonPreset1:active {
    transition: background-color 0s ease;
    background-color: rgb(32, 38, 54);
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

  #moreOptionsButton {
    background-color: var(--mainBackgroundColor);
    border: none;
    height: 25px;
    width: 25px;
    padding: 5px;
    border-radius: 50%;
    color: white;
    transform: scale(1.6);
    position: relative;
    margin-right: 80px;
  }

  #moreOptionsButton {
    text-align: center;
  }

  #moreOptionsButton:hover {
    transition: background-color 0.3s ease;
    background-color: rgb(50, 59, 80);
  }

  #moreOptionsButton:active {
    transition: background-color 0s ease;
    background-color: rgb(32, 38, 54);
  }

  @media (max-width: 1225px) {
    #lastUse {
      display: none;
    }

    #lastUse {
      display: none;
    }
  }

  @media (max-width: 1040px) {
    #serverType {
      display: none;
    }

    #serverType {
      display: none;
    }
  }

  @media (max-width: 985px) {
    #serverVersion {
      display: none;
    }

    #serverVersion {
      display: none;
    }
  }
</style>
