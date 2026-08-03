<script>
  const {
    path,
    color = "#ddd",
    size = "32",
    style,
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
  {style}
  viewBox={vb}><path d={path}></path></svg
>
