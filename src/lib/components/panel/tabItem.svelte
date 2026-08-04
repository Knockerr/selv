<script>
  import { pathDb } from "$lib/icons/pathDb";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { fly } from "svelte/transition";
  import Icon from "../Icon.svelte";

  const { tabName, tabIconPath, onclick, unselectable } = $props();

  let isSelected = $derived(sidebarStore.currentTab("panel") == tabName);
</script>

<button
  class="component"
  onclick={async () => {
    await onclick();
    if (!unselectable) {
      sidebarStore.setCurrentTab("panel", tabName);
    }
  }}
  class:selected={isSelected}
>
  {#if isSelected}
    <div
      class="stick"
      in:fly={{ x: -5, duration: 300 }}
      out:fly={{ x: -5, duration: 300 }}
    ></div>
  {/if}
  <Icon path={tabIconPath} size={"1.35rem"} />
  <h1 id="tabName">{tabName}</h1>
</button>

<style>
  .component {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    padding: 0;
    padding-left: 20px;
    height: 45px;
    gap: 10px;
    border: 0;
    border-radius: 5px;
    background-color: transparent;
    width: 95%;
    box-sizing: border-box;
    color: #ddd;
    border-radius: 12px;
    transition: background-color 0.3s ease;
  }

  .component.selected {
    background-color: rgba(255, 255, 255, 0.08);
  }

  .component:hover {
    background-color: rgba(255, 255, 255, 0.08);
  }

  .component:active {
    transition: all 0s ease;
    background-color: rgba(255, 255, 255, 0.1);
  }

  button:hover {
    cursor: pointer;
  }

  .stick {
    height: 18px;
    width: 2.5px;
    border-radius: 999px;
    background-color: rgba(255, 255, 255, 0.8);
    position: absolute;
    left: 16px;
  }

  #tabName {
    font-size: 1.15rem;
    font-weight: 400;
  }
</style>
