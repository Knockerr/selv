<script>
  import Container from "../baseComponents/Container.svelte";

  const { children, label } = $props();
</script>

<Container {label}>
  {@render children?.()}
</Container>
