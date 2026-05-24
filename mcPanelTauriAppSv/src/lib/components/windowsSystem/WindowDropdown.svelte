<script>
  let { value = $bindable(), options, children } = $props();

  const dropDownId = crypto.randomUUID();
</script>

<select name={dropDownId} bind:value>
  {#each options as option (option)}
    <option value={option}>{option}</option>
  {/each}
</select>
