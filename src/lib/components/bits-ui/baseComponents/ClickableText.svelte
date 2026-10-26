<script>
  const { children, style, onclick = () => {} } = $props();
</script>

<button class="component" {onclick} {style}>
  {@render children?.()}
</button>

<style>
  .component {
    display: inline;
    padding: 0;
    margin: 0;
    gap: 5px;
    height: fit-content;
    background-color: transparent;
    outline: none;
    border: none;
    text-decoration: underline;
    color: var(--emphasized);
  }

  .component:hover {
    cursor: pointer;
  }
</style>
