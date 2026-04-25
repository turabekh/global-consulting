<template>
  <q-layout view="hHh lpr fFf">
    <SiteHeader @open-mobile-menu="mobileOpen = true" />
    <MobileDrawer v-model="mobileOpen" />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SiteHeader from 'src/components/layout/SiteHeader.vue';
import MobileDrawer from 'src/components/layout/MobileDrawer.vue';

const mobileOpen = ref(false);
</script>
