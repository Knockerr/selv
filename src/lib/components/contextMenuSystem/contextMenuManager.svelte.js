// @ts-nocheck
import {
  SvelteMap,
  SvelteSet
} from 'svelte/reactivity';

let openMenu = $state(null);

export const contextManager = {
  get openMenu(){
    return openMenu;
  },
  get isAMenuOpen(){
    return !(openMenu===null);
  },
  isOpen(contextName){
    return openMenu===null
  },
  open(contextName) {
    console.log("Opening ", contextName);
    openMenu = contextName;
  },
  close() {
    openMenu = null;
  }
};