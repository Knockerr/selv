<script>
  import { Tabs } from "bits-ui";
  import { onMount } from "svelte";

  const { tabNames, tabsContentSnippet, tabListClass = "" } = $props();
  // tabsContentSnipper contains <Tabs.Content />
</script>

<Tabs.Root value={tabNames[0]}>
  <Tabs.List
    class={`flex flex-row gap-5 ${tabListClass}`}
  >
    {#each tabNames as tab}
      <Tabs.Trigger
        class="p-2 w-21 h-7 flex items-center justify-center rounded-full text-sm font-semibold bg-white/60 hover:bg-white/70 data-[state=active]:bg-white/90 text-black/95 border-[5px]"
        style="border: 1.8px solid #bbb; box-shadow: 0 0 5px rgba(255, 255, 255, 0.2);"
        value={tab}>{tab}</Tabs.Trigger
      >
    {/each}
  </Tabs.List>
  {@render tabsContentSnippet?.()}
</Tabs.Root>
