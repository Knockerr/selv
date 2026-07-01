<script>
  import Icon from "$lib/components/Icon.svelte";

  const { iconPath="16", iconSize, onClick } = $props();
</script>

<button class="composant" onclick={onClick}>
  <Icon path={iconPath} size={iconSize} color="#998fbb" />
</button>

<style>
  .composant {
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

  .composant:hover {
    background-color: #1d2735;
  }

  .composant:active {
    transition:
      background-color 0s ease,
      color 0s ease;
    background-color: #121820;
    color: #998fbb;
  }
</style>
