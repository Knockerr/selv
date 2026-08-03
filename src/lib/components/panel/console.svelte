<script>
  // @ts-nocheck
  const { consoleContent = $bindable(), uuid } = $props();

  let currentCommand = $state("");

  function sendCommand() {
    fetch("http://localhost:8000/api/servers/" + uuid + "/sendCommand", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        command: currentCommand,
      }),
    })
      .then((res) => res.json())
      .then((data) => console.log("data -> ", data))
      .catch((error) => console.error(error));
  }
</script>

<div class="component">
  <div class="console">
    <textarea
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
      onkeydown={(e) => {
        if (event.key !== "Enter") return;
        sendCommand();
        currentCommand = "";
      }}
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
  :root {
    --consoleBg: #0b1020;
    --consoleInputBg: #070b17;
    --consoleBorder: #1f2a44;
    --consoleBorderShadow: #ffffff3b;
  }

  .component {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 80%;
    width: 70%;
    box-shadow: 0 0 5px var(--consoleBorderShadow);
    border-radius: 10px;
  }

  .console {
    width: 100%;
    height: 100%;
    background-color: var(--consoleBg);
    border: 2px var(--consoleBorder) solid;
    border-radius: 10px 10px 0 0;
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
    font-size: 0.8rem;
    letter-spacing: 0.2px;
    font-weight: 200;
    background-color: transparent;
    cursor: default;
    color: white;
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
    border: none;
    height: 25px;
    padding: 10px;
    box-sizing: border-box;
    background-color: var(--consoleInputBg);
    color: white;
    border: 2px var(--consoleBorder) solid;
    border-top: none;
    border-bottom-left-radius: 10px;
  }

  .sendCommandButton {
    height: 100%;
    width: 70px;
    background-color: var(--consoleBorder);
    color: white;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: 0 20px;
    border: 2px var(--consoleBorder) solid;
    border-left: none;
    border-top: none;
    border-bottom-right-radius: 10px;
    cursor: pointer;
    font-family: sans-serif;
    font-weight: 600;
    transition: background-color 0.2s;
  }

  .sendCommandButton:hover {
    background-color: rgb(74, 71, 231);
  }

  .sendCommandButton:active {
    background-color: rgb(29, 27, 148);
  }
</style>
