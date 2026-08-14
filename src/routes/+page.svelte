<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  onMount(() => {
    goto("/authentication");
  });
</script>

<div class="container"></div>
	<h1>Chargement...</h1>
<style>
  .container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }
</style>
