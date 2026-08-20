<script>
  import { onMount } from "svelte";
  import Dialog from "./baseComponents/dialog.svelte";
</script>

<Dialog empty name="loader">
  <div class="loaderContainer">
    <div class="loader"></div>
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

  .loader {
    width: 100px;
    height: 100px;
    border: 6px solid transparent;
    border-top: 6px solid #3b82f6;
    border-bottom: 6px solid var(--emphasized);
    border-radius: 50%;
    animation: rotate 1s linear infinite;
  }

  @keyframes rotate {
    to {
      transform: rotate(360deg);
    }
  }
</style>
