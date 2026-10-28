<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import Loader from "$lib/components/bits-ui/baseComponents/Loader.svelte";
  import { check } from "@tauri-apps/plugin-updater";

  async function isUpdate() {
    try {
      let update = await check();
      if (update) return true;
      else return false;
    } catch (error) {
      return false;
    }
  }

  onMount(async () => {
    const isUpdateAvailable = await isUpdate();
    // Check for updates
    if (isUpdateAvailable) {
      console.log("Update detected, redirecting to update...")
      goto("/update");
    } else {
      console.log("No update detected, redirecting to auth...")
      goto("/authentication");
    }
  });
</script>

<div class="container">
  <Loader width="150px" height="150px" />
</div>

<style>
  .container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }
</style>
