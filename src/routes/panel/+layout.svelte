<script>
  // @ts-nocheck

  import { goto } from "$app/navigation";
  import Console from "$lib/components/panel/console.svelte";
  import DataDisplayer from "$lib/components/panel/dataDisplayer.svelte";
  import PanelTabList from "$lib/components/panel/panelTabList.svelte";
  import EulaWindow from "$lib/components/windowsSystem/WindowsBank/eulaWIndow/eulaWindow.svelte";
  import { windowsManager } from "$lib/components/windowsSystem/windowsManager.svelte";
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

<EulaWindow serverUuid={uuid} />

<style>
  @import url("https://fonts.googleapis.com/css2?family=Funnel+Sans:ital,wght@0,300..800;1,300..800&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Roboto:ital,wght@0,100..900;1,100..900&family=Zain:ital,wght@0,200;0,300;0,400;0,700;0,800;0,900;1,300;1,400&family=Zalando+Sans:ital,wght@0,200..900;1,200..900&display=swap");

  :root {

    --interFont: "Inter", sans-serif;
    --zalondoFont: "Zalando Sans", sans-serif;
    --zainFont: "Zain", sans-serif;
    --funnelFont: "Funnel Sans", sans-serif;
    --robotoFont: "Roboto", sans-serif;
  }

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
