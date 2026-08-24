<script>
  import { onMount } from "svelte";
  import Dialog from "./baseComponents/dialog.svelte";
  import Loader from "./baseComponents/Loader.svelte";
  import { uiStore } from "./uiComponentsStore.svelte";

  const loaderTitle = $derived(uiStore.loaderTitle);
</script>

<Dialog empty name="loader">
  <div class="dialogContainer">
    {#if loaderTitle}
      <h1>{loaderTitle}</h1>
    {/if}
    <div class="loaderContainer">
      <Loader />
    </div>
  </div>
</Dialog>

<style>
  .dialogContainer {
    height: 490px;
    width: 490px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  h1{
    font-size: 1.3rem;
  }

  .loaderContainer {
    width: 490px;
    flex: 1;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }
</style>
