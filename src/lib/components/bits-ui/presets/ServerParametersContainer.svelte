<script>
  import Container from "../baseComponents/Container.svelte";
  import Input from "../baseComponents/Input.svelte";
  import Select from "../baseComponents/select.svelte";
  import Switch from "../baseComponents/switch.svelte";
  import Number from "../baseComponents/number.svelte";
  import { onMount, untrack } from "svelte";
  import { error } from "@sveltejs/kit";
  import { load } from "@tauri-apps/plugin-store";
  import PanelSettingsBlock from "./panelSettingsBlock.svelte";
  import PanelSettingsItem from "./panelSettingsItem.svelte";

  // Settings corresponds to an array of settings from settingsBank
  let { uuid, settings, label, values = $bindable() } = $props();

  let valuesInitialized = $state(false);

  async function loadProperties() {
    let result = {};
    // TODO : Optimize, not fetching in each tab
    const response = await fetch(
      "http://localhost:40401/api/servers/" + uuid + "/properties",
    );
    const datas = await response.json();
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

  onMount(async () => {
    const res = await loadProperties();
    Object.assign(values, res);
    valuesInitialized = true;
  });
</script>

<PanelSettingsBlock {label}>
  {#if valuesInitialized}
    {#each settings as setting}
      <PanelSettingsItem
        title={setting.name}
        description={setting.description}
        inputPlaceholder={values[setting.property]["initValue"]}
        inputItems={setting.options ?? ""}
        iconPath={setting.iconPath}
        bind:value={values[setting.property].currentValue}
        inputType={setting.type}
      />{/each}
  {/if}
</PanelSettingsBlock>
