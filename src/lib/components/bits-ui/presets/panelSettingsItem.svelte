<script>
  import Input from "../baseComponents/Input.svelte";
  import Number from "../baseComponents/number.svelte";
  import Select from "../baseComponents/select.svelte";
  import Switch from "../baseComponents/switch.svelte";

  let {
    title,
    description,
    inputType,
    inputItems,
    inputPlaceholder,
    iconPath,
    value = $bindable(),
  } = $props();
</script>

<div class="itemContainer">
  <div class="leftSide">
    <span class="title">{title}</span>
    <span class="description">{description}</span>
  </div>
  {#if inputType == "select"}
    <Select
      bind:value
      items={inputItems}
      width="120px"
      style="max-height: 45px;"
      {iconPath}
    />
  {:else if inputType === "bool"}
    <Switch bind:checked={value} />
  {:else if inputType === "input"}
    <Input placeholder={inputPlaceholder} {iconPath} bind:value width="200px" />
  {:else if inputType === "number"}
    <Number placeholder={inputPlaceholder} {iconPath} bind:value width="50px" />
  {/if}
</div>

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
