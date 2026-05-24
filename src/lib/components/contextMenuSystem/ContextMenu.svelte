<script>
  // @ts-nocheck
  import { pathDb } from "$lib/icons/pathDb";
  import { fade, fly } from "svelte/transition";
  import Icon from "../Icon.svelte";
  import { contextManager } from "./contextMenuManager.svelte";

  // Récuperation des enfants
  const { children = null, posx, posy, contextId } = $props();
</script>

<div
  class="menu"
  style="left: {posx}px; top: {posy}px;"
  transition:fly|local={{ y: 20, duration: 100 }}
  role="button"
  tabindex="0"
  onclick={(e) => {
    e.stopPropagation();
  }}
  onkeypress={(e) => {
    e.stopPropagation();
  }}
>
  {@render children?.()}
</div>


<style>
  .menu {
    position: absolute;
    width: fit-content;
    top: 50%;
    right: 50%;
    transform: translate(50%, -50%);
    background-color: #030712;
    border: 1.25px solid rgb(11, 17, 29);
    box-shadow: 0 0 10px #53505018;
    border-radius: 30px;
    z-index: 999999;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    padding: 0 20px;
    overflow-x: hidden;
    overflow-y: scroll;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
</style>
