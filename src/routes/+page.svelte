<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import Loader from "$lib/components/bits-ui/baseComponents/Loader.svelte";

  onMount(() => {
    goto("/update");
    //goto("/authentication");
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
