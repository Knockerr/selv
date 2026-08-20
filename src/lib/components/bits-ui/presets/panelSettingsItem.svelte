<script>
  import Button from "../baseComponents/Button.svelte";
  import Input from "../baseComponents/Input.svelte";
  import Number from "../baseComponents/number.svelte";
  import RestrictedInput from "../baseComponents/RestrictedInput.svelte";
  import Select from "../baseComponents/select.svelte";
  import Switch from "../baseComponents/switch.svelte";
  import IpInput from "./IpInput.svelte";

  let {
    title,
    description,
    inputType,
    inputItems,
    inputPlaceholder,
    inputLabel,
    iconPath,
    children,
    emphasize,
    itemDisabled,
    onclick = () => {},
    value = $bindable(),
  } = $props();
</script>

<div class="itemContainer" class:itemDisabled>
  <div class="leftSide">
    <span class="title">{title}</span>
    <span class="description">{description}</span>
  </div>
  <div class="flex flex-col gap-1">
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
      <Input
        placeholder={inputPlaceholder}
        {iconPath}
        bind:value
        width="200px"
      />
    {:else if inputType === "number"}
      <Number
        placeholder={inputPlaceholder}
        {iconPath}
        bind:value
        width="50px"
      />
    {:else if inputType === "ip"}
      <IpInput
        placeholder={inputPlaceholder}
        {iconPath}
        bind:value
        width="290px"
      />
    {:else if inputType === "button"}
      <Button {iconPath} bind:value {onclick} {emphasize}>{inputLabel}</Button>
    {/if}
    {@render children?.()}
  </div>
</div>

<style>
  .itemContainer {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #dddddd48;
    padding: 17px 17px;
    position: relative;
    overflow: hidden;
  }

  .itemContainer::after {
    z-index: 100;
    position: absolute;
    left: -500px;
    width: 2000px;
    height: 2000px;
    background-color: transparent;
  }

  .itemContainer.itemDisabled::after {
    background-color: rgba(0, 0, 0, 0.7);
    content: "";
  }

  .leftSide {
    height: 100%;
    max-width: 60%;
    display: flex;
    flex-direction: column;
    gap: 2px;
    justify-content: center;
  }

  .title {
    font-size: 1.1rem;
  }

  .description {
    max-width: 320px;
    color: var(--color-foreground-alt);
    font-size: 0.85rem;
    letter-spacing: 0.15px;
  }
</style>
