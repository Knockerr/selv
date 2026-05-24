<script>
  import { fly } from "svelte/transition";

  const { children } = $props();

  let isVisible = $state(false); // TODO

  function closeForm() {
    isVisible = false;
  }

  function showForm() {
    isVisible = true;
  }

  export { showForm };
</script>

{#if isVisible}
  <div class="component">
    <div
      class="backgroundBlocker"
      role="button"
      tabindex="0"
      onclick={(e) => {
        e.preventDefault();
        closeForm();
      }}
      onkeypress={(e) => {
        e.preventDefault();
        closeForm();
      }}
    >
      <div
        class="form"
        role="button"
        tabindex="0"
        onclick={(e) => {
          e.stopPropagation();
        }}
        onkeypress={(e) => {
          e.stopPropagation();
        }}
      >
        {@render children?.()}
      </div>
    </div>
  </div>
{/if}

<style>
  .backgroundBlocker {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: rgba(14, 22, 49, 0.308);
    z-index: 9998;
  }

  .form {
    background-color: black;
    width: 400px;
    height: fit-content;
    min-height: 100px;
    border: none;
    border-radius: 20px;
    z-index: 9999;
  }
</style>
