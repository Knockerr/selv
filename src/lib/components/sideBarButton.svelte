<script>
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";
  import Icon from "./Icon.svelte";

  let {
    path = "M3 12h18M12 3v18",
    title = "undefined",
    classes,
    id,
    href,
    num = 0,
    onclick = () => {},
    noselect = false,
  } = $props();
  let fillColor = $state("#ddd");
  let bgColor = $state("111825");
  const size = "28px";

  let visible = $state(false);

  let isSelected = $derived(sidebarStore.currentTab("main") == title);

  onMount(() => {
    setTimeout(() => {
      visible = true;
    }, num * 100);
  });
</script>

{#if visible}
  <li class={classes} {id} transition:fly={{ x: -10, duration: 500 }}>
    {#if href}
      <a
        {href}
        class="button"
        aria-label={title}
        class:selected={isSelected}
        onclick={() => {
          if (noselect) return;
          sidebarStore.setCurrentTab("main", title);
        }}
      >
        <Icon {path} {size} />
      </a>
    {:else}
      <button class="button" {onclick} aria-label={title}>
        <Icon {path} {size} />
      </button>
    {/if}

    <p>{title}</p>
  </li>
{/if}

<style>
  @import url("https://fonts.googleapis.com/css2?family=Open+Sans:ital,wdth,wght@0,96.2,335;1,96.2,335&display=swap");

  .button {
    font-size: 25px;
    padding: 10px;
    width: 30px !important;
    height: 30px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #111825;
    border: 0;
    border-radius: 15px;
    margin: 0 auto;
    color: white;
    transition:
      color 0.4s ease,
      background-color 0.4s ease;
    text-decoration: none;
  }

  button.button {
    box-sizing: content-box;
    flex-shrink: 0;
}

button.button :global(svg) {
    width: 28px;
    height: 28px;
    min-width: 28px;
    min-height: 28px;
}

  .button :global(svg) {
    fill: whitesmoke;
  }

  .button:hover :global(svg) {
    fill: #674dbd;
  }

  .button:hover {
    background-color: #1f2937;
    cursor: pointer;
  }

  .button.selected :global(svg) {
    fill: #674dbd;
  }

  .button.selected {
    background-color: #1f2937;
  }

  p {
    font-size: 12.5px;
    font-family: "Open Sans", sans-serif;
    font-optical-sizing: auto;
    font-weight: 335;
    font-style: normal;
    font-variation-settings: "wdth" 96.2;
    color: white;
    text-decoration: none;
    margin-top: 2px;
  }

  #topOptions {
    list-style-type: none;
    padding: 0;
    background-color: #111825;
  }

  #bottomOptions {
    list-style-type: none;
    padding: 0;
    position: absolute;
    bottom: 0;
  }

  .topOptions,
  .bottomOptions {
    font-family: "Roboto", sans-serif;
    list-style: none;
    list-style-type: none;
    color: white;
    text-align: center;
    font-size: 20px;
    padding: 20px, 10px;
    display: flex;
    flex-direction: column;
  }

  .topOptions:first-child .button{
    margin-top: 15px;
  }

  .topOptions .button {
    margin-top: 20px;
  }

  .bottomOptions {
    display: flex;
    flex-direction: column;
    margin-top: 0;
  }

  .bottomOptions .button {
    margin-top: 5px;
  }

</style>
