<template>
  <footer class="gc-site-footer">
    <div class="gc-footer-inner">
      <div class="gc-footer-card">
        <div class="gc-footer-grid">
          <div class="gc-footer-brand-col">
            <span class="gc-logo-mark">G</span>
            <ul class="gc-contact-list">
              <li class="gc-contact-item">
                <q-icon name="place" size="16px" />
                <span>{{ siteConfig.contact.address }}</span>
              </li>
              <li class="gc-contact-item">
                <q-icon name="call" size="16px" />
                <a :href="`tel:${siteConfig.contact.phone}`" class="gc-contact-link">
                  {{ siteConfig.contact.phone }}
                </a>
              </li>
              <li class="gc-contact-item">
                <q-icon name="mail" size="16px" />
                <a :href="`mailto:${siteConfig.contact.email}`" class="gc-contact-link">
                  {{ siteConfig.contact.email }}
                </a>
              </li>
            </ul>
          </div>

          <div v-for="column in columns" :key="column.label" class="gc-footer-col">
            <span class="gc-footer-label">{{ t(`footer.${column.label}`) }}</span>
            <ul class="gc-footer-links">
              <li v-for="link in column.links" :key="link.path">
                <router-link :to="link.path" class="gc-footer-link">
                  {{ t(link.labelKey) }}
                </router-link>
              </li>
            </ul>
          </div>
        </div>

        <div class="gc-footer-bottom">
          <div class="gc-footer-bottom-text">
            <span>
              Copyright &copy; {{ siteConfig.legal.copyrightYear }} {{ siteConfig.legal.company }}.
              {{ t('footer.rightsReserved') }}
            </span>
            <span class="gc-footer-bottom-divider">|</span>
            <router-link to="/privacy" class="gc-footer-link">
              {{ t('footer.privacyPolicy') }}
            </router-link>
            <span class="gc-footer-bottom-divider">|</span>
            <router-link to="/terms" class="gc-footer-link">
              {{ t('footer.termsOfService') }}
            </router-link>
          </div>

          <ul class="gc-social-list">
            <li>
              <a
                :href="siteConfig.social.facebook"
                target="_blank"
                rel="noopener noreferrer"
                class="gc-social-link"
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
                class="gc-social-link gc-social-instagram"
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
                class="gc-social-link gc-social-youtube"
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
                class="gc-social-link gc-social-telegram"
                aria-label="Telegram"
              >
                <q-icon name="send" size="18px" />
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { siteConfig } from 'src/config/site';

const { t } = useI18n();

interface FooterLink {
  path: string;
  labelKey: string;
}

interface FooterColumn {
  label: 'menuLabel' | 'servicesLabel' | 'aboutLabel';
  links: FooterLink[];
}

const columns: FooterColumn[] = [
  {
    label: 'menuLabel',
    links: [
      { path: '/', labelKey: 'nav.home' },
      { path: '/testimonial', labelKey: 'nav.testimonial' },
      { path: '/contact', labelKey: 'nav.contact' },
      { path: '/blog', labelKey: 'nav.blog' },
    ],
  },
  {
    label: 'servicesLabel',
    links: [
      { path: '/services/tourism', labelKey: 'services.tourism.title' },
      { path: '/services/work', labelKey: 'services.work.title' },
      { path: '/services/study', labelKey: 'services.study.title' },
      { path: '/services/visa', labelKey: 'services.visa.title' },
    ],
  },
  {
    label: 'aboutLabel',
    links: [
      { path: '/about', labelKey: 'footer.aboutUs' },
      { path: '/about/team', labelKey: 'footer.ourTeam' },
      { path: '/partnership', labelKey: 'footer.partnership' },
      { path: '/careers', labelKey: 'footer.career' },
    ],
  },
];
</script>

<style scoped lang="scss">
.gc-site-footer {
  background: var(--gc-bg);
  padding: 32px 16px 48px;
}

.gc-footer-inner {
  max-width: 1600px;
  margin: 0 auto;
}

.gc-footer-card {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-lg);
  padding: 40px 32px 32px;
}

.gc-footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;

  @media (min-width: 720px) {
    grid-template-columns: 1.3fr 1fr 1fr 1fr;
    gap: 24px;
  }
}

.gc-footer-brand-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.gc-logo-mark {
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

.gc-contact-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-contact-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--gc-text);
}

.gc-contact-link {
  color: var(--gc-text);
  text-decoration: none;

  &:hover {
    color: var(--gc-primary);
  }
}

.gc-footer-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.gc-footer-label {
  align-self: flex-start;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: var(--gc-radius-pill);
  letter-spacing: 0.01em;
}

.gc-footer-links {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.gc-footer-link {
  font-size: 13px;
  color: var(--gc-text);
  text-decoration: none;

  &:hover {
    color: var(--gc-primary);
  }
}

.gc-footer-bottom {
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid var(--gc-border);
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;

  @media (min-width: 720px) {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 24px;
  }
}

.gc-footer-bottom-text {
  font-size: 12px;
  color: var(--gc-text-muted);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  text-align: center;

  @media (min-width: 720px) {
    text-align: left;
  }
}

.gc-footer-bottom-divider {
  color: var(--gc-border);
}

.gc-social-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 8px;
}

.gc-social-link {
  width: 32px;
  height: 32px;
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

.gc-social-instagram {
  background: linear-gradient(135deg, #f58529 0%, #dd2a7b 50%, #515bd4 100%);
}

.gc-social-youtube {
  background: #ff0000;
}

.gc-social-telegram {
  background: #229ed9;
}
</style>
