<template>
  <q-layout view="hHh lpR fFf">
    <div class="gc-dash-shell">
      <div class="gc-dash-sidebar-wrap">
        <DashboardSidebar />
      </div>

      <div class="gc-dash-main">
        <DashboardTopbar :title="pageTitle" @open-mobile-menu="mobileOpen = true" />

        <main class="gc-dash-content">
          <router-view v-slot="{ Component }">
            <component :is="Component" @page-title="onPageTitle" />
          </router-view>
        </main>
      </div>
    </div>

    <q-drawer v-model="mobileOpen" side="left" overlay behavior="mobile" :width="280">
      <DashboardSidebar />
    </q-drawer>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import DashboardSidebar from 'src/components/dashboard/DashboardSidebar.vue';
import DashboardTopbar from 'src/components/dashboard/DashboardTopbar.vue';

const route = useRoute();
const { t } = useI18n();

const mobileOpen = ref(false);
const pageTitle = ref(t('dashboard.breadcrumb.home'));

function onPageTitle(title: string) {
  pageTitle.value = title || t('dashboard.breadcrumb.home');
}

watch(
  () => route.fullPath,
  () => {
    mobileOpen.value = false;
  },
);
</script>

<style scoped lang="scss">
.gc-dash-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 1fr;
  background: var(--gc-bg-soft);

  @media (min-width: 1024px) {
    grid-template-columns: 260px 1fr;
  }
}

.gc-dash-sidebar-wrap {
  display: none;

  @media (min-width: 1024px) {
    display: block;
    position: sticky;
    top: 0;
    height: 100vh;
  }
}

.gc-dash-main {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.gc-dash-content {
  flex: 1;
  padding: 24px 16px 64px;

  @media (min-width: 720px) {
    padding: 32px 32px 64px;
  }
}
</style>
