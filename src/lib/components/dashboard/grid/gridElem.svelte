<script>
  import IconButton from "$lib/components/bits-ui/baseComponents/iconButton.svelte";
  import Icon from "$lib/components/Icon.svelte";
  import { pathDb } from "$lib/icons/pathDb";

  const { title, children, reloadable = false, onReload = () => {} } = $props();
</script>

<div class="component">
  {#if title}
    <h2 class="title">{title}</h2>
  {/if}
  <div class="childrenContainer">
    {@render children?.()}
  </div>
  {#if reloadable}
    <IconButton
      iconPath={pathDb.arrowClockwise}
      iconSize="18"
      onclick={onReload}
      color="white"
      style="position: absolute; top: 13px; right: 13px;"
      spinOnClick
    />
  {/if}
</div>

<style>
  .component {
    height: 100%;
    width: 100%;
    background-color: var(--background-dark);
    border: 1px solid rgb(100, 100, 100);
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    font-size: 1.2rem;
    position: relative;
    overflow: hidden;
    overflow-x: scroll;
  }

  .title {
    position: relative;
    color: var(--foreground-alt);
    font-size: 1.1rem;
    font-weight: 400;
    width: 100%;
    padding-left: 10px;
    box-sizing: border-box;
  }

  .childrenContainer {
    flex: 1;
  }
</style>
