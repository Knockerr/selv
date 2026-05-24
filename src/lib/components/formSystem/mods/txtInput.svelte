<script>
  let { input = "", value = $bindable() } = $props();
</script>

<input type="text" placeholder={input} bind:value={value}>

<style>
  input {
    color: #ddd;
    font-size: 20px;
  }
</style>
