<script>
  import { goto } from "$app/navigation";
  import Tile from "$lib/components/bits-ui/Tile.svelte";
  import { settingsBank } from "$lib/components/panel/settings/settingsBank.svelte";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";

  const sections = [
    { name: "Compte", href: "/core/settings/account" },
    { name: "Sécurité", href: "/core/settings/security" },
    { name: "Serveurs", href: "/core/settings/servers" },
  ];
</script>

<div class="component">
  <div class="sections">
    {#each sections as section}
      <Tile
        label={section.name}
        height="35px"
        width="100%"
        labelStyle="font-weight: 600;"
        onclick={() => {
          goto(section.href);
          sidebarStore.setCurrentTab("settings", section.name);
        }}
        selected={sidebarStore.currentTab("settings") === section.name}
      />
    {/each}
  </div>
</div>

<style>
  .component {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 240px;
    padding: 10px;
    padding-left: 0;
    padding-top: 0;
  }

  .sections {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 100%;
  }
</style>
