<script>
  // @ts-nocheck
  import { pathDb } from "$lib/icons/pathDb";
  import Icon from "../../Icon.svelte";

  const {
    iconPath = pathDb.cross,
    iconSize = "18px",
    emphasize = false,
    style = "",
    onclick,
    label,
    className = "",
    disabled = false,
    children,
    ...others
  } = $props();
</script>

<div class="flex flex-col gap-1">
  {#if label}
    <span class="text-sm font-semibold text-foreground" onclick={(e) => {e.stopPropagation()}}
      >{label}</span
    >
  {/if}
  <button
    class="component {className}"
    class:emphasize
    {onclick}
    {style}
    {disabled}
    {...others}
  >
    {#if iconPath}
      <div class="iconContainer">
        <Icon path={iconPath} size={iconSize} color="white" />
      </div>
    {/if}
    <p>{@render children?.()}</p>
  </button>
</div>

<style>
  .component {
    background-color: transparent;
    border: 1px solid var(--border-input);
    border-radius: 7px;
    color: white;
    font-family: "Open Sans", sans-serif;
    height: 37px;
    font-size: 14px;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    transition:
      background-color 0.3s ease,
      transform 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .component.emphasize {
    background-color: #6e41e2;
  }

  .component::after {
    content: "";
    height: 125%;
    width: 125%;
    z-index: 999;
    position: absolute;
    background-color: transparent;
    transition: 0.3s ease all;
  }

  .component:hover::after {
    background-color: rgb(255, 255, 255, 0.1);
    cursor: pointer;
  }

  .component:disabled::after {
    background-color: rgb(0, 0, 0, 0.5);
    cursor: pointer;
  }
  .component:disabled {
    border: none;
  }

  .component:hover .iconContainer {
    transform: scale(1.1);
  }

  .component:hover p {
    transform: scale(1);
  }

  .component:active {
    transition: background-color 0s;
    background-color: rgb(255, 255, 255, 0.15);
  }

  .component.emphasize:active {
    transition: background-color 0s;
    background-color: #8151f8;
  }

  .iconContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease;
  }

  p,
  .iconContainer {
    margin: 0;
  }
</style>
