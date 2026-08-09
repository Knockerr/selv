<script>
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";

  const {
    label = "",
    iconPath = pathDb.arrowLeft,
    color,
    disabled = false,
    onclick = () => {},
  } = $props();

  const colorChecked = $derived(color ? color : "rgb(70, 70, 70)");
</script>

<button
  class="component"
  style:background-color={colorChecked}
  {onclick}
  {disabled}
>
  <Icon path={iconPath} size="23" />
  <span>
    {label}
  </span>
</button>

<style>
  .component {
    border: 1px solid var(--border-input);
    border-radius: 10px;
    color: white;
    font-family: "Open Sans", sans-serif;
    width: 90%;
    height: 43px;
    font-size: 14px;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition:
      background-color 0.3s ease,
      transform 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .component::after {
    content: "";
    position: relative;
    left: -100px;
    height: 125%;
    width: 150%;
    z-index: 999;
    position: absolute;
    background-color: transparent;
    transition: 0.3s ease all;
  }

  .component:hover::after {
    background-color: rgb(0, 0, 0, 0.1);
    cursor: pointer;
  }

  .component:disabled::after {
    background-color: rgb(0, 0, 0, 0.6);
    cursor: default;
  }
  .component:disabled {
    color: var(--foreground-alt);
    border: none;

    cursor: default;
  }

  span {
    font-family: var(--robotoFont);
    font-weight: 400;
    font-size: 1rem;
  }
</style>
