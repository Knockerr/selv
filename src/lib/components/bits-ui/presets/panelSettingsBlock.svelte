<script>
  import Container from "../baseComponents/Container.svelte";

  const { children, label, width } = $props();
</script>

<Container {label} {width}>
  {@render children?.()}
</Container>
