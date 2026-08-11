<script>
  import { Dialog, Label } from "bits-ui";
  import Separator from "./Separator.svelte";
  import X from "phosphor-svelte/lib/X";
  import Button from "./Button.svelte";

  let {
    open = $bindable(false),
    triggerButton,
    closeButton,
    contentProps,
    title,
    description,
    cancelLabel = "Annuler",
    confirmLabel = "Confirmer",
    onConfirm = () => {},
    children,
    ...others
  } = $props();


  // Open the dialog from the store
  let dialogOpenTrigger = $derived(uiStore.isDialogOpen(name));
  $effect(() => {
    if (dialogOpenTrigger) {
      open = true;
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
      class="rounded-[15px] bg-background-dark shadow-popover data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 outline-hidden fixed left-[50%] top-[50%] z-50 w-full max-w-[calc(100% - 2rem)] translate-x-[-50%] translate-y-[-50%] border p-5 flex flex-col max-w-110"
      {...contentProps}
    >
      <Dialog.Title
        class="flex w-full items-center text-2xl font-semibold tracking-tight"
      >
        {title}
      </Dialog.Title>
      <div class="relative flex flex-col gap-5 mt-4">
        <Dialog.Description class="text-foreground-alt text-sm">
          {description}
        </Dialog.Description>
        <div class="mb-3">
          <Separator />
        </div>
        {@render children?.()}
      </div>

      <div class="w-full relative flex flex-row gap-2 justify-end">
        <Dialog.Close
          class="bg-transparent p-0 w-fit h-fit border-none outline-hidden "
        >
          <Button iconPath="">{cancelLabel}</Button>
        </Dialog.Close>
        <Button emphasize onclick={onConfirm} iconPath="">{confirmLabel}</Button
        >
      </div>

      <Dialog.Close
        class="focus-visible:ring-foreground focus-visible:ring-offset-background focus-visible:outline-hidden absolute right-5 top-5 rounded-md focus-visible:ring-2 focus-visible:ring-offset-2 active:scale-[0.98] bg-transparent border-none outline-hidden "
      >
        <div>
          <X class="text-foreground size-4" />
          <span class="sr-only">Close</span>
        </div>
      </Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
