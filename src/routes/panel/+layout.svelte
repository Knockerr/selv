<script>
  // @ts-nocheck

  import { goto } from "$app/navigation";
  import Console from "$lib/components/panel/console.svelte";
  import DataDisplayer from "$lib/components/panel/dataDisplayer.svelte";
  import PanelTabList from "$lib/components/panel/panelTabList.svelte";
  import { folderSystem } from "$lib/stores/folderSystem.svelte";

  const { children } = $props();

  const params = new URLSearchParams(window.location.search);
  let uuid = params.get("uuid") ?? "demoUuid";
</script>

<div class="container">
  <PanelTabList {uuid} />
  <div class="children">
    {@render children()}
  </div>
</div>

<style>
  .container {
    background-color: #030712;
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .children{
    width: 100%;
    height: 100%;
  }
</style>
