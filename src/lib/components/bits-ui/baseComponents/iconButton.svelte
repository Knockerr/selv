<script>
  import Icon from "$lib/components/Icon.svelte";

  const {
    iconPath = "16",
    iconSize,
    color = "#998fbb",
    onclick = () => {},
    spinOnClick = false,
    style,
  } = $props();

  let rotate = $state(false);
</script>

<button
  class="component"
  onclick={(e) => {
    if (spinOnClick) rotate = true;
    onclick(e);
  }}
  onanimationend={() => {
    rotate = false;
  }}
  class:spin={rotate}
  {style}
>
  <Icon path={iconPath} size={iconSize} {color} />
</button>

<style>
  .component {
    --containerEditButtonSize: 30px;
    background-color: transparent;
    border: 0px solid;
    border-radius: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 14px;
    width: var(--containerEditButtonSize);
    height: var(--containerEditButtonSize);
    transition: background-color 0.2s ease;
  }

  .component:hover {
    background-color: rgba(255, 255, 255, 0.2);
    cursor: pointer;
  }

  .component:active {
    transition:
      background-color 0s ease,
      color 0s ease;
    background-color: #121820;
    color: #998fbb;
  }

  .component.spin {
    animation: spin 0.4s ease;
  }

  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
