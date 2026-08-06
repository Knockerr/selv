<script>
  const { title, description, input, onclick } = $props();
</script>

<button class="component" {onclick}>
  <div class="infos">
    <span class="title text-sm text-foreground font-semibold tracking-wide">{title}</span>
    <span class="description text-sm text-foreground-alt">{description}</span>
  </div>
  <div class="input">
    {@render input?.()}
  </div>
</button>

<style>
  .component {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 12px 15px;
    box-sizing: border-box;
    background: rgba(0, 0, 0, 0.15);
    border: 1px solid #dddddd62;
    border-radius: 15px;
    outline: none;
    text-align: left;
  }

  .component:hover {
    background: rgba(0, 0, 0, 0.295);
    cursor:default;
  }

  .infos {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
  }

  .input {
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
