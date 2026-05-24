<script>
  let {
    value = $bindable(true),
    sliderColor = "#2a47c9",
    handleColorTrue = "#37e6b2",
    handleColorFalse = "#2472e0",
    onSwitch = () => {},
  } = $props();

  let handlePos = $derived(value ? "20px" : "0");
  let handleColor = $derived(value ? handleColorTrue : handleColorFalse);

  $inspect(value);
</script>

<div class="component">
  <div
    class="slider"
    onclick={() => {
      value = !value;
      onSwitch();
    }}
    role="button"
    tabindex="0"
    onkeypress={() => {
      value = !value;
      onSwitch();
    }}
    style="background-color: {sliderColor};"
  >
    <div
      class="handle"
      style="left: {handlePos}; background-color: {handleColor};"
    ></div>
  </div>
</div>

<style>
  .component {
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .slider {
    width: 40px;
    height: 20px;
    border-radius: 999px;
    padding: 0;
    z-index: 5;
  }

  .handle {
    height: 20px;
    width: 20px;
    border: none;
    border-radius: 50%;
    z-index: 20;
    position: relative;
    transition:
      left 0.2s ease,
      background-color 0.3s ease;
  }
</style>
