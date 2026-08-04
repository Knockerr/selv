<script>
  import SaveSnackbar from "$lib/components/bits-ui/baseComponents/SaveSnackbar.svelte";
  import CustomTabs from "$lib/components/bits-ui/baseComponents/Tabs.svelte";
  import ServerParametersContainer from "$lib/components/bits-ui/presets/ServerParametersContainer.svelte";
  import { settingsBank } from "$lib/components/panel/settings/settingsBank.svelte";
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { Tabs } from "bits-ui";
  import { onMount, untrack } from "svelte";

  const params = new URLSearchParams(window.location.search);
  let uuid = params.get("uuid") ?? "demoUuid";

  onMount(() => {
    sidebarStore.setCurrentTab("panel", "Parametres");
  });

  let values = $state({});

  let isPageDirty = $derived.by(() => {
    if (!values) return false;
    return Object.values(values).some((value) => value.isDirty);
  });

  function cancelChanges() {
    Object.keys(values).forEach((property) => {
      values[property].currentValue = values[property].initValue;
    });
  }

  function redefineDirty() {
    Object.keys(values).forEach((property) => {
      const isValDirty =
        values[property]["initValue"] !== values[property]["currentValue"];

      untrack(() => {
        values[property]["isDirty"] = isValDirty;
      });
    });
  }

  $effect(() => {
    if (!values) return;
    redefineDirty();
  });

  async function sendChanges() {
    const dirtyProperties = Object.keys(values).filter(
      (property) => values[property].isDirty,
    );
    if (!dirtyProperties) {
      console.error("None of the values are dirty..");
      return;
    }
    console.warn("dirtyProperties", dirtyProperties);
    const dirtyPropertiesClean = Object.fromEntries(
      dirtyProperties.map((property) => [
        property,
        values[property].currentValue,
      ]),
    );
    console.warn("dirtyPropertiesClean", dirtyPropertiesClean);
    const res = await fetch(
      "http://localhost:8000/api/servers/" + uuid + "/editProperties",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          datas: dirtyPropertiesClean,
        }),
      },
    );
    values = await loadProperties();
  }
</script>

<div class="component">
  <h1 class="title">Paramètres</h1>
  <CustomTabs
    tabNames={["Jeu", "Monde", "Serveur"]}
    tabListClass="flex flex-row justify-center mb-8"
  >
    {#snippet tabsContentSnippet()}
      <Tabs.Content value="Jeu">
        <ServerParametersContainer
          settings={settingsBank.filter(
            (setting) => setting.category === "game",
          )}
          label="Test label"
          {uuid}
          {values}
        />
      </Tabs.Content>
      <Tabs.Content value="Monde">
        <ServerParametersContainer
          settings={settingsBank.filter(
            (setting) => setting.category === "world",
          )}
          label="Test label"
          {uuid}
          {values}
        />
      </Tabs.Content>
      <Tabs.Content value="Serveur">
        <ServerParametersContainer
          settings={settingsBank.filter(
            (setting) => setting.category === "server",
          )}
          label="Test label"
          {uuid}
          {values}
        />
      </Tabs.Content>
    {/snippet}
  </CustomTabs>
</div>

<SaveSnackbar
  label="Une ou plusieurs modifications ne sont pas sauvegardées!"
  oncancel={cancelChanges}
  onsave={sendChanges}
  className="relative bottom-40 w-fit left-[50%] translate-[-50%]"
  bind:visible={isPageDirty}
/>

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
