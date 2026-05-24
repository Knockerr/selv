<script>
  let {
    title = "UNDEFINED",
    color = "#ddd",
    path = "M3 12h18M12 3v18",
    classes = "",
    id = "",
  } = $props();
  const size = $derived(id === "accountButton" ? "35px" : "20px");
</script>

<button aria-label={title} class={classes} {id}>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    fill={color}
    viewBox="0 0 256 256"><path d={path}></path></svg
  >
  <p>{title}</p>
</button>

<style>
  .topButton {
    background-color: transparent;
    border: 1px solid #1f2937;
    border-radius: 7px;
    color: white;
    font-family: "Open Sans", sans-serif;
    font-size: 1rem;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    gap: 5px;
    transition:
      background-color 0.3s ease,
      transform 0.3s ease;
    height: 42px;
  }

  .topButton svg {
    transition: transform 0.3s ease;
    will-change: transform;
  }

  .topButton:hover {
    background-color: rgba(255, 255, 255, 0.05);
    cursor: pointer;
  }

  .topButton:hover p {
    transform: scale(1);
  }

  .topButton:hover svg {
    transform: scale(1.1);
  }

  .topButton:active {
    transition: background-color 0s;
    background-color: rgba(255, 255, 255, 0.1);
  }

  #serverNumberButton {
    margin-right: -10px;
  }

  #accountButton {
    position: relative;
    margin-right: 2px;
    background-color: #624dd8;
    border: 0px solid black;
    border-radius: 50%;
    transition:
      background-color 0.3s ease,
      transform 0.3s ease;
    text-decoration: none;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 45px;
    width: 45px;
  }

  #accountButton:hover {
    background-color: #6b56e0;
    transform: scale(1.04);
    cursor: pointer;
  }
</style>
