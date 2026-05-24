// @ts-nocheck
import {
  SvelteMap,
  SvelteSet
} from 'svelte/reactivity';

let openWindows = new SvelteSet();

export const windowsManager = {
  get openWindows() {
    return openWindows;
  },
  isOpen(windowId) {
    return openWindows.has(windowId);
  },
  closeAll() {
    openWindows.clear();
  },
  open(windowId) {
    openWindows.add(windowId);
  },
  close(windowId) {
    openWindows.delete(windowId);
  }
};
