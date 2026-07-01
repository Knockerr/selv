<script>
  const {
    path,
    color = "#ddd",
    size = "32",
    className="",
    vb = "0 0 256 256",
    onclick = () => {},
  } = $props();
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  width={size}
  height={size}
  class={className}
  fill={color}
  viewBox={vb}><path d={path}></path></svg
>
