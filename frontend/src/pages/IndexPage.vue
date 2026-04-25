<template>
  <q-page class="row items-center justify-evenly">
    <div class="column items-center q-gutter-md">
      <h3>{{ t('app.name') }}</h3>
      <p>{{ t('auth.login.title') }}</p>
      <p>{{ t('auth.login.subtitle') }}</p>

      <q-btn-group>
        <q-btn
          :label="'EN'"
          :color="locale === 'en' ? 'primary' : 'grey'"
          @click="switchLocale('en')"
        />
        <q-btn
          :label="'UZ'"
          :color="locale === 'uz' ? 'primary' : 'grey'"
          @click="switchLocale('uz')"
        />
      </q-btn-group>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { setLocale } from 'src/boot/i18n';
import type { SupportedLocale } from 'src/i18n';

const { t, locale } = useI18n();

function switchLocale(newLocale: SupportedLocale) {
  setLocale(newLocale);
}
</script>
