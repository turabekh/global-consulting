<template>
  <q-layout view="hHh lpr fFf">
    <q-page-container>
      <q-page class="gc-auth-page">
        <div class="gc-auth-shell">
          <div class="gc-auth-form">
            <div class="gc-auth-form-inner">
              <div class="gc-auth-header">
                <div class="gc-logo">G</div>
                <q-btn
                  flat
                  dense
                  size="sm"
                  :icon="locale === 'uz' ? 'language' : 'language'"
                  :label="locale.toUpperCase()"
                  class="gc-locale-toggle"
                  @click="toggleLocale"
                />
              </div>

              <router-view />
            </div>
          </div>

          <aside class="gc-auth-art" aria-hidden="true">
            <div class="gc-gradient-bg gc-art-canvas"></div>
          </aside>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { setLocale } from 'src/boot/i18n';

const { locale } = useI18n();

function toggleLocale() {
  setLocale(locale.value === 'en' ? 'uz' : 'en');
}
</script>

<style scoped lang="scss">
.gc-auth-page {
  min-height: 100vh;
  background: var(--gc-bg);
}

.gc-auth-shell {
  display: grid;
  grid-template-columns: 1fr;
  min-height: 100vh;

  @media (min-width: 900px) {
    grid-template-columns: minmax(420px, 1fr) 1fr;
  }
}

.gc-auth-form {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
}

.gc-auth-form-inner {
  width: 100%;
  max-width: 380px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.gc-auth-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.gc-logo {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #c084fc 0%, #ec4899 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: -0.02em;
}

.gc-locale-toggle {
  border-radius: var(--gc-radius-pill);
  font-weight: 500;
  letter-spacing: 0.05em;
}

.gc-auth-art {
  display: none;
  padding: 16px;

  @media (min-width: 900px) {
    display: block;
  }
}

.gc-art-canvas {
  width: 100%;
  height: 100%;
  border-radius: var(--gc-radius-lg);
}
</style>
