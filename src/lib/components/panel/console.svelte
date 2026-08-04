<script>
  // @ts-nocheck
  const { consoleContent = $bindable(), uuid } = $props();

  let currentCommand = $state("");
  let textareaEl = $state();
  let isPinnedToBottom = $state(true);
  const bottomLimit = 30;

  function handleScroll() {
    if (!textareaEl) return;
    const { scrollTop, scrollHeight, clientHeight } = textareaEl;
    isPinnedToBottom = scrollHeight - scrollTop - clientHeight < bottomLimit;
  }

  $effect(() => {
    consoleContent;
    if (isPinnedToBottom && textareaEl) {
      requestAnimationFrame(() => {
        textareaEl.scrollTop = textareaEl.scrollHeight;
      });
    }
  });

  async function sendCommand() {
    console.info("JE SEND" + $state.snapshot(currentCommand));
    const _ = await fetch(
      "http://localhost:8000/api/servers/" + uuid + "/sendCommand",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: currentCommand }),
      },
    )
      .then((res) => res.json())
      .then((data) => console.log("data -> ", data))
      .catch((error) => console.error(error));
  }

  function handleKeydown(e) {
    if (e.key !== "Enter") return;
    sendCommand();
    currentCommand = "";
  }
</script>

<div class="component">
  <div class="console">
    <textarea
      bind:this={textareaEl}
      onscroll={handleScroll}
      id="consoleContent"
      class="consoleContent"
      spellcheck="false"
      readonly>{consoleContent}</textarea
    >
  </div>
  <div class="sendCommandLine">
    <input
      type="text"
      class="commandTextInput"
      id="commandTextInput"
      placeholder="Commande.."
      bind:value={currentCommand}
      onkeydown={handleKeydown}
    />
    <button
      class="sendCommandButton"
      id="sendCommandButton"
      onclick={() => {
        sendCommand();
        currentCommand = "";
      }}
    >
      SEND
    </button>
  </div>
</div>

<style>
  .component {
    --accent: #6e41e2;
    --accent-hover: #8151f8;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 80%;
    width: 70%;
    box-shadow: 0 0 2px var(--dark-10);
    border-radius: 10px;
  }

  .console {
    width: 100%;
    height: 100%;
    background-color: var(--background-dark);
    border: 2px solid var(--border-input);
    border-radius: 10px 10px 0 0;
    border-bottom: none;
    padding: 10px;
    box-sizing: border-box;
    overflow: hidden;
  }

  .consoleContent {
    width: 100%;
    height: 100%;
    outline: none;
    border: none;
    box-sizing: border-box;
    padding: 5px;
    font-size: 0.85rem;
    letter-spacing: 0.3px;
    font-weight: 200;
    font-family: "Open Sans", sans-serif;
    background-color: transparent;
    cursor: default;
    color: var(--foreground);
    resize: none;
  }

  .sendCommandLine {
    display: flex;
    width: 100%;
    box-sizing: border-box;
  }

  .commandTextInput {
    flex: 1;
    outline: none;
    border: 2px solid var(--border-input);
    height: 25px;
    padding: 10px;
    box-sizing: border-box;
    background-color: var(--background-dark);
    color: var(--foreground);
    border-bottom-left-radius: 10px;
    font-family: "Open Sans", sans-serif;
    transition: border-color 0.2s ease;
  }

  .commandTextInput:focus {
    border-color: var(--border-input-hover);
  }

  .sendCommandButton {
    height: 100%;
    width: 70px;
    background-color: var(--muted);
    color: var(--foreground);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid var(--border-input);
    border-left: none;
    border-top: none;
    border-bottom-right-radius: 10px;
    cursor: pointer;
    font-family: "Open Sans", sans-serif;
    font-weight: 600;
    transition:
      background-color 0.2s ease,
      border-color 0.2s ease;
  }

  .sendCommandButton:hover {
    background-color: var(--accent);
    border-color: var(--accent);
  }

  .sendCommandButton:active {
    transition: background-color 0s;
    background-color: var(--accent-hover);
  }
</style>
