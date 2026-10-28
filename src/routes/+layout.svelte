<script>
  import favicon from "$lib/assets/favicon.svg";
  import LoadingDialog from "$lib/components/bits-ui/LoadingDialog.svelte";
  import { onDestroy, onMount } from "svelte";

  import "../app.css";
  import { uiStore } from "$lib/components/bits-ui/uiComponentsStore.svelte";
  import ErrorReportDialog from "$lib/components/bits-ui/presets/ErrorReportDialog.svelte";
  import { invoke } from "@tauri-apps/api/core";
  import { initManifests } from "$lib/manifestsManager.svelte";

  let { children } = $props();

  // Chance icon in taskbar depending on system theme
  onMount(() => {
    const media = window.matchMedia("(prefers-color-scheme: light)");

    const updateIcon = () => {
      invoke("set_window_icon", {
        light: !media.matches,
      }).catch(console.error);
    };

    updateIcon();

    initManifests().catch(console.error);

    media.addEventListener("change", updateIcon);

    return () => {
      media.removeEventListener("change", updateIcon);
    };
  });
</script>

<svelte:window />

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

{@render children()}

<LoadingDialog />
<ErrorReportDialog />

<style>
  @import url("https://fonts.googleapis.com/css2?family=Funnel+Sans:ital,wght@0,300..800;1,300..800&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Roboto:ital,wght@0,100..900;1,100..900&family=Zain:ital,wght@0,200;0,300;0,400;0,700;0,800;0,900;1,300;1,400&family=Zalando+Sans:ital,wght@0,200..900;1,200..900&display=swap");

  :root {
    --interFont: "Inter", sans-serif;
    --zalondoFont: "Zalando Sans", sans-serif;
    --zainFont: "Zain", sans-serif;
    --funnelFont: "Funnel Sans", sans-serif;
    --robotoFont: "Roboto", sans-serif;

    font-family: var(--robotoFont);
  }
</style>
