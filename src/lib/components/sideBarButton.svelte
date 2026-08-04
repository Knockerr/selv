<script>
  import { sidebarStore } from "$lib/sideBarsStore.svelte";
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";

  let {
    path = "M3 12h18M12 3v18",
    title = "undefined",
    classes,
    id,
    href,
    num = 0,
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
    <a {href} aria-label={title} class:selected={isSelected} onclick={() => {sidebarStore.setCurrentTab("main", title)}}>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width={size}
        height={size}
        viewBox="0 0 256 256"
      >
        <path d={path} />
      </svg>
    </a>

    <p>{title}</p>
  </li>
{/if}

<style>
  @import url("https://fonts.googleapis.com/css2?family=Open+Sans:ital,wdth,wght@0,96.2,335;1,96.2,335&display=swap");

  a {
    font-size: 25px;
    padding: 10px;
    width: 30px;
    height: 30px;
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

  a svg {
    fill: whitesmoke;
  }

  a:hover svg {
    fill: #674dbd;
  }

  a:hover {
    background-color: #1f2937;
  }

  a.selected svg {
    fill: #674dbd;
  }

  a.selected {
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

  .topOptions {
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

  .topOptions a {
    margin-top: 30px;
  }

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
    margin-top: 0;
  }

  .bottomOptions a {
    margin-top: 5px;
  }

  #dashboard {
    margin-top: 0;
    padding-top: 0;
  }
</style>
