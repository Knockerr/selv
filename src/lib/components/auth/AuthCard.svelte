<script>
  const { children } = $props();
</script>

<div class="component">
  {@render children?.()}
</div>

<style>
.component{
    border: 1px solid var(--muted);
    border-radius: 20px;
    background-color: var(--background-alt);
    width: 25%;
    height: fit-content;
    max-height: 700px;
    padding: 30px;
    box-sizing: border-box;
}
</style>
