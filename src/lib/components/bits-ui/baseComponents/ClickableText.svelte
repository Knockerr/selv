<script>
  const { children, style, onclick = () => {} } = $props();
</script>

<button class="component" {onclick} {style}>
  {@render children?.()}
</button>

<style>
  .component {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 5px;
    width: fit-content;
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
