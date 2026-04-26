<template>
  <q-page class="gc-contact-page">
    <div class="gc-contact-shell">
      <header class="gc-contact-header">
        <h1 class="gc-contact-title">
          {{ t('pages.contact.title') }}
          <span class="gc-gradient-text">{{ t('pages.contact.titleHighlight') }}</span>
        </h1>
        <p class="gc-contact-subtitle">{{ t('pages.contact.subtitle') }}</p>
      </header>

      <div class="gc-contact-grid">
        <aside class="gc-contact-info">
          <h2 class="gc-info-heading">{{ t('pages.contact.infoTitle') }}</h2>

          <ul class="gc-info-list">
            <li class="gc-info-item">
              <div class="gc-info-icon">
                <q-icon name="place" size="20px" />
              </div>
              <div class="gc-info-text">
                <span class="gc-info-label">{{ t('pages.contact.addressLabel') }}</span>
                <span class="gc-info-value">{{ siteConfig.contact.address }}</span>
              </div>
            </li>

            <li class="gc-info-item">
              <div class="gc-info-icon">
                <q-icon name="call" size="20px" />
              </div>
              <div class="gc-info-text">
                <span class="gc-info-label">{{ t('pages.contact.phoneLabel') }}</span>
                <a :href="`tel:${siteConfig.contact.phone}`" class="gc-info-link">
                  {{ siteConfig.contact.phone }}
                </a>
              </div>
            </li>

            <li class="gc-info-item">
              <div class="gc-info-icon">
                <q-icon name="mail" size="20px" />
              </div>
              <div class="gc-info-text">
                <span class="gc-info-label">{{ t('pages.contact.emailLabel') }}</span>
                <a :href="`mailto:${siteConfig.contact.email}`" class="gc-info-link">
                  {{ siteConfig.contact.email }}
                </a>
              </div>
            </li>

            <li class="gc-info-item">
              <div class="gc-info-icon">
                <q-icon name="schedule" size="20px" />
              </div>
              <div class="gc-info-text">
                <span class="gc-info-label">{{ t('pages.contact.hoursLabel') }}</span>
                <div class="gc-info-hours">
                  <span class="gc-info-hours-row">
                    <span>{{ t('pages.contact.hoursWeekday') }}</span>
                    <span class="gc-info-hours-time">{{
                      t('pages.contact.hoursWeekdayTime')
                    }}</span>
                  </span>
                  <span class="gc-info-hours-row">
                    <span>{{ t('pages.contact.hoursWeekend') }}</span>
                    <span class="gc-info-hours-time">{{
                      t('pages.contact.hoursWeekendTime')
                    }}</span>
                  </span>
                </div>
              </div>
            </li>
          </ul>

          <ul class="gc-info-social">
            <li>
              <a
                :href="siteConfig.social.facebook"
                target="_blank"
                rel="noopener noreferrer"
                class="gc-info-social-link"
                aria-label="Facebook"
              >
                <q-icon name="facebook" size="18px" />
              </a>
            </li>
            <li>
              <a
                :href="siteConfig.social.instagram"
                target="_blank"
                rel="noopener noreferrer"
                class="gc-info-social-link gc-info-social-instagram"
                aria-label="Instagram"
              >
                <q-icon name="photo_camera" size="18px" />
              </a>
            </li>
            <li>
              <a
                :href="siteConfig.social.youtube"
                target="_blank"
                rel="noopener noreferrer"
                class="gc-info-social-link gc-info-social-youtube"
                aria-label="YouTube"
              >
                <q-icon name="smart_display" size="18px" />
              </a>
            </li>
            <li>
              <a
                :href="siteConfig.social.telegram"
                target="_blank"
                rel="noopener noreferrer"
                class="gc-info-social-link gc-info-social-telegram"
                aria-label="Telegram"
              >
                <q-icon name="send" size="18px" />
              </a>
            </li>
          </ul>
        </aside>

        <div class="gc-contact-form-wrap">
          <header class="gc-form-card-header">
            <h2 class="gc-form-card-title">{{ t('forms.contact.title') }}</h2>
            <p class="gc-form-card-subtitle">{{ t('forms.contact.subtitle') }}</p>
          </header>

          <ContactForm @done="onDone" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { siteConfig } from 'src/config/site';
import ContactForm from 'src/components/forms/ContactForm.vue';

const { t } = useI18n();

function onDone() {}
</script>

<style scoped lang="scss">
.gc-contact-page {
  background: var(--gc-bg);
  padding: 48px 16px 96px;

  @media (min-width: 720px) {
    padding: 80px 16px 128px;
  }
}

.gc-contact-shell {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.gc-contact-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}

.gc-contact-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 48px;
  }
}

.gc-contact-subtitle {
  font-size: 15px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 540px;
  line-height: 1.5;
}

.gc-contact-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;

  @media (min-width: 900px) {
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: start;
  }
}

.gc-contact-info {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-lg);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;

  @media (min-width: 720px) {
    padding: 40px 32px;
  }
}

.gc-info-heading {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-info-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.gc-info-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.gc-info-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.gc-info-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.gc-info-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
  font-weight: 600;
}

.gc-info-value {
  font-size: 14px;
  color: var(--gc-text);
  line-height: 1.4;
}

.gc-info-link {
  font-size: 14px;
  color: var(--gc-text);
  text-decoration: none;

  &:hover {
    color: var(--gc-primary);
  }
}

.gc-info-hours {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-info-hours-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  font-size: 13px;
  color: var(--gc-text);
}

.gc-info-hours-time {
  color: var(--gc-text-muted);
  font-weight: 500;
}

.gc-info-social {
  list-style: none;
  margin: 0;
  padding: 16px 0 0;
  border-top: 1px solid var(--gc-border);
  display: flex;
  gap: 8px;
}

.gc-info-social-link {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #1877f2;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: transform 0.15s ease;

  &:hover {
    transform: translateY(-2px);
  }
}

.gc-info-social-instagram {
  background: linear-gradient(135deg, #f58529 0%, #dd2a7b 50%, #515bd4 100%);
}

.gc-info-social-youtube {
  background: #ff0000;
}

.gc-info-social-telegram {
  background: #229ed9;
}

.gc-contact-form-wrap {
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  border-radius: var(--gc-radius-lg);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;

  @media (min-width: 720px) {
    padding: 40px 32px;
  }
}

.gc-form-card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-form-card-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-form-card-subtitle {
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 0;
}
</style>
