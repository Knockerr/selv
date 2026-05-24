<script>
  let { value = $bindable(), placeholder } = $props();
</script>

<div class="component">
  <input type="text" class="textInput" bind:value={value} {placeholder} />
</div>

<style>
  .component {
    margin: 0;
    margin-bottom: 10px;
  }

  .textInput {
    background-color: #030712;
    border: 1px solid #1f2937;
    border-radius: 7px;
    color: #f5f5f5;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 15px;
    padding: 7px 12px;
  }
</style>
