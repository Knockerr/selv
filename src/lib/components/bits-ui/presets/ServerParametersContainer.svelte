<script>
  import Container from "../baseComponents/Container.svelte";
  import Input from "../baseComponents/Input.svelte";
  import Select from "../baseComponents/select.svelte";
  import Switch from "../baseComponents/switch.svelte";
  import SaveSnackbar from "../baseComponents/SaveSnackbar.svelte";
  import Number from "../baseComponents/number.svelte";
  import { onMount, untrack } from "svelte";
  import { error } from "@sveltejs/kit";

  // Settings corresponds to an array of settings from settingsBank
  const { uuid, settings, label } = $props();

  let values = $state();

  let isPageDirty = $derived.by(() => {
    if (!values) return false;
    return Object.values(values).some((value) => value.isDirty);
  });
  $inspect(isPageDirty).with(() => {
    console.warn("isPageDirty", isPageDirty);
  });
  let valuesInitialized = $state(false);

  function formatType(val) {
    if (val === "true") return true;
    if (val === "false") return false;
    return val;
  }

  async function loadProperties() {
    let result = {};
    // TODO : Optimize, not fetching in each tab
    const response = await fetch(
      "http://localhost:8000/api/servers/" + uuid + "/properties",
    );
    const datas = await response.json();
    console.warn(datas);
    const properties = datas.properties;
    settings.forEach((setting) => {
      const property = setting.property;
      let currentVal = properties[property];
      if (!currentVal && currentVal !== "") {
        console.error("Impossible to get property", property);
        return;
      }
      if (currentVal === "true") currentVal = true;
      if (currentVal === "false") currentVal = false;
      result[property] = {
        initValue: currentVal,
        currentValue: currentVal,
        isDirty: false,
      };
    });
    return result;
  }

  function cancelChanges() {
    Object.keys(values).forEach((property) => {
      values[property].currentValue = values[property].initValue;
    });
  }

  onMount(async () => {
    values = await loadProperties();
    valuesInitialized = true;
  });

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

<Container {label}>
  {#each settings as setting}
    <div class="itemContainer">
      <div class="leftSide">
        <span class="title">{setting.name}</span>
        <span class="description">{setting.description}</span>
      </div>
      {#if valuesInitialized}
        {#if setting.type == "select"}
          <Select
            bind:value={values[setting.property].currentValue}
            items={setting.options}
            width="120px"
            style="max-height: 45px;"
          />
        {:else if setting.type === "bool"}
          <Switch bind:checked={values[setting.property].currentValue} />
        {:else if setting.type === "input"}
          <Input
            placeholder={values[setting.property]["initValue"]}
            iconPath={setting.iconPath}
            bind:value={values[setting.property].currentValue}
            width="200px"
          />
        {:else if setting.type === "number"}
          <Number
            placeholder={values[setting.property]["initValue"]}
            iconPath={setting.iconPath}
            bind:value={values[setting.property].currentValue}
            width="50px"
          />
        {/if}
      {/if}
    </div>
  {/each}
</Container>

<SaveSnackbar
  label="Une ou plusieurs modifications ne sont pas sauvegardées!"
  oncancel={cancelChanges}
  onsave={sendChanges}
  className="absolute bottom-20"
  bind:visible={isPageDirty}
/>

<style>
  .itemContainer {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #dddddd48;
    padding: 15px 15px;
  }

  .leftSide {
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 2px;
    justify-content: center;
  }

  .title {
    font-size: 1rem;
  }

  .description {
    max-width: 320px;
    color: var(--color-foreground-alt);
    font-size: 0.8rem;
  }
</style>
