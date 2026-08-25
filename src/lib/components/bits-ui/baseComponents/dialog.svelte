<script>
  import { Dialog, Label } from "bits-ui";
  import Separator from "./Separator.svelte";
  import X from "phosphor-svelte/lib/X";
  import { uiStore } from "../uiComponentsStore.svelte";
  import { onDestroy, untrack } from "svelte";
  let {
    open = $bindable(false),
    triggerButton,
    closeButton,
    contentProps,
    title,
    description,
    children,
    name,
    contentClass,
    empty = false,
    ...others
  } = $props();

  // Open the dialog from the store
  let dialogOpenTrigger = $derived(uiStore.isDialogOpen(name));
  $effect(() => {
    if (dialogOpenTrigger) {
      open = true;
    } else {
      open = false;
    }
  });

  // Close the window in the store on standard closure
  $effect(() => {
    open;
    untrack(() => {
      if (!open) {
        uiStore.closeDialog(name);
      }
    });
  });
</script>

<Dialog.Root bind:open {...others}>
  <Dialog.Trigger class="bg-transparent h-fit w-fit p-0 border-none">
    {@render triggerButton?.()}
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay
      class="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 fixed inset-0 z-50 bg-black/80"
    />
    <Dialog.Content
      class="rounded-card-lg bg-background-dark shadow-popover data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 outline-hidden fixed left-[50%] top-[50%] z-9999 w-full max-w-[calc(100% - 2rem)] translate-x-[-50%] translate-y-[-50%] border p-5 sm:max-w-122.5 md:w-full flex flex-col max-h-170 overflow-y-scroll overflow-x-hidden"
    >
      {#if !empty}
        <Dialog.Title
          class="flex w-full items-center justify-center text-lg font-semibold tracking-tight"
        >
          {title}
        </Dialog.Title>
        <div class="mt-5 mb-6">
          <Separator />
        </div>

        <div
          class={`relative flex flex-col gap-5 ${contentClass}`}
          {...contentProps}
        >
          <Dialog.Description class="text-foreground-alt text-sm">
            {description}
          </Dialog.Description>
          {@render children?.()}
          {#if closeButton}
            <div class="w-full flex flex-row justify-end">
              <Dialog.Close
                class="w-fit h-fit outline-none border-none bg-transparent right-5"
              >
                {@render closeButton?.()}
              </Dialog.Close>
            </div>
          {/if}
        </div>
        <Dialog.Close
          class="focus-visible:ring-foreground focus-visible:ring-offset-background focus-visible:outline-hidden absolute right-5 top-5 rounded-md focus-visible:ring-2 focus-visible:ring-offset-2 active:scale-[0.98] bg-transparent border-none outline-hidden "
        >
          <div>
            <X class="text-foreground size-5" />
            <span class="sr-only">Close</span>
          </div>
        </Dialog.Close>
      {:else}
        {@render children?.()}
      {/if}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
