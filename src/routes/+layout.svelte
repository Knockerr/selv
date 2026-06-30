<script>
  import favicon from "$lib/assets/favicon.svg";
  import { contextManager } from "$lib/components/contextMenuSystem/contextMenuManager.svelte";

  import "../app.css";

  let { children } = $props();

  const isAContextOpen = $derived(contextManager.isAMenuOpen);
</script>

<svelte:window
  onclick={() => {
    if (isAContextOpen) contextManager.close();
  }}
/>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

{@render children()}

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
