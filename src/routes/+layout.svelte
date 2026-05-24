<script>
  import favicon from "$lib/assets/favicon.svg";
  import { contextManager } from "$lib/components/contextMenuSystem/contextMenuManager.svelte";

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
