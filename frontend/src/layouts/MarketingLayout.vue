<template>
  <q-layout view="hHh lpr fFf">
    <SiteHeader @open-mobile-menu="mobileOpen = true" />
    <MobileDrawer v-model="mobileOpen" />
    <q-page-container>
      <router-view />
    </q-page-container>
    <SiteFooter />

    <ContactFormDialog v-model="dialogs.contactOpen" />
    <PartnershipFormDialog v-model="dialogs.partnershipOpen" />
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SiteHeader from 'src/components/layout/SiteHeader.vue';
import SiteFooter from 'src/components/layout/SiteFooter.vue';
import MobileDrawer from 'src/components/layout/MobileDrawer.vue';
import ContactFormDialog from 'src/components/forms/ContactFormDialog.vue';
import PartnershipFormDialog from 'src/components/forms/PartnershipFormDialog.vue';
import { useDialogsStore } from 'src/stores/dialogs';

const mobileOpen = ref(false);
const dialogs = useDialogsStore();
</script>
