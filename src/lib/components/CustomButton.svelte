<script>
  // @ts-nocheck
  import { pathDb } from "$lib/icons/pathDb";
  import Icon from "./Icon.svelte";

  const {
    iconPath,
    iconSize = "18px",
    emphasize = false,
    style = "",
    onclick,
    children,
    ...others
  } = $props();

  const color = $derived(emphasize ? "#6e41e2" : "transparent");
  const hoverColor = $derived(
    emphasize ? "#8151f8" : "rgb(255, 255, 255, 0.1)",
  );
  const activeColor = $derived(
    emphasize ? "#7140ee" : "rgb(255, 255, 255, 0.15)",
  );
</script>

<button
  class="component"
  style={`--bgColor: ${color}; --bgHoverColor: ${hoverColor}; --bgActiveColor: ${activeColor}; ${style}`}
  {onclick}
  {...others}
>
  <div class="iconContainer">
    <Icon path={iconPath} size={iconSize} color="white" />
  </div>
  <p>{@render children?.()}</p>
</button>

<style>
  .component {
    --bgColor: #ddd;
    --bgHoverColor: #ddd;
    --bgActiveColor: #ddd;
  }

  .component {
    background-color: var(--bgColor);
    border: 1px solid #1f2937;
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
  }

  .component:hover {
    background-color: var(--bgHoverColor);
  }

  .component:hover .iconContainer {
    transform: scale(1.1);
  }

  .component:hover p {
    transform: scale(1);
  }

  .component:active {
    transition: background-color 0s;
    background-color: var(--bgActiveColor);
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
