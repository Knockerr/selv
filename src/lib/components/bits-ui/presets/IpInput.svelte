<script>
  import RestrictedInput from "../baseComponents/RestrictedInput.svelte";

  let { value = $bindable(""), label = false, width="300px", className, onchange = () => {} } = $props();
</script>

<RestrictedInput
  bind:value
  label={label ?? ""}
  placeholder="monServeur"
  ending=".nomLogiciel.com"
  {width}
  {className}
  {onchange}
/>
