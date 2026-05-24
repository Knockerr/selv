<script>
  // @ts-nocheck
  import { pathDb } from "$lib/icons/pathDb";
  import { fade, fly } from "svelte/transition";
  import Icon from "../Icon.svelte";
  import { windowsManager } from "./windowsManager.svelte";

  // Récuperation des enfants
  const {
    children = null,
    title = "Page indéfinie",
    height,
    width,
    windowId,
  } = $props();

  export function openWindow() {
    windowsManager.open(windowId);
  }

  function closeWindow() {
    windowsManager.close(windowId);
  }

  const isOpen = $derived(windowsManager.openWindows.has(windowId));
</script>

<div
  class="backgroundDarkener"
  transition:fade={{ duration: 200 }}
  role="button"
  tabindex="0"
  onclick={(e) => {
    e.preventDefault();
    closeWindow();
  }}
  onkeypress={(e) => {
    e.preventDefault();
    closeWindow();
  }}
></div>
<div
  class="window"
  style:width
  style:height
  transition:fly|local={{ y: 50, duration: 200 }}
  role="button"
  tabindex="0"
  onclick={(e) => {
    e.stopPropagation();
  }}
  onkeypress={(e) => {
    e.stopPropagation();
  }}
>
  <div class="topBar">
    <div class="none"></div>
    <h2>{title}</h2>
    <button class="closeFormButton" onclick={closeWindow}>
      <Icon path={pathDb.cross} size="25" />
    </button>
  </div>
  {@render children?.()}
</div>

<style>
  .backgroundDarkener {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999999;
  }

  .window {
    position: absolute;
    top: 50%;
    right: 50%;
    transform: translate(50%, -50%);
    background-color: #030712;
    border: 1.25px solid rgb(11, 17, 29);
    box-shadow: 0 0 10px #53505018;
    border-radius: 30px;
    z-index: 99999999;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    padding: 0 20px;
    overflow-x: hidden;
    overflow-y: scroll;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }

  .topBar {
    display: flex;
    flex-direction: row;
    padding: 0;
    padding-bottom: 10px;
    margin-top: 10px;
    justify-content: space-between;
    align-items: center;
  }

  h2 {
    color: #ddd;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 2.75rem;
    padding: 0;
    margin: 0;
    margin-top: 5px;
  }

  .closeFormButton {
    background-color: transparent;
    width: fit-content;
    height: fit-content;
    padding: 4px;
    border: none;
    border-radius: 50%;
    outline: none;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .closeFormButton:hover {
    background-color: #dddddd3d;
  }

  .closeFormButton:active {
    background-color: #dddddd10;
  }
</style>
