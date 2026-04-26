import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useDialogsStore = defineStore('dialogs', () => {
  const contactOpen = ref(false);
  const partnershipOpen = ref(false);

  function openContact() {
    contactOpen.value = true;
  }

  function openPartnership() {
    partnershipOpen.value = true;
  }

  return {
    contactOpen,
    partnershipOpen,
    openContact,
    openPartnership,
  };
});
