<script>
  const { label, width = "500px", children } = $props();
</script>

<div class="flex flex-col gap-0">
  <span class="text-base font-semibold" style:width>{label}</span>
  <div class="container">
    {@render children?.()}
  </div>
</div>

<style>
  .container {
    height: fit-content;
    background-color: #c1d6fd1a;
    border: 1px solid #dddddd48;
    border-radius: 15px;
    overflow: hidden;
  }
</style>
