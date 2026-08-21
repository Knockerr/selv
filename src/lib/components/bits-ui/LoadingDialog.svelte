<script>
  import { onMount } from "svelte";
  import Dialog from "./baseComponents/dialog.svelte";
  import Loader from "./baseComponents/Loader.svelte";
</script>

<Dialog empty name="loader">
  <div class="loaderContainer">
    <Loader />
  </div>
</Dialog>

<style>
  .loaderContainer {
    width: 100%;
    height: 300px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }
</style>
