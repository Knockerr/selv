<script>
  import Icon from "../Icon.svelte";

  const {
    label,
    iconPath,
    iconSize,
    children,
    selected,
    width = "100%",
    height = "40px",
    style,
    fontSize = "1rem",
    labelStyle,
    onclick,
  } = $props();
</script>

<button
  class="component"
  style:height
  style:width
  class:selected
  {style}
  {onclick}
>
  <div class="labelContainer">
    {#if iconPath}
      <Icon path={iconPath} size={iconSize} />
    {/if}
    <span class="label" style={labelStyle} style:font-size={fontSize}
      >{label}</span
    >
  </div>
  {@render children?.()}
</button>

<style>
  .component {
    background-color: #040713;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 5px;
    border: 0px solid;
    border-radius: 10px;
    transition:
      background-color 0.15s ease,
      color 0.15s ease;
    padding: 5px;
    padding-left: 10px;
    color: var(--foreground-alt);
  }

  .labelContainer {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .component:hover {
    background-color: #283446;
    cursor: pointer;
    color: var(--foreground);
  }

  .component.selected {
    background-color: #283446 !important;
    color: var(--foreground);
  }
</style>
