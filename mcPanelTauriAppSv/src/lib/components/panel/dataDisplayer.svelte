<script>
  const { stat, value = $bindable() } = $props();
</script>

<div class="component">
  <div class="label">{stat}</div>
  <p class="displayer">{value ?? "TODO"}</p>
</div>

<style>
  .component {
    height: 80px;
    width: 100%;
    border: 1px solid #5581a5;
    border-radius: 10px;
    background-color: rgb(41, 58, 104);;
    display: flex;
    flex-direction: column;
    justify-content: center;
    color: whitesmoke;
    padding: 10px;
    box-sizing: border-box;
    gap: 2px;
  }

  .label {
    color: rgba(255, 255, 255, 0.712);
    margin: 0;
    padding: 0;
    font-weight: 400;
    font-family: var(--funnelFont);
    font-size: 0.8rem;
    margin-left: 5px;
  }

  .displayer {
    padding: 0;
    margin: 0;
    font-weight: 400;
    font-family: sans-serif;
    font-size: 1.3rem;
    font-family: var(--zainFont);
    margin-left: 6px;
  }
</style>
