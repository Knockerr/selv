<script>
  import CustomTabs from "$lib/components/bits-ui/baseComponents/Tabs.svelte";
  import ServerParametersContainer from "$lib/components/bits-ui/presets/ServerParametersContainer.svelte";
  import { settingsBank } from "$lib/components/panel/settings/settingsBank.svelte";
  import { Tabs } from "bits-ui";

  //@ts-nocheck
  const params = new URLSearchParams(window.location.search);
  let uuid = params.get("uuid") ?? "demoUuid";
</script>

<div class="component">
  <h1 class="title">Paramètres</h1>
  <CustomTabs tabNames={["Jeu", "Monde", "Serveur"]} tabListClass="flex flex-row justify-center mb-8">
    {#snippet tabsContentSnippet()}
      <Tabs.Content value="Jeu">
        <ServerParametersContainer
          settings={settingsBank.filter(
            (setting) => setting.category === "game",
          )}
          label="Test label"
          {uuid}
        />
      </Tabs.Content>
      <Tabs.Content value="Monde">
        <ServerParametersContainer
          settings={settingsBank.filter(
            (setting) => setting.category === "world",
          )}
          label="Test label"
          {uuid}
        />
      </Tabs.Content>
      <Tabs.Content value="Serveur">
        <ServerParametersContainer
          settings={settingsBank.filter(
            (setting) => setting.category === "server",
          )}
          label="Test label"
          {uuid}
        />
      </Tabs.Content>
    {/snippet}
  </CustomTabs>
</div>

<style>
  .component {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: transparent;
  }

  .component:hover {
    background-color: transparent;
  }

  .title {
    width: 100%;
    padding: 5px 50px;
    box-sizing: border-box;
    font-family: var(--robotFont);
    font-size: 3rem;
    font-weight: 500;
  }
</style>
