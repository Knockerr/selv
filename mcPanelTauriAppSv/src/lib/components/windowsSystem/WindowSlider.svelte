<script>
  // @ts-nocheck
  import SliderSwitch from "../SliderSwitch.svelte";

  let { value = $bindable() } = $props();
</script>

<div class="component">
  <SliderSwitch bind:value />
</div>

<style>
  .component {
    margin: 0;
    margin-bottom: 10px;
  }
</style>
