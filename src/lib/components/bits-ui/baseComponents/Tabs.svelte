<script>
  import { Tabs } from "bits-ui";
  import { onMount } from "svelte";
  import Tile from "../Tile.svelte";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";

  const { tabNames, tabsContentSnippet, tabListClass = "" } = $props();
  // tabsContentSnipper contains <Tabs.Content />

  $inspect(sidebarStore.currentTab("serverSettings"));
</script>

<Tabs.Root value={tabNames[0]} class="flex flex-row gap-5 justify-start w-full">
  <Tabs.List class="flex flex-col gap-px w-50">
    {#each tabNames as tab}
      <Tabs.Trigger
        class="bg-transparent h-fit w-full border-0 outline-0"
        value={tab}
      >
        <Tile
          label={tab}
          height="35px"
          width="100%"
          labelStyle="font-weight: 600;"
          onclick={() => {
            sidebarStore.setCurrentTab("serverSettings", tab);
          }}
          selected={sidebarStore.currentTab("serverSettings") == tab}
        />
      </Tabs.Trigger>
    {/each}
  </Tabs.List>
  <div class="childrenContainer">
    {@render tabsContentSnippet?.()}
  </div>
</Tabs.Root>

<style>
  .childrenContainer {
    position: absolute;
    top: 150px;
    left: 63%;
    transform: translateX(-50%);
  }
</style>
